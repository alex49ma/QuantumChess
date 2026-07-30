"""Lifecycle of `Game.flagList` -- turn, castling rights, en passant target.

`flagList` is the FEN tail: [turn, castlingRights, enPassantTarget, halfmove,
fullmove]. It feeds `boardToFen`, so a stale flag silently corrupts every engine
call made afterwards.
"""

import pytest

pytestmark = pytest.mark.needs_engine


def broken(item, reason):
    return pytest.mark.xfail(strict=True, reason=f"PLAN.md {item} -- {reason}")


# --------------------------------------------------------------------------
# Turn
# --------------------------------------------------------------------------


def test_turn_alternates(game):
    g = game()
    assert g.flagList[0] == "w"
    g.move("e2e4")
    assert g.flagList[0] == "b"
    g.move("e7e5")
    assert g.flagList[0] == "w"


def test_a_refused_move_does_not_consume_the_turn(game):
    g = game()
    assert g.move("e2e5") is False
    assert g.flagList[0] == "w"


# --------------------------------------------------------------------------
# En passant target
# --------------------------------------------------------------------------


def test_double_push_sets_the_en_passant_target(game):
    g = game()
    g.move("e2e4")
    assert g.flagList[2] == "e3"


def test_black_double_push_sets_the_en_passant_target(game):
    g = game()
    g.move("e2e4")
    g.move("e7e5")
    assert g.flagList[2] == "e6"


@broken("2.5", "`flags[2] == '-'` is a comparison, not an assignment")
def test_en_passant_target_is_cleared_by_a_quiet_move(game):
    """The target square must survive exactly one ply."""
    g = game()
    g.move("e2e4")
    g.move("e7e5")
    g.move("g1f3")
    assert g.flagList[2] == "-"


@broken("2.5", "the stale target makes isCapture report a capture on an empty square")
def test_expired_en_passant_window_does_not_fake_a_capture(game):
    """An en passant chance lasts one ply. After it lapses, d6 is just empty.

    The window genuinely opens here (black double-pushes past the white e5
    pawn), white declines it, and the target is then never cleared -- so the
    phantom capture stays available for the rest of the game.
    """
    import Move

    g = game(
        ["....k...", "...p....", "........", "....P...",
         "........", "........", ".......P", "....K..."],
        flags=["b", "KQkq", "-", "0", "1"],
    )
    g.move("d7d5")          # opens the window: flags[2] == "d6"
    assert g.flagList[2] == "d6"

    g.move("h2h3")          # white declines; the window has now lapsed

    assert Move.Move("e5d6", g.flagList).isCapture(g.position) is False


# --------------------------------------------------------------------------
# Castling rights
# --------------------------------------------------------------------------


def test_castling_rights_start_complete(game):
    assert game().flagList[1] == "KQkq"


@broken("2.6", "str.replace() result discarded -- strings are immutable")
def test_king_move_revokes_both_white_rights(game):
    g = game()
    g.move("e2e4")
    g.move("e7e5")
    g.move("e1e2")
    assert "K" not in g.flagList[1] and "Q" not in g.flagList[1]
    assert "k" in g.flagList[1] and "q" in g.flagList[1]


@broken("2.6", "str.replace() result discarded -- strings are immutable")
def test_rook_move_revokes_only_that_side(game):
    g = game(
        ["....k...", "........", "........", "........",
         "........", "........", "........", "R...K..R"]
    )
    g.move("h1h5")
    assert "K" not in g.flagList[1]
    assert "Q" in g.flagList[1]


# --------------------------------------------------------------------------
# Flag aliasing
# --------------------------------------------------------------------------


@broken("4.2", "Move stores the caller's list by reference instead of copying")
def test_move_snapshots_the_flags_it_was_created_with(game):
    """A recorded move must remember the position it was played in.

    Today every Move shares one live list, so history rewrites itself: move 1
    reports whatever the flags happen to be now.
    """
    g = game()
    g.move("e2e4")
    firstMove = g.moveList[0]
    assert firstMove.flags is not g.flagList
    assert firstMove.flags[0] == "w"

    g.move("e7e5")
    assert firstMove.flags[0] == "w", "history changed under us"
