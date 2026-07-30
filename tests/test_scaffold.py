"""Scaffolding checks: proves the harness itself works.

This file exists to verify that the test setup is sound -- imports resolve, the
engine-free stub board behaves, and the `needs_engine` skip works. It asserts
only behaviour that is already correct.

The real suites (board golden files, classical rules, the superposition-tree
invariant) are the next phase of the remediation plan. Add them as
``tests/test_<area>.py`` alongside this file.
"""

import pytest

import Piece
from validator import validator


def test_repo_root_is_importable():
    """sys.path wiring in conftest works for engine-free modules."""
    assert Piece.Piece("K").pieceClass == "K"
    assert callable(validator.isValid)


def test_stub_board_reads_the_starting_array(stub_start):
    assert stub_start.getWhatIsOnSquare("e1").pieceClass == "K"
    assert stub_start.getWhatIsOnSquare("e8").pieceClass == "k"
    assert stub_start.getWhatIsOnSquare("a1").pieceClass == "R"
    assert stub_start.getWhatIsOnSquare("h8").pieceClass == "r"
    assert stub_start.getWhatIsOnSquare("d4") is None


def test_stub_board_accepts_a_custom_diagram(stub_board):
    board = stub_board(
        [
            "....k...",
            "........",
            "........",
            "........",
            "........",
            "........",
            "........",
            "....K..R",
        ]
    )
    assert board.getWhatIsOnSquare("e1").pieceClass == "K"
    assert board.getWhatIsOnSquare("h1").pieceClass == "R"
    assert board.getWhatIsOnSquare("a1") is None


def test_piece_superposition_round_trip():
    piece = Piece.Piece("N")
    assert piece.isQuantic() is False

    piece.setQuantic(True)
    piece.addMoves([3])
    assert piece.isQuantic() is True
    assert piece.listMoves == [3]

    # Collapsing a piece clears the entanglement indices it carried.
    piece.setQuantic(False)
    assert piece.isQuantic() is False
    assert piece.listMoves == []


def test_knight_moves_engine_free(stub_start):
    """A rule that is correct today, checked without the engine."""
    assert validator.knightMoveValid(stub_start, "g1f3") is True
    assert validator.knightMoveValid(stub_start, "g1g3") is not True


@pytest.mark.needs_engine
def test_engine_marker_and_real_position(real_board):
    """Skipped automatically when the Stockfish binary is absent."""
    position = real_board()
    assert position.getWhatIsOnSquare("e1").pieceClass == "K"
    assert position.isQuantic() is False
