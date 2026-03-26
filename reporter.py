import Game
import Position
import Piece

class AllowedMoves:

    def listAllMoves(self, game):
        if isinstance(game, Game):
            for row in range(len(game.position.listRows)):
                for col in range(len(game.position.listRows[row])):
                    piece = game.position.listRows[row][col]
                    if isinstance(piece, Piece.Piece):
                        if piece.pieceClass.lower() == "p":
                            self.allMovesPawn(game.position, piece, row, col, game.flagList)
                        if piece.pieceClass.lower() == "b":
                            self.allMovesBishop(game.position, piece, row, col)
                        if piece.pieceClass.lower() == "n":
                            self.allMovesKnight(game.position, piece, row, col)
                        if piece.pieceClass.lower() == "r":
                            self.allMovesRook(game.position, piece, row, col)
                        if piece.pieceClass.lower() == "q":
                            self.allMovesQueen(game.position, piece, row, col)
                        if piece.pieceClass.lower() == "k":
                            self.allMovesKing(game.position, piece, row, col, game.flagList)
        elif isinstance(game.position, Position.QuanticPosition):
            listOfMoves0 = self.listAllMoves(game.position.position0)
            listOfMoves1 = self.listAllMoves(game.position.position1)
            return list(set(listOfMoves0).union(set(listOfMoves1)))
        elif isinstance(game.position, Position.AbstractPosition):
            return self.listAllMoves(game.position.position)
        else:
            pass

    def allMovesPawn(self, position, piece, row, col, flags):
        res = []
        if(piece.pieceClass.isupper()):
            # Case move one step
            if not position.listRows[row - 1][col]:
                res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col) + str(7 - row))
                # Case move two steps in case you can move one step
                if not position.listRows[row - 2][col] and row == 6:
                    res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col) + str(6 - row))
                # Case try capture, first en passant
            squareUpLeft = chr(ord('a') + col - 1) + str(7 - row)
            squareUpRight = chr(ord('a') + col + 1) + str(7 - row)
            try:
                pieceUpLeft = position.getWhatIsOnSquare(squareUpLeft)
            except Exception as exc:
                print(type(exc))
                print("Out of boundaries on the left side of the board")
            try:
                pieceUpRight = position.getWhatIsOnSquare(squareUpRight)
            except Exception as exc:
                print(type(exc))
                print("Out of boundaries on the right side of the board")
                if flags[2] == squareUpLeft:
                    res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col - 1) + str(7 - row))
                if flags[2] == squareUpRight:
                    res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col + 1) + str(7 - row))
                # Case normal captures
                if isinstance(pieceUpLeft, Piece.Piece):
                    if pieceUpLeft.pieceClass.islower:
                        res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col - 1) + str(7 - row))
                if isinstance(pieceUpRight, Piece.Piece):
                    if pieceUpRight.pieceClass.islower:
                        res.append(chr(ord('a') + col) + str(8 - row) + chr(ord('a') + col - 1) + str(7 - row))

        else:
            pass
            # TODO Moves by black pawns

    def allMovesBishop(self, position, piece, row, col):
        if(piece.pieceClass.isupper()):
            pass
        else:
            pass

    def allMovesKnight(self, position, piece, row, col):
        if(piece.pieceClass.isupper()):
            pass
        else:
            pass

    def allMovesRook(self, position, piece, row, col):
        if(piece.pieceClass.isupper()):
            pass
        else:
            pass

    def allMovesQueen(self, position, piece, row, col):
        if(piece.pieceClass.isupper()):
            pass
        else:
            pass

    def allMovesKing(self, position, piece, row, col):
        if(piece.pieceClass.isupper()):
            pass
        else:
            pass