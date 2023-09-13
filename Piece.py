class Piece:
    def __init__(self, pieceClass):
        self.pieceClass = pieceClass
        self.quantic = False
        self.listMoves = []

    def setQuantic(self, quantic):
        # Input:
        #       A boolean to set if we want the piece to be quantum or not
        # Output:
        #       The move itself
        self.quantic = quantic
        if not quantic:
            self.listMoves.clear()
        return self
        
    def addMoves(self, moves = []):
        # Input:
        #       Moves we want to add to the merging indexes of this piece
        # Output:
        #       The list of indexes after being updated
        union = list(set(moves) | set(self.listMoves))
        self.listMoves = union
        return self.listMoves

    def isQuantic(self):
        # Input:
        #       None
        # Output:
        #       If the piece is quantum
        return self.quantic
