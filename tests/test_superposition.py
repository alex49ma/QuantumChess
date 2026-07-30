"""Superposition, collapse, and the tree-depth invariant.

The invariant these tests exist to protect (PLAN.md 1.3):

    The tree level of a superposition equals the ordinal of the move that
    created it.

`Piece.listMoves` stores plain move numbers, and `mergePosition(index, choice)`
locates a superposition by descending `index` levels from the root. Those two
only agree because every move adds exactly one level *at the bottom* of the tree
and merging preserves depth. Nothing in the code enforces it, so it is asserted
here: if a change to how moves build the tree breaks it, collapse starts picking
the wrong superposition and no other test would notice.
"""

import copy

import pytest

pytestmark = pytest.mark.needs_engine


def broken(item, reason):
    return pytest.mark.xfail(strict=True, reason=f"PLAN.md {item} -- {reason}")


# --------------------------------------------------------------------------
# Creating a superposition
# --------------------------------------------------------------------------


def test_quantum_move_puts_one_piece_on_two_squares(game, quantics):
    g = game()
    assert g.qMove("b1a3", "b1c3") is True

    assert quantics(g.position) == [("a3", "N", (0,)), ("c3", "N", (0,))]
    assert g.position.getWhatIsOnSquare("b1") is None
    assert g.position.isQuantic() is True


def test_quantum_move_consumes_the_budget(game):
    g = game()
    assert g.QMovesWhite == 0
    g.qMove("b1a3", "b1c3")
    assert g.QMovesWhite == 1
    assert g.QMovesBlack == 0
    assert g.flagList[0] == "b"


def test_quantum_budget_is_capped(game):
    g = game()
    g.QMovesWhite = g.QMovesAllowed
    assert g.qMove("b1a3", "b1c3") is False


def test_quantum_move_must_start_from_one_square(game):
    g = game()
    assert g.qMove("b1a3", "g1f3") is False


def test_quantum_move_may_not_capture(game):
    g = game(
        ["....k...", "........", "........", "........",
         "........", "..p.p...", "........", "...NK..."]
    )
    # Both halves land on a black pawn (c3 / e3); a capture is an observation.
    assert g.qMove("d1c3", "d1e3") is False


def test_quantum_move_may_not_capture_with_either_half(game):
    g = game(
        ["....k...", "........", "........", "........",
         "........", "..p.....", "........", "...NK..."]
    )
    # Only the c3 half is a capture -- that is still enough to refuse it.
    assert g.qMove("d1c3", "d1e3") is False


def test_tree_depth_grows_by_one_per_move(game):
    g = game()
    assert g.position.depth() == 1
    g.move("e2e4")
    assert g.position.depth() == 2
    g.move("e7e5")
    assert g.position.depth() == 3
    g.qMove("b1a3", "b1c3")
    assert g.position.depth() == 4


# --------------------------------------------------------------------------
# The invariant (PLAN.md 1.3)
# --------------------------------------------------------------------------


@pytest.fixture
def twoSuperpositions(game):
    """Two independent superpositions, created at move ordinals 0 and 2."""
    g = game()
    g.qMove("b1a3", "b1c3")   # ordinal 0 -> knight on a3 / c3
    g.move("d7d5")            # ordinal 1
    g.qMove("g1f3", "g1h3")   # ordinal 2 -> knight on f3 / h3
    g.move("d5d4")            # ordinal 3
    return g


def test_superpositions_are_tagged_with_their_move_ordinal(twoSuperpositions, quantics):
    assert quantics(twoSuperpositions.position) == [
        ("a3", "N", (0,)),
        ("c3", "N", (0,)),
        ("f3", "N", (2,)),
        ("h3", "N", (2,)),
    ]


@pytest.mark.parametrize(
    "ordinal, collapsed, untouched",
    [
        (0, {"a3", "c3"}, {"f3", "h3"}),
        (2, {"f3", "h3"}, {"a3", "c3"}),
    ],
)
def test_merge_collapses_the_superposition_with_that_ordinal(
    twoSuperpositions, quantics, ordinal, collapsed, untouched
):
    """THE invariant. `mergePosition(n)` must collapse the superposition
    created by move `n`, and leave every other one alone."""
    g = copy.deepcopy(twoSuperpositions)
    g.position = g.position.mergePosition(ordinal, 0)
    remaining = {square for square, _, _ in quantics(g.position)}

    assert len(remaining & collapsed) == 1, "exactly one branch must survive"
    assert untouched <= remaining, "the other superposition must be untouched"


def test_merge_preserves_tree_depth(twoSuperpositions):
    """Depth preservation is what keeps level == ordinal true after a collapse."""
    before = twoSuperpositions.position.depth()
    twoSuperpositions.position = twoSuperpositions.position.mergePosition(0, 0)
    assert twoSuperpositions.position.depth() == before


def test_merge_choice_selects_the_branch(twoSuperpositions, quantics):
    """choice 0 and choice 1 must not collapse to the same square."""
    left = copy.deepcopy(twoSuperpositions)
    right = copy.deepcopy(twoSuperpositions)
    left.position = left.position.mergePosition(0, 0)
    right.position = right.position.mergePosition(0, 1)

    leftSquares = {sq for sq, _, _ in quantics(left.position)} & {"a3", "c3"}
    rightSquares = {sq for sq, _, _ in quantics(right.position)} & {"a3", "c3"}
    assert leftSquares != rightSquares


# --------------------------------------------------------------------------
# Collapse hygiene
# --------------------------------------------------------------------------


@broken("4.6", "mergePosition(0) keeps a live reference to the surviving branch")
def test_merge_does_not_alias_the_surviving_branch(twoSuperpositions):
    g = twoSuperpositions
    survivor = g.position.mergePosition(0, 0)
    assert survivor.position is not g.position.position0
    assert survivor.position is not g.position.position1


@broken("4.5", "QuanticPosition.setPiece writes one Piece object into both branches")
def test_collapsed_pieces_are_not_shared_between_branches(game):
    g = game()
    g.qMove("b1a3", "b1c3")
    g.move("d7d5")

    quantic = g.position
    left = quantic.position0.getWhatIsOnSquare("e1")
    right = quantic.position1.getWhatIsOnSquare("e1")
    assert left is not right, "both worlds share one king object"
