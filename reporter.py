import Position
import Piece

class AllowedMoves:

    def listAllMoves(self, position):
        if isinstance(position, Position.Position):
            for row in position.listRows:
                for square in row:
                    if isinstance(square, Piece.Piece):
                        if square.pieceClass.lower() == "p":
                            self.allMovesPawn(position, square)
                        if square.pieceClass.lower() == "b":
                            self.allMovesBishop(position, square)
                        if square.pieceClass.lower() == "n":
                            self.allMovesKnight(position, square)
                        if square.pieceClass.lower() == "r":
                            self.allMovesRook(position, square)
                        if square.pieceClass.lower() == "q":
                            self.allMovesQueen(position, square)
                        if square.pieceClass.lower() == "k":
                            self.allMovesKing(position, square)
        elif isinstance(position, Position.QuanticPosition):
            listOfMoves0 = self.listAllMoves(position.position0)
            listOfMoves1 = self.listAllMoves(position.position1)
            return list(set(listOfMoves0).union(set(listOfMoves1)))
        elif isinstance(position, Position.AbstractPosition):
            return self.listAllMoves(position.position)
        else:
            pass

    def allMovesPawn(self, position, piece):
        pass

    def allMovesBishop(self, position, piece):
        pass

    def allMovesKnight(self, position, piece):
        pass

    def allMovesRook(self, position, piece):
        pass

    def allMovesQueen(self, position, piece):
        pass

    def allMovesKing(self, position, piece):
        pass