import math
import chess
import copy
import Position
import Piece
#import stockfish
from stockfish import Stockfish

stockfish = Stockfish(path="./Stockfish/stockfish_15_x64_avx2.exe")

class ChessUtils:

    def get_piece_unicode(piece_string):
            # Input:
            #       String with the piece class
            # Output:
            #       The assigned unicode for the piece class
        piece_mapping = {
            'P': '♟', #'\u265F',
            'R': '♜',
            'N': '♞',
            'B': '♝',
            'Q': '♛',
            'K': '♚',
            'p': '♙',
            'r': '♖',
            'n': '♘',
            'b': '♗',
            'q': '♕',
            'k': '♔'       #'\u2654'
        }

        return piece_mapping.get(piece_string, '')
    
    def isValid(position, move):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic
            # Output:
            #       If the move is valid or not
        flags = move.flags
        if len(move.move) < 4:
            return False
        if move.move[0:2] == move.move[2:4]:
            return False
        if ord(move.move[2]) > ord('h') | ord(move.move[2]) < ord('a'):
            return False
        if int(move.move[3]) > 8 | int(move.move[3]) < 1:
            return False
        piece = position.getWhatIsOnSquare(move.move) 
        otherPiece = position.getWhatIsOnSquare(move.move[2:])
        if piece is not None:
            if flags[0] == "w" and piece.pieceClass.islower():
                return False
            if flags[0] == "b" and piece.pieceClass.isupper():
                return False
            if otherPiece is not None:
                if piece.pieceClass.islower() == otherPiece.pieceClass.islower():
                    return False
            match piece.pieceClass:
                case "k" | "K":
                    return ChessUtils.kingMoveValid(position, move.move, flags)
                case "q" | "Q":
                    return ChessUtils.queenMoveValid(position, move.move)
                case "r" | "R":
                    return ChessUtils.rookMoveValid(position, move.move)
                case "b" | "B":
                    return ChessUtils.bishMoveValid(position, move.move)
                case "n" | "N":
                    return ChessUtils.knightMoveValid(position, move.move)
                case "p" | "P":
                    return ChessUtils.pawnMoveValid(position, move.move, flags)
                
    def kingMoveValid(position, move, flags):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a king
            # Output:
            #       If the move is valid or not
        if abs(int(ord(move[0])) - int(ord(move[2]))) <= 1 & abs(int(move[1]) - int(move[3])) <= 1:
            return True
        else:
            if move[2:] == "g1" and "K" in flags[1] and move[:2] == "e1":
                return True
            if move[2:] == "c1" and "Q" in flags[1] and move[:2] == "e1":
                return True
            if move[2:] == "g8" and "k" in flags[1] and move[:2] == "e8":
                return True
            if move[2:] == "c8" and "q" in flags[1] and move[:2] == "e8":
                return True
                    
    def queenMoveValid(position, move):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a queen
            # Output:
            #       If the move is valid or not
        movementInCols = ord(move[2]) - ord(move[0])
        movementInRows = int(move[3]) - int(move[1])
        if abs(movementInCols) == abs(movementInRows): # Diagonal Movement
            for i in range(1, abs(movementInCols)):
                col = int(math.copysign(i, movementInCols))
                row = int(math.copysign(i, movementInRows))
                if position.getWhatIsOnSquare(str(chr(ord(move[0]) + col)) + str(int(move[1]) + row)) is not None:
                    return False
            return True
        else:
            if movementInRows == 0:
                for i in range(1, abs(movementInCols)):
                    col = int(math.copysign(i, movementInCols))
                    if position.getWhatIsOnSquare(str(chr(ord(move[0]) + col)) + move[1]) is not None:
                        return False
                return True
            else:
                if movementInCols == 0:
                    for i in range(1, abs(movementInRows)):
                        row = int(math.copysign(i, movementInRows))
                        if position.getWhatIsOnSquare(move[0] + str(int(move[1]) + row)) is not None:
                            return False
                    return True
                else:
                    return False
                    
    def rookMoveValid(position, move):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a rook
            # Output:
            #       If the move is valid or not
        movementInCols = ord(move[2]) - ord(move[0])
        movementInRows = int(move[3]) - int(move[1])
        if movementInCols != 0:
            if movementInRows != 0:
                return False
            else:
                for i in range(1, abs(movementInCols)):
                    if position.getWhatIsOnSquare(str(chr(ord(move[0]) + i)) + move[1]) is not None:
                        return False
                return True
        else:
            for i in range(1, abs(movementInRows)):
                row = int(math.copysign(i, movementInRows))
                if position.getWhatIsOnSquare(move[0] + str(int(move[1]) + row)) is not None:
                    return False
            return True
                    
    def bishMoveValid(position, move):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a bishop
            # Output:
            #       If the move is valid or not
        movementInCols = ord(move[2]) - ord(move[0])
        movementInRows = int(move[3]) - int(move[1])
        if abs(movementInCols) != abs(movementInRows): # Diagonal Movement
            return False
        else:
            for i in range(1, abs(movementInCols)):
                col = int(math.copysign(i, movementInCols))
                row = int(math.copysign(i, movementInRows))
                if position.getWhatIsOnSquare(str(chr(ord(move[0]) + col)) + str(int(move[1]) + row)) is not None:
                    return False
            return True
                    
    def knightMoveValid(position, move):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a knight
            # Output:
            #       If the move is valid or not
        movementInCols = ord(move[2]) - ord(move[0])
        movementInRows = int(move[3]) - int(move[1])
        if abs(movementInCols) == 2 and abs(movementInRows) == 1:
            return True
        if abs(movementInCols) == 1 and abs(movementInRows) == 2:
            return True
              
    def pawnMoveValid(position, move, flags):
            # Input:
            #       An object Position, not quantic, not abstract and a move, also not quantic, made by a pawn
            # Output:
            #       If the move is valid or not
        if int(move[1]) == 1 | int(move[1]) == 8:
            return False
        if move[0] == move[2]:
            if abs(int(move[1]) - int(move[3])) == 1 and position.getWhatIsOnSquare(move[2:4]) == None:     # One step pawn move
                if (int(move[1]) - int(move[3]) < 0 and flags[0] == "w") or (int(move[1]) - int(move[3]) > 0 and flags[0] == "b"):
                    if (int(move[3]) == 1 and flags[0] == "b") | (int(move[3]) == 8 and flags[0] == "w"):
                        if len(move) > 4:
                            if move[4] in "qrbnQRBN":
                                return True
                    else:
                        return True
            elif abs(int(move[1]) - int(move[3])) == 2 and position.getWhatIsOnSquare(move[2:4]) == None:   # Two steps pawn move
                dif = (int(move[1]) + int(move[3])) / 2
                if position.getWhatIsOnSquare(move[2] + str(dif)) == None:
                    if (int(move[1]) - int(move[3]) < 0 and flags[0] == "w") or (int(move[1]) - int(move[3]) > 0 and flags[0] == "b"):
                        return True
            return False
        elif abs(ord(move[0]) - ord(move[2])) == 1 and abs(int(move[1]) - int(move[3])) == 1:           # Normal capture pawn move
            if move[2:4] != None:
                captured = position.getWhatIsOnSquare(move[2:4])
                if captured:
                    if (captured.pieceClass.islower() and flags[0] == "w") or (captured.pieceClass.isupper() and flags[0] == "b"):
                        if (int(move[1]) - int(move[3]) < 0 and flags[0] == "w") or (int(move[1]) - int(move[3]) > 0 and flags[0] == "b"):
                            if (int(move[3]) == 1 and flags[0] == "b") | (int(move[3]) == 8 and flags[0] == "w"):
                                if len(move) > 4:
                                    if move[4] in "qrbk":
                                        return True
                            else:
                                return True
            elif len(flags[2]) == 2:
                if flags[2][1] == move[1] and flags[2][0] == move[2]:                                   # En passent pawn move
                    if (int(move[1]) - int(move[3]) < 0 and flags[0] == "w") or (int(move[1]) - int(move[3]) > 0 and flags[0] == "b"):
                        return True
        return False
    
    def isCapture(position, move):
            # Input:
            #       An object Position and a classical move
            # Output:
            #       If the move is a capture or not
        if position.getWhatIsOnSquare(move.move[2:4]) is not None:
            return True
        elif len(move.flags[2]) == 2 and position.getWhatIsOnSquare(move.move[0:2]) is not None:
            if position.getWhatIsOnSquare(move.move[0:2]).pieceClass in "Pp":
                if move.flags[2] == move.move[2:4]:
                    return True
        return False
    
    def isCaptureStr(position, move, flags):
            # Input:
            #       An object Position and a string move
            # Output:
            #       If the move is a capture or not
        if position.getWhatIsOnSquare(move[2:4]) is not None:
            return True
        elif len(flags[2]) == 2 and position.getWhatIsOnSquare(move[0:2]) is not None:
            if position.getWhatIsOnSquare(move[0:2]).pieceClass in "Pp":
                if flags[2] == move[2:4]:
                    return True
        return False
    
    def getInterference(position, move):
            # Input:
            #       An object Position and a move, also not quantic
            # Output:
            #       The index list of moves from all pieces in between origin square and destination.
        result = []
        piece = position.getWhatIsOnSquare(move[0:2])
        if piece is not None:
            if piece.pieceClass in "Nn":
                objective = position.getWhatIsOnSquare(move[2:4])
                if isinstance(objective, Piece.Piece):
                    if piece.pieceClass.islower() == objective.pieceClass.islower():
                        result.extend(objective.listMoves)
                        return result
                return []
            else:
                file1, rank1 = ord(move[0]) - ord('a'), int(move[1])
                file2, rank2 = ord(move[2]) - ord('a'), int(move[3])

            # Iterate over the files and ranks
                if max(file1, file2) - min(file1, file2) > 1:
                    for file in range(min(file1, file2) + 1, max(file1, file2)):
                        if max(rank1, rank2) - min(rank1, rank2) > 1:
                            for rank in range(min(rank1, rank2) + 1, max(rank1, rank2)):
                                square = chr(ord('a') + file) + str(rank)
                                interf = position.getWhatIsOnSquare(square)
                                if interf is not None:
                                    result.extend(interf.listMoves)
                        elif rank1 - rank2 == 0:
                                square = chr(ord('a') + file) + str(rank1)
                                interf = position.getWhatIsOnSquare(square)
                                if interf is not None:
                                    result.extend(interf.listMoves)

                elif file1 - file2 == 0:
                    if max(rank1, rank2) - min(rank1, rank2) > 1:
                        for rank in range(min(rank1, rank2) + 1, max(rank1, rank2)):
                            square = chr(ord('a') + file1) + str(rank)
                            interf = position.getWhatIsOnSquare(square)
                            if interf is not None:
                                result.extend(interf.listMoves)
                    else:
                            square = chr(ord('a') + file1) + str(rank1)
                            interf = position.getWhatIsOnSquare(square)
                            if interf is not None:
                                result.extend(interf.listMoves)
        return result
    
    def evalPosition(position, moveClass, flags, timeOut):
            # Input:
            #       An object Position and a list of flags
            # Output:
            #       An evaluation of the current position
        timeOut -= 1
        if timeOut == 0:
            if isinstance(position, Position.AbstractPosition):
                return ChessUtils.evalPosition(position.position, flags, timeOut)
            if  isinstance(position, Position.QuanticPosition):
                resPos0 = ChessUtils.evalPosition(position.position0, flags, timeOut)
                resPos1 = ChessUtils.evalPosition(position.position1, flags, timeOut)
                return round((resPos0 + resPos1) / 2, 2)
            if isinstance(position, Position.Position):
                fen = position.boardToFen(flags)
                try:
                    stockfish.set_fen_position(fen)
                    result = stockfish.get_evaluation().get("value")/100.0
                    return round(result, 2)
                except:
                    if flags[0] == "w":
                        return 100.0
                    else:
                         return -100.0
        else:
            moves = ChessUtils.moveHint(position, flags)
            return ChessUtils.evalListMoves(position, moveClass, flags, moves, timeOut)
                
    def evalListMoves(position, moveClass, flags, moves, timeOut):
            # Input:
            #       An object Position, a list of flags, a list of moves and the timeOut counter
            # Output:
            #       An evaluation of the best move between the specified moves in the current position
        if flags[0] == "w":
            i = 1
        else:
            i = -1
            best = None
        for move in moves:
            if ", " in move[0]:
                moveCopy = copy.deepcopy(moveClass)
                moveCopy.move0.move = move[0].split(", ")[0]
                moveCopy.move0.flags = copy.deepcopy(flags)
                moveCopy.move1.move = move[0].split(", ")[1]
                moveCopy.move1.flags = copy.deepcopy(flags)
            else:
                moveCopy = copy.deepcopy(moveClass.move0)
                moveCopy.move = move[0]
                moveCopy.flags = copy.deepcopy(flags)
            eval = ChessUtils.evalMoveFormula(position, flags, moveCopy, timeOut)
            best = None
            if best != None:
                best = max(best, eval * i)
            else:
                best = eval
        return best
        
    def evalMove(position, flags, move):
            # Input:
            #       An object Position, a list of flags and a move
            # Output:
            #       An evaluation of the current move in the current position.
        if move.isQuantic():
            return (ChessUtils.evalNMove(position, flags, move.move0.move) + ChessUtils.evalNMove(position, flags, move.move1.move)) / 2
        else:
            return ChessUtils.evalNMove(position, flags, move.move)
        
    def evalMoveFormula(position, flags, move, timeOut):
            # Input:
            #       An object Position, a list of flags and a move
            # Output:
            #       An evaluation of the current move in the current position. Uses the quantum evaluation formula
        timeOut -= 1
        if timeOut == 0:
            return ChessUtils.evalMove(position, flags, move)
        if move.isQuantic():
            moveA = move.move0
            moveB = move.move1
            FuncA = ChessUtils.evalNMove(position, flags, moveA.move)
            FuncB = ChessUtils.evalNMove(position, flags, moveB.move)
            PosAfterA = Position.AbstractPosition(copy.deepcopy(position), moveA)
            PosAfterB = Position.AbstractPosition(copy.deepcopy(position), moveB)
            updatedFlags = ChessUtils.updateFlags(position, move, flags)
            bestForA = ChessUtils.moveHint(PosAfterA, updatedFlags)
            bestForB = ChessUtils.moveHint(PosAfterB, updatedFlags)
            evalCounterA = ChessUtils.evalListMoves(PosAfterA, move, updatedFlags, bestForB, timeOut)
            evalCounterB = ChessUtils.evalListMoves(PosAfterB, move, updatedFlags, bestForA, timeOut)

            
            return (FuncA + FuncB + evalCounterA + evalCounterB) / 4
        else:
            return ChessUtils.evalNMove(position, flags, move.move)
        
    def copyPos(position, move = None):
        # UNUSED, not working propperly
            # Input:
            #       An object Position and an optional move
            # Output:
            #       A copy of the position itself, or the position result after making the move
        if isinstance(position, Position.AbstractPosition):
            return Position.AbstractPosition(copy.deepcopy(position), move)
        if isinstance(position, Position.QuanticPosition):
            return Position.AbstractPosition(copy.deepcopy(position), move)
        if isinstance(position, Position.Position):
            return Position.Position(copy.deepcopy(position.listRows), move)
        else:
            raise Exception("Error, can not copy a position from a non position object")
       
    def evalNMove(position, flags, move):
            # Input:
            #       An object Position, a list of flags and a move that must not be quantic
            # Output:
            #       An evaluation of the current classical move
        if isinstance(position, Position.AbstractPosition):
            return ChessUtils.evalNMove(position.position, flags, move)
        if  isinstance(position, Position.QuanticPosition):
            resPos0 = ChessUtils.evalNMove(position.position0, flags, move)
            resPos1 = ChessUtils.evalNMove(position.position1, flags, move)
            return round((resPos0 + resPos1) / 2, 2)
        if isinstance(position, Position.Position):
            fen = position.boardToFen(flags)
            try:
                stockfish.set_fen_position(fen)
                if stockfish.is_move_correct(move):
                    stockfish.make_moves_from_current_position([move])
                    result = stockfish.get_evaluation().get("value")/100.0
                    return round(result, 2)
                else:
                    copyPosition = copy.deepcopy(position)
                    piece = copyPosition.getWhatIsOnSquare(move[0:2])
                    copyPosition.setPiece(None, move[0:2])
                    copyPosition.setPiece(piece, move[2:4])
                    fen = position.boardToFen(flags)
                    board = chess.Board(fen)
                    if board.is_check():
                        if flags[0] == "w":
                            return -100.0
                        else:
                            return 100.0
                    else:
                        flags[0] = ChessUtils.invert(flags[0])
                        return ChessUtils.evalPosition(position, flags)
            except:
                if flags[0] == "w":
                    return -100.0
                else:
                    return 100.0
            
    def oppose(turn):
            # Input:
            #       A character representing the turn
            # Output:
            #       The opposite turn
        if turn == "w":
            return "b"
        if turn == "b":
            return "w"
        
    def invert(pieceClass):
            # Input:
            #       A character representing a piece from either black or white
            # Output:
            #       The same character but with the colour changed
        if pieceClass.isUpper():
            return pieceClass.lower()
        else:
            return pieceClass.upper()
        
    def moveHint(position, flags):
            # Input:
            #       An object Position and a list of flags
            # Output:
            #       A list of recommended moves to make in certain position
        averageEvalForMoves = []
        if isinstance(position, Position.AbstractPosition):
            return ChessUtils.moveHint(position.position, flags)
        if position.isQuantic():
            bestMoves0 = ChessUtils.moveHint(position.position0, flags)
            bestMoves1 = ChessUtils.moveHint(position.position1, flags)
            for move in bestMoves0:
                average = (ChessUtils.evalNMove(position.position0, flags, move[0]) + ChessUtils.evalNMove(position.position1, flags, move[0])) / 2
                averageEvalForMoves.append(round(average, 2))
            for move in bestMoves1:
                average = (ChessUtils.evalNMove(position.position0, flags, move[0]) + ChessUtils.evalNMove(position.position1, flags, move[0])) / 2
                averageEvalForMoves.append(round(average, 2))
            listAllMoves = bestMoves0 + bestMoves1
            return ChessUtils.optimize(position, flags, averageEvalForMoves, list(list(zip(*listAllMoves))[0]))           # Optimize executes twice the matching moves for quantum move evaluation
        else:
            try:
                fen = position.boardToFen(flags)
                stockfish.set_fen_position(fen)
                listDict = stockfish.get_top_moves(3)
                listMoves = []
                evalMoves = []
                for move in listDict:
                    listMoves.append(move.get("Move"))
                    if move.get("Mate") != None:
                        if flags[0] == "w":
                            evalMoves.append(100.0 / (move.get("Mate")))
                        else:
                            evalMoves.append(-100.0 / (move.get("Mate")))
                    else:
                        evalMoves.append(move.get("Centipawn") / 100)
                return ChessUtils.optimize(position, flags, evalMoves, listMoves)
            except Exception as inst:
                return inst
            
    def optimize(position, flags, averageEvalForMoves, listAllMoves):
            # Input:
            #       An object Position, a list of flags, a list of evaluations of moves and a list of moves
            # Output:
            #       Evaluates possible quantum moves based on good classical moves. Modifies the existing move list to add this new moves
        listAllMoves = list(set(listAllMoves))
        matches = ChessUtils.check_matching_prefix(listAllMoves)
        if len(matches)>0:
            for match in matches:
                if (", " in listAllMoves[match[1]]) or (", " in listAllMoves[match[0]]):
                    pass        # Moves are quantum already
                else:
                    if (listAllMoves[match[0]] + ", " + listAllMoves[match[1]] in listAllMoves) or (listAllMoves[match[1]] + ", " + listAllMoves[match[0]] in listAllMoves):
                        pass        # This quantum moves are already on the list
                    else:    
                        if (ChessUtils.isCaptureStr(position, listAllMoves[match[0]], flags) or ChessUtils.isCaptureStr(position, listAllMoves[match[1]], flags)):
                            pass        # Captures are not elegible quantum moves
                        else:
                            listAllMoves.append(listAllMoves[match[0]] + ", " + listAllMoves[match[1]])
                            evaluated = (ChessUtils.evalNMove(position, flags, listAllMoves[match[0]]) + ChessUtils.evalNMove(position, flags, listAllMoves[match[1]])) / 2
                            averageEvalForMoves.append(round(evaluated, 2))
        if flags[0] == "w":
            lambdaFunction = lambda x: -x[1]
        else:
            lambdaFunction = lambda x: x[1]
        sorted_moves = sorted(zip(listAllMoves, averageEvalForMoves), key=lambdaFunction)
        return sorted_moves
    
    def check_matching_prefix(listMoves):
            # Input:
            #       A list of moves
            # Output:
            #       A list of dictionaries that link every index on the list which share the origin square, meaning they are made by the same piece.
        matches = []
        for i in range(len(listMoves)):
            for j in range(i + 1, len(listMoves)):
                if listMoves[i][:2] == listMoves[j][:2]:
                    matches.append((i,j))
        return matches
    
    def updateFlags(position, move, flagsOrig):
        # Input:
        #       The move we just completed and the piece class of the moved piece
        # Action:
        #       Updates flags, castle, en passent. It also promotes the pawn in case it happens to the demanded piece
        # Output:
        #       None
        flags = copy.deepcopy(flagsOrig)
        if (move.isQuantic()):
            if move.move1.move[3] in "54": # Possible en passent flag, prioritize move that allows en passent to be able to create the flag. The other move creates no flag
                squares = move.move1.move
            else:
                squares = move.move0.move
        else:
            squares = move.move[0:4]
        
        piece = position.getWhatIsOnSquare(squares)
        if piece != None:
            pieceClass = piece.pieceClass
        else:
            print("No piece found to move")
        if pieceClass == "K":
            flags[1].replace("KQ", "")
        if pieceClass == "k":
            flags[1].replace("kq", "")
 
        if squares[0:2] == "a1":
            flags[1].replace("Q", "")
        if squares[0:2] == "h1":
            flags[1].replace("K", "")
        if squares[0:2] == "a8":
            flags[1].replace("q", "")
        if squares[0:2] == "h8":
            flags[1].replace("k", "")
        if pieceClass == "P" and int(squares[1]) - int(squares[3]) == -2:
            flags[2] = squares[0] + str(3)
        elif pieceClass == "p" and int(squares[1]) - int(squares[3]) == 2:
            flags[2] = squares[0] + str(6)
        else:
            flags[2] == "-"

        if pieceClass in "Pp":
            if (pieceClass.islower() and squares[3] == '1') or ((pieceClass.isupper()) and squares[3] == '8'):
                promoted = position.getWhatIsOnSquare(squares[2:4])
                if move.flags[0] == "w":
                    promoted.pieceClass = move.move[4].upper()
                else:
                    promoted.pieceClass = move.move[4].lower()
        flags[0] = ChessUtils.oppose(flags[0])
        return flags