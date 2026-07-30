"""Golden boards: fixed move sequences, asserted square by square.

These drive the real `Game`, so they need the Stockfish binary (importing
`utils` constructs it at module level) and are marked `needs_engine`.

As in `test_validator_rules.py`, the expected boards are **correct chess**.
Anything broken today is `xfail(strict=True)` against its PLAN.md item.
"""

import pytest

pytestmark = pytest.mark.needs_engine


def broken(item, reason):
    return pytest.mark.xfail(strict=True, reason=f"PLAN.md {item} -- {reason}")


CASTLING_SETUP = [
    "....k...",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "R...K..R",
]


def test_opening_sequence(game, render):
    g = game()
    assert g.move("e2e4") is True
    assert g.move("e7e5") is True
    assert g.move("g1f3") is True

    assert render(g.position) == [
        "rnbqkbnr",
        "pppp.ppp",
        "........",
        "....p...",
        "....P...",
        ".....N..",
        "PPPP.PPP",
        "RNBQKB.R",
    ]


def test_capture_removes_the_captured_piece(game, render):
    g = game()
    g.move("e2e4")
    g.move("d7d5")
    assert g.move("e4d5") is True

    assert render(g.position)[3] == "...P...."   # rank 5
    assert render(g.position)[4] == "........"   # rank 4, the pawn left


def test_queenside_castling_places_king_and_rook(game, render):
    g = game(CASTLING_SETUP)
    assert g.move("e1c1") is True
    assert render(g.position)[7] == "..KR...R"


def test_kingside_castling_places_king_and_rook(game, render):
    g = game(CASTLING_SETUP)
    assert g.move("e1g1") is True
    assert render(g.position)[7] == "R....RK."


@broken("2.2", "complementaryMove reads listRows[..][0] instead of [7] for O-O")
def test_kingside_castling_moves_the_h1_rook_not_the_a1_rook(game):
    """The board *looks* right after O-O, but f1 holds the a1 rook object.

    The h1 rook is discarded and a1/f1 end up aliasing one `Piece`, so making
    one of them superposed silently makes the other superposed too.
    """
    g = game(CASTLING_SETUP)
    a1RookBefore = g.position.getWhatIsOnSquare("a1")
    h1RookBefore = g.position.getWhatIsOnSquare("h1")

    g.move("e1g1")

    assert g.position.getWhatIsOnSquare("f1") is h1RookBefore
    assert g.position.getWhatIsOnSquare("a1") is a1RookBefore
    assert g.position.getWhatIsOnSquare("f1") is not g.position.getWhatIsOnSquare("a1")


def test_promotion_to_queen(game, render):
    g = game(
        ["........", "P......k", "........", "........",
         "........", "........", "........", "....K..."]
    )
    assert g.move("a7a8q") is True
    assert render(g.position)[0] == "Q......."


@broken("2.4", "en passant is unreachable in the validator, so the move is refused")
def test_white_en_passant_capture(game, render):
    g = game(
        ["rnbqkbnr", "ppp.pppp", "........", "...pP...",
         "........", "........", "PPPP.PPP", "RNBQKBNR"],
        flags=["w", "KQkq", "d6", "0", "1"],
    )
    assert g.move("e5d6") is True
    rows = render(g.position)
    assert rows[2] == "...P...."   # rank 6: the capturing pawn
    assert rows[3] == "........"   # rank 5: both pawns gone


@broken("2.4", "en passant is unreachable in the validator, so the move is refused")
def test_black_en_passant_capture(game, render):
    g = game(
        ["rnbqkbnr", "pppp.ppp", "........", "........",
         "....pP..", "........", "PPPPP.PP", "RNBQKBNR"],
        flags=["b", "KQkq", "f3", "0", "1"],
    )
    assert g.move("e4f3") is True
    rows = render(g.position)
    assert rows[5] == ".....p.."   # rank 3: the capturing pawn
    assert rows[4] == "........"   # rank 4: both pawns gone


def test_invalid_move_is_refused_and_leaves_the_board_untouched(game, render):
    g = game()
    before = render(g.position)
    assert g.move("e2e5") is False
    assert render(g.position) == before


def test_moving_out_of_turn_is_refused(game, render):
    g = game()
    before = render(g.position)
    assert g.move("e7e5") is False
    assert render(g.position) == before
