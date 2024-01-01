import math

class validator:

    @classmethod
    def isValid(self, position, move):
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
                    return self.kingMoveValid(position, move.move, flags)
                case "q" | "Q":
                    return self.queenMoveValid(position, move.move)
                case "r" | "R":
                    return self.rookMoveValid(position, move.move)
                case "b" | "B":
                    return self.bishMoveValid(position, move.move)
                case "n" | "N":
                    return self.knightMoveValid(position, move.move)
                case "p" | "P":
                    return self.pawnMoveValid(position, move.move, flags)
                
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