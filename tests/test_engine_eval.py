"""The Stockfish bridge: FEN generation, evaluation, and move ordering.

Phase 1 removed the bare `except:` blocks that were hiding failures in this
layer, so the defects below are now observable. They are pinned here as
`xfail(strict=True)` so Phase 3 gets a pass/fail signal per item.
"""

import pytest

pytestmark = pytest.mark.needs_engine


def broken(item, reason):
    return pytest.mark.xfail(strict=True, reason=f"PLAN.md {item} -- {reason}")


# --------------------------------------------------------------------------
# FEN
# --------------------------------------------------------------------------


@broken("3.1", "fen.rstrip('/') result discarded, leaving a trailing slash")
def test_starting_fen_is_well_formed(game):
    import chess

    fen = game().position.boardToFen(["w", "KQkq", "-", "0", "1"])
    chess.Board(fen)   # raises on a malformed FEN
    assert fen.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR ")


def test_quantic_position_has_no_fen(game):
    g = game()
    g.qMove("b1a3", "b1c3")
    with pytest.raises(Exception):
        g.position.boardToFen(g.flagList)


# --------------------------------------------------------------------------
# Move ordering
# --------------------------------------------------------------------------


@broken("3.2", "optimize() de-dups moves with set() but not the parallel eval list")
def test_optimize_keeps_moves_paired_with_their_evaluations(game):
    """The highest-scored move must still carry its own score afterwards."""
    from utils import ChessUtils

    g = game()
    moves = ["a2a3", "b2b3", "c2c3", "d2d4", "e2e4", "g1f3", "b1c3"]
    evaluations = [0.1, 0.2, 0.3, 9.9, 8.8, 0.5, 0.6]
    expected = dict(zip(moves, evaluations))

    result = ChessUtils.optimize(g.position, g.flagList, list(evaluations), list(moves))

    for move, score in result:
        if move in expected:
            assert score == expected[move], f"{move} lost its evaluation"


@broken("3.2", "set() ordering varies per process, so the ranking is unstable")
def test_move_hint_ranking_is_deterministic(game):
    """The same position must rank the same way every time.

    Run in-process here; the cross-process variant is what PYTHONHASHSEED=0
    pins in CI.
    """
    from utils import ChessUtils

    g = game()
    listMoves = ["c2c4", "d2d4", "e2e4"]
    evaluations = [0.55, 0.40, 0.32]
    expected = dict(zip(listMoves, evaluations))

    for _ in range(5):
        result = ChessUtils.optimize(
            g.position, g.flagList, list(evaluations), list(listMoves)
        )
        assert dict(result) == expected


def test_move_hint_returns_a_list(game):
    hint = game().moveHint()
    assert isinstance(hint, list), f"moveHint returned {type(hint).__name__}"
    assert hint, "no moves suggested for the starting position"
    for move, score in hint:
        assert isinstance(move, str) and isinstance(score, float)


# --------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------


@broken("3.3/3.12", "evalPosition arity + stockfish.is_move_correct no longer exists")
def test_starting_position_evaluates_near_zero(game):
    """The initial position is close to balanced; ±100 is the failure sentinel."""
    assert abs(game().evaluate()) < 1.5


@broken("3.3/3.12", "same: every evalNMove call falls through to the sentinel")
def test_evaluating_a_move_is_not_the_sentinel(game):
    assert abs(game().evaluate("e2e4")) < 1.5


@broken("3.4", "invert() calls isUpper(); the method is isupper()")
def test_invert_flips_piece_colour():
    from utils import ChessUtils

    assert ChessUtils.invert("K") == "k"
    assert ChessUtils.invert("k") == "K"


def test_oppose_flips_the_turn():
    from utils import ChessUtils

    assert ChessUtils.oppose("w") == "b"
    assert ChessUtils.oppose("b") == "w"


# --------------------------------------------------------------------------
# Phase 1 outcome: failures are logged, not swallowed
# --------------------------------------------------------------------------


def test_engine_failures_are_logged(game, caplog):
    """The point of Phase 1: a fallback to the sentinel must leave a trace.

    Delete this test once Phase 3 makes the evaluation path succeed -- at that
    point nothing should be logging warnings here at all.
    """
    import logging

    with caplog.at_level(logging.WARNING, logger="utils"):
        result = game().evaluate()

    if abs(result) >= 100.0:
        assert caplog.records, "sentinel returned with no warning logged"
        assert "falling back to sentinel" in caplog.text
