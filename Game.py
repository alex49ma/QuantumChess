import Position
import Piece
import Move
import random
from utils import ChessUtils

class Game:
    def __init__(self):
        self.QMovesAllowed = 3
        self.QMovesWhite = 0
        self.QMovesBlack = 0
        self.position = Position.Position(self.setInitPieces())
        self.moveList = []
        self.flags = "w KQkq - 0 1"
        self.flagList = self.flags.split()
        self.linked = []

        self.over = False

    def setInitPieces(self, board = ["rnbqkbnr", "pppppppp", "........", "........", "........", "........", "PPPPPPPP", "RNBQKBNR"]):
        # Input:
        #       Optional list of string representing the list of rows
        # Output:
        #       The piece matrix initialized with all its pieces inside
        pieceMatrix = []
        row = 0
        while row < 8:
            col = 0
            rowList = []
            while col < 8:
                if board[row][col] != ".":
                    piece = Piece.Piece(board[row][col])
                    rowList.append(piece)
                else:
                    rowList.append(None)
                col += 1
            pieceMatrix.append(rowList)
            row += 1
        return pieceMatrix
    
    def setPosition(self, position):
        # Input:
        #       Position we want to set
        # Output:
        #       None
        self.position = position
    
    def move(self, moveStr):
        # Input:
        #       Move string. Move that we want to make
        # Action:
        #       Checks captures and validity, merges and manages entanglement. Also calls a method to manage flags
        # Output:
        #       None
        move = Move.Move(moveStr, self.flagList)
        piece = self.position.getWhatIsOnSquare(move.move[0:2])
        if move.isValid(self.position):
            interferencers = list(set(ChessUtils.getInterference(self.position, move.move)))
            if move.isCapture(self.position):
                capturer = piece
                captured = self.position.getWhatIsOnSquare(move.move[2:4])
                
                for indexMove in interferencers:
                    choice = random.randint(0, 1)
                    self.position = self.position.mergePosition(indexMove, choice)
                    if self.moveList[indexMove].move0.flags[0] == "w":              # The piece that provokes the Quantum entanglement needs to be defined
                        self.QMovesWhite -=1     # When merging, we give back the possibility to make more quantic moves
                    else:
                        self.QMovesBlack -=1

                if capturer.isQuantic():
                    listToMerge = self.getListToMerge(moveStr[0:2], capturer)
                    for indexMove in listToMerge:
                        choice = random.randint(0, 1)
                        self.position = self.position.mergePosition(indexMove, choice)
                        if self.flagList[0] == "w":     # When merging, we give back the possibility to make more quantic moves
                            self.QMovesWhite -=1
                        else:
                            self.QMovesBlack -=1
                if captured == None: ### ONLY HAPPENS WHEN EN PASSENT
                    if move.move[3] == "6" and move.move[1] == "5":
                        captured = self.position.getWhatIsOnSquare(move.move[2] + str(5))
                    if move.move[3] == "3" and move.move[1] == "4":
                        captured = self.position.getWhatIsOnSquare(move.move[2] + str(4))
                if captured.isQuantic():
                    listToMerge = self.getListToMerge(moveStr[2:4], captured)
                    for indexMove in listToMerge:
                        choice = random.randint(0, 1)
                        self.position = self.position.mergePosition(indexMove, choice)
                        if self.flagList[0] == "b":
                            self.QMovesWhite -=1
                        else:
                            self.QMovesBlack -=1
            if move.isValid(self.position):          # Move must still be valid after merging to be executed
                self.position = self.position.makeMove(move)
            self.moveList.append(move)
            
            self.flagList[0] = "w" if self.flagList[0] == "b" else "b" if self.flagList[0] == "w" else self.flagList[0]
            self.updateFlags(move, piece.pieceClass)
            self.link(move)
            self.deQuantify()
            return True
        else:
            print("Move not valid")
            return False

    def getListToMerge(self, sq, piece):
        # Input:
        #       A string that represents a square, with a character and a number
        # Action:
        #       Checks in the linked list all the other pieces he is linked to and his merging indexes
        # Output:
        #       A list with the merging indexes of this piece and all others linked to
        listMerged = []
        for links in self.linked:
            if sq in links:
                for squareLinked in links:
                    piece = self.position.getWhatIsOnSquare(squareLinked)
                    if isinstance(piece, Piece.Piece):
                        listMerged = list(set(listMerged) | set(piece.listMoves))
        return listMerged


    def qMove(self, moveStr0, moveStr1):
        # Input:
        #       Two Move string. Moves that we want to make
        # Action:
        #       Checks validity, captures not allowed, manages merging indexes. Also calls a method to manage flags
        # Output:
        #       Boolean: if the move has been performed or not
        move0 = Move.Move(moveStr0, self.flagList)
        move1 = Move.Move(moveStr1, self.flagList)
        qMove = Move.QuanticMove(move0, move1)
        piece = self.position.getWhatIsOnSquare(moveStr0[0:2])
        if qMove.isValid(self.position):
            if (self.flagList[0] == "w" and self.QMovesWhite < self.QMovesAllowed):
                self.setPosition(self.position.makeMove(qMove))
                self.position.addToAllOnSquare(moveStr0[2:4], ([len(self.moveList)]))
                self.position.addToAllOnSquare(moveStr1[2:4], ([len(self.moveList)]))
                self.QMovesWhite += 1
                self.flagList[0] = "b"
                self.moveList.append(qMove)
                self.updateFlags(qMove, piece.pieceClass)
                self.deQuantify()
                self.link(qMove)
                self.linked.append([moveStr0[2:4], moveStr1[2:4]])
                return True
            elif(self.flagList[0] == "w" and self.QMovesWhite >= self.QMovesAllowed):
                print("No more Qmoves allowed for white")
                return False
            if (self.flagList[0] == "b" and self.QMovesBlack < self.QMovesAllowed):
                self.setPosition(self.position.makeMove(qMove))
                self.position.addToAllOnSquare(moveStr0[2:4], ([len(self.moveList)]))
                self.position.addToAllOnSquare(moveStr1[2:4], ([len(self.moveList)]))
                self.QMovesBlack += 1
                self.flagList[0] = "w"
                self.moveList.append(qMove)
                self.updateFlags(qMove, piece.pieceClass)
                self.deQuantify()
                self.link(qMove)
                self.linked.append([moveStr0[2:4], moveStr1[2:4]])

                return True
            elif(self.flagList[0] == "b" and self.QMovesBlack >= self.QMovesAllowed):
                print("No more Qmoves allowed for black")
                return False
        else:
            print("Move not valid")
            return False
        
    def link(self, move):
        # Input:
        #       Move object, movement that has been done
        # Action:
        #       Alters the self.linked list, containing the squares where are quantum pieces that are linked to each other
        # Output:
        #       None
        if move.isQuantic():
            self.link(move.move0)
            self.link(move.move1)
        else:
            for i in range(len(self.linked)):  
                objective = move.move[0:2]
                subs = move.move[2:4]
                if objective in self.linked[i]:
                    self.linked[i][self.linked[i].index(objective)] = subs

    def deQuantify(self):
        # Input:
        #       None
        # Action:
        #       Checks square by square if each piece is quantic. Checks if each king is alive or not and sets the winner.
        # Output:
        #       None
        isWhiteAlive = False
        isBlackAlive = False
        for row in range(8):
            for col in range(8):
                piece = self.position.deQuantify(row, col)
                if piece != None:
                    if piece.pieceClass in "k":
                        isBlackAlive = True
                    if piece.pieceClass in "K":
                        isWhiteAlive = True
                    if not piece.isQuantic():
                        square = ""
                        square += chr(col + ord('a'))
                        square += str(row + 1)
                        self.position.setPiece(piece, square)
        if not isWhiteAlive:
            self.over = "Black Wins!"
        if not isBlackAlive:
            self.over = "White Wins!"

    def updateFlags(self, move, piece):
        # Input:
        #       The move we just completed and the piece class of the moved piece
        # Action:
        #       Updates flags, castle, en passent. It also promotes the pawn in case it happens to the demanded piece
        # Output:
        #       None
        if piece == "K":
            self.flagList[1].replace("KQ", "")
        if piece == "k":
            self.flagList[1].replace("kq", "")
        if (isinstance(move, Move.QuanticMove)):
            if move.move1.move[3] =="4":
                squares = move.move0.move
            else:
                squares = move.move1.move
        else:
            squares = move.move[0:4]
        if squares[0:2] == "a1":
            self.flagList[1].replace("Q", "")
        if squares[0:2] == "h1":
            self.flagList[1].replace("K", "")
        if squares[0:2] == "a8":
            self.flagList[1].replace("q", "")
        if squares[0:2] == "h8":
            self.flagList[1].replace("k", "")
        if piece == "P" and int(squares[1]) - int(squares[3]) == -2:
            self.flagList[2] = squares[0] + str(3)
        elif piece == "p" and int(squares[1]) - int(squares[3]) == 2:
            self.flagList[2] = squares[0] + str(6)
        else:
            self.flagList[2] == "-"

        if piece in "Pp":
            if (piece.islower() and squares[3] == '1') or ((piece.isupper()) and squares[3] == '8'):
                promoted = self.position.getWhatIsOnSquare(squares[2:4])
                if move.flags[0] == "b":
                    promoted.pieceClass = move.move[4].upper()
                else:
                    promoted.pieceClass = move.move[4].lower()

    def evaluate(self, movestr0 =0, movestr1 = 0):
        # Input:
        #       Optional move and optional second move if quantum
        # Output:
        #       An evaluation of the position, the position after certain move or the position after certain quantum move
        timeOut = 10
        if movestr1 != 0:
            move = Move.QuanticMove(Move.Move(movestr0, self.flagList), Move.Move(movestr1, self.flagList))
            return ChessUtils.evalMoveFormula(self.position, self.flagList, move, timeOut)
        elif movestr0 != 0:
            move = Move.Move(movestr0, self.flagList)
            return ChessUtils.evalMoveFormula(self.position, self.flagList, move, timeOut)
        moveClass = Move.QuanticMove(Move.Move("", self.flags), Move.Move("", self.flags))
        return ChessUtils.evalPosition(self.position, moveClass, self.flagList, timeOut)
    
    def moveHint(self):
        return ChessUtils.moveHint(self.position, self.flagList)