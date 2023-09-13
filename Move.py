import Position
from utils import ChessUtils

class Move:

    def __init__(self, move, flags):
        self.move = move
        self.flags = flags

    def isQuantic(self):
        # Input:
        #       None
        # Output:
        #       If the move is quantum
        return False
            
    def isValid(self, position):
        # Input:
        #       Position in which the move must be done
        # Output:
        #       If the move is valid
        if isinstance(position, Position.AbstractPosition):
            return self.isValid(position.position)
        
        piece = position.getWhatIsOnSquare(self.move[:2]) 
        otherPiece = position.getWhatIsOnSquare(self.move[2:])
        if piece is not None:
            if piece.pieceClass in "Kk" and int(abs(ord(self.move[0]) - ord(self.move[2]))) > 1:
                movement = ord(self.move[0]) - ord(self.move[2])
                if int(movement) < 0:
                    if position.getWhatIsOnSquare("f" + self.move[1]) is not None:
                        return False
                if int(movement) > 0:
                    if position.getWhatIsOnSquare("b" + self.move[1]) is not None and position.getWhatIsOnSquare("d" + self.move[1]) is not None:
                        return False
            if otherPiece is not None:
                if piece.pieceClass.islower() == otherPiece.pieceClass.islower():
                    return False

        if position.isQuantic():
            isValid0 = self.isValid(position.position0)
            isValid1 = self.isValid(position.position1)
            return isValid0 or isValid1
        else:
            return ChessUtils.isValid(position, self)

    def isCapture(self, position):
        # Input:
        #       Position in which the move must be done
        # Output:
        #       If the move is a capture
        if isinstance(position, Position.AbstractPosition):
            return self.isCapture(position.position)
        if position.isQuantic():
            try:
                return self.isCapture(position.position0) or self.isCapture(position.position1)
            except:
                return False
        else:
            return ChessUtils.isCapture(position, self)
            
class QuanticMove(Move):
    
    def __init__(self, move0, move1):
        self.move0 = move0
        self.move1 = move1

    def isQuantic(self):
        # Input:
        #       None
        # Output:
        #       If the move is quantum
        return True
    
    def isValid(self, position):
        # Input:
        #       Position in which the move must be done
        # Output:
        #       If the move is valid
        piece = position.getWhatIsOnSquare(self.move0.move[:2]) 
        pieceCap0 = position.getWhatIsOnSquare(self.move0.move[2:]) 
        pieceCap1 = position.getWhatIsOnSquare(self.move1.move[2:])
        if piece is not None:
            if pieceCap0 is not None:
                if piece.pieceClass.islower() == pieceCap0.pieceClass.islower():
                    return False
            if pieceCap1 is not None:
                if piece.pieceClass.islower() == pieceCap1.pieceClass.islower():
                    return False
        if self.move0.isCapture(position):
            return False
        if self.move1.isCapture(position):
            return False
        if self.move0.move[0:2] != self.move1.move[0:2]:
            return False
        return self.move0.isValid(position) and self.move1.isValid(position)
    
    def isCapture(self, position):
        # Input:
        #       Position in which the move must be done
        # Output:
        #       If the move is a capture
        return self.move0.isCapture(position) or self.move1.isCapture(position)
