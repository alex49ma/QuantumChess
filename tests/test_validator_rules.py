"""Classical chess legality, as implemented by `validator.py`.

Engine-free: `validator` imports only `math`, so everything here runs in CI.

These tests assert **correct chess**, not current behaviour. Rules that are
broken today are marked `xfail(strict=True)` and cite their PLAN.md item. Strict
mode means a fix turns the xfail into an *unexpected pass*, which pytest reports
as a failure --so the suite tells you exactly when a defect is repaired and
which marker to delete. Never "fix" one of these by weakening the assertion.
"""

import pytest

from validator import validator

STARTING = [
    "rnbqkbnr",
    "pppppppp",
    "........",
    "........",
    "........",
    "........",
    "PPPPPPPP",
    "RNBQKBNR",
]

WHITE = ["w", "KQkq", "-"]
BLACK = ["b", "KQkq", "-"]


def broken(item, reason):
    return pytest.mark.xfail(strict=True, reason=f"PLAN.md {item} --{reason}")


# --------------------------------------------------------------------------
# King
# --------------------------------------------------------------------------

KING_OPEN = [
    "....k...",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "...QK..R",
]


def test_king_moves_one_square_forward(stub_board):
    assert validator.kingMoveValid(stub_board(KING_OPEN), "e1e2", WHITE) is True


@broken("2.1", "`&` precedence reduces the test to abs(fileDelta) <= (rankDelta & 1)")
def test_king_moves_one_square_sideways(stub_board):
    """A king must be able to step sideways. Today this is rejected."""
    assert validator.kingMoveValid(stub_board(KING_OPEN), "e1f1", WHITE) is True


@broken("2.1", "same precedence bug lets the king slide any distance vertically")
def test_king_cannot_cross_the_whole_board(stub_board):
    assert validator.kingMoveValid(stub_board(STARTING), "e1e8", WHITE) is not True


# --------------------------------------------------------------------------
# Rook
# --------------------------------------------------------------------------


def test_rook_blocked_vertically(stub_board):
    """a1-a3 is blocked by the pawn on a2. The vertical scan is correct today."""
    assert validator.rookMoveValid(stub_board(STARTING), "a1a3") is False


def test_rook_moves_along_a_clear_file(stub_board):
    board = stub_board(
        ["....k...", "........", "........", "........",
         "........", "........", "........", "R...K..."]
    )
    assert validator.rookMoveValid(board, "a1a7") is True


@broken("2.3", "the horizontal scan omits copysign and walks off the board")
def test_rook_blocked_horizontally_leftwards(stub_board):
    """h1-a1 is blocked by the king on e1. Today this raises IndexError."""
    assert validator.rookMoveValid(stub_board(STARTING), "h1a1") is False


# --------------------------------------------------------------------------
# Knight, bishop, queen --correct today; these are regression guards
# --------------------------------------------------------------------------


def test_knight_jumps_over_pieces(stub_board):
    assert validator.knightMoveValid(stub_board(STARTING), "g1f3") is True


def test_knight_rejects_a_non_knight_shape(stub_board):
    assert validator.knightMoveValid(stub_board(STARTING), "g1g3") is not True


def test_bishop_blocked_by_own_pawn(stub_board):
    assert validator.bishMoveValid(stub_board(STARTING), "c1e3") is False


def test_queen_blocked_by_own_pawn(stub_board):
    assert validator.queenMoveValid(stub_board(STARTING), "d1d3") is False


def test_queen_rejects_a_non_line_move(stub_board):
    assert validator.queenMoveValid(stub_board(STARTING), "d1f4") is False


# --------------------------------------------------------------------------
# Pawn
# --------------------------------------------------------------------------


def test_pawn_single_step(stub_board):
    assert validator.pawnMoveValid(stub_board(STARTING), "e2e3", WHITE) is True


def test_pawn_double_step_from_the_starting_rank(stub_board):
    assert validator.pawnMoveValid(stub_board(STARTING), "e2e4", WHITE) is True


def test_pawn_cannot_step_onto_an_occupied_square(stub_board):
    board = stub_board(
        ["....k...", "........", "........", "........",
         "........", "....n...", "....P...", "....K..."]
    )
    assert validator.pawnMoveValid(board, "e2e3", WHITE) is False


@broken("2.7", "the double push never checks the pawn is on its starting rank")
def test_pawn_cannot_double_step_from_a_later_rank(stub_board):
    board = stub_board(
        ["....k...", "........", "........", "........",
         "........", "....P...", "........", "....K..."]
    )
    assert validator.pawnMoveValid(board, "e3e5", WHITE) is False


@broken("2.8", "the rank 1/8 guard is defeated by `|` precedence")
def test_pawn_cannot_exist_on_the_last_rank(stub_board):
    board = stub_board(
        ["....p...", "........", "........", "........",
         "........", "........", "........", "....K..k"]
    )
    assert validator.pawnMoveValid(board, "e8e7", BLACK) is False


EN_PASSANT = [
    "rnbqkbnr",
    "ppp.pppp",
    "........",
    "...pP...",
    "........",
    "........",
    "PPPP.PPP",
    "RNBQKBNR",
]


@broken("2.4", "`if move[2:4] != None` is always true, so the en passant branch is dead")
def test_en_passant_capture_is_legal(stub_board):
    board = stub_board(EN_PASSANT)
    assert validator.pawnMoveValid(board, "e5d6", ["w", "KQkq", "d6"]) is True


def test_pawn_cannot_capture_an_empty_square_without_an_en_passant_target(stub_board):
    board = stub_board(EN_PASSANT)
    assert validator.pawnMoveValid(board, "e5f6", ["w", "KQkq", "-"]) is False


PROMOTION = [
    ".n......",
    "P......k",
    "........",
    "........",
    "........",
    "........",
    "........",
    "....K...",
]


def test_promotion_to_queen_on_a_quiet_move(stub_board):
    board = stub_board(
        ["........", "P......k", "........", "........",
         "........", "........", "........", "....K..."]
    )
    assert validator.pawnMoveValid(board, "a7a8q", WHITE) is True


@broken("2.9", "the capture branch checks 'qrbk' --knight missing")
def test_promotion_to_knight_on_a_capture(stub_board):
    assert validator.pawnMoveValid(stub_board(PROMOTION), "a7b8n", WHITE) is True


@broken("2.9", "the capture branch checks 'qrbk' --king wrongly accepted")
def test_cannot_promote_to_king_on_a_capture(stub_board):
    assert validator.pawnMoveValid(stub_board(PROMOTION), "a7b8k", WHITE) is False


# --------------------------------------------------------------------------
# Shared entry point
# --------------------------------------------------------------------------


class FakeMove:
    """`validator.isValid` only reads `.move` and `.flags`."""

    def __init__(self, move, flags):
        self.move = move
        self.flags = flags


def test_isValid_rejects_a_null_move(stub_board):
    assert validator.isValid(stub_board(STARTING), FakeMove("e2e2", WHITE)) is False


def test_isValid_rejects_a_truncated_move(stub_board):
    assert validator.isValid(stub_board(STARTING), FakeMove("e2", WHITE)) is False


def test_isValid_rejects_moving_the_opponents_piece(stub_board):
    assert validator.isValid(stub_board(STARTING), FakeMove("e7e5", WHITE)) is False


def test_isValid_rejects_capturing_your_own_piece(stub_board):
    assert validator.isValid(stub_board(STARTING), FakeMove("a1a2", WHITE)) is False


def test_isValid_accepts_a_normal_opening_move(stub_board):
    assert validator.isValid(stub_board(STARTING), FakeMove("e2e4", WHITE)) is True
