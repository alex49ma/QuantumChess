"""Shared pytest configuration for the Quantum Chess test suite.

Three things happen here:

1. The game modules (``Game``, ``Position``, ``validator``, ...) live at the
   repository root rather than inside an installed package, so the root is put
   on ``sys.path``.

2. Tests that need the real Stockfish executable are skipped when it is not
   installed. The binary is ~48 MB and deliberately not tracked in git, so it
   is absent on a fresh clone and in CI.

   Importing ``utils`` -- and therefore ``Game``, ``Position`` and ``Move`` --
   constructs the engine at *module* level, so those imports fail outright
   without the binary. ``validator`` and ``Piece`` have no such dependency
   (``validator`` imports only ``math``), which is why the classical rule tests
   can run everywhere.

3. A dependency-free board stub is provided so the ``validator`` rules can be
   exercised without the engine. It implements the one method the validators
   actually call, ``getWhatIsOnSquare``.
"""

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import Piece  # noqa: E402  -- must follow the sys.path setup above

STARTING_ROWS = [
    "rnbqkbnr",
    "pppppppp",
    "........",
    "........",
    "........",
    "........",
    "PPPPPPPP",
    "RNBQKBNR",
]


def _engine_path() -> Path:
    """Where the Stockfish binary is expected, honouring STOCKFISH_PATH."""
    override = os.environ.get("STOCKFISH_PATH")
    if override:
        return Path(override)
    return REPO_ROOT / "Stockfish" / "stockfish_15_x64_avx2.exe"


ENGINE_PATH = _engine_path()
ENGINE_AVAILABLE = ENGINE_PATH.is_file()


def pytest_collection_modifyitems(config, items):
    """Skip `needs_engine` tests when the Stockfish binary is missing."""
    if ENGINE_AVAILABLE:
        return
    skip = pytest.mark.skip(reason=f"Stockfish binary not found at {ENGINE_PATH}")
    for item in items:
        if "needs_engine" in item.keywords:
            item.add_marker(skip)


class StubBoard:
    """Minimal stand-in for ``Position`` with no Stockfish dependency.

    Built from an 8-row ASCII diagram, rank 8 first, '.' for an empty square::

        StubBoard(["....k...", "........", ..., "....K..R"])

    Deliberately mirrors ``Position.getWhatIsOnSquare`` exactly -- including its
    lack of bounds checking -- so a test that walks off the board fails here the
    same way it would in the real thing.
    """

    def __init__(self, rows: list[str]):
        assert len(rows) == 8 and all(len(r) == 8 for r in rows), "need an 8x8 diagram"
        self.listRows = [
            [Piece.Piece(square) if square != "." else None for square in row]
            for row in rows
        ]

    def getWhatIsOnSquare(self, square: str):
        file = ord(square[0]) - ord("a")
        rank = len(self.listRows) - int(square[1])
        return self.listRows[rank][file]

    def isQuantic(self) -> bool:
        return False


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def stub_board():
    """Factory for an engine-free board. See :class:`StubBoard`."""
    return StubBoard


@pytest.fixture
def stub_start():
    """The standard starting array as an engine-free board."""
    return StubBoard(STARTING_ROWS)


@pytest.fixture
def real_board():
    """Factory for a genuine ``Position``. Requires the engine.

    Use with ``@pytest.mark.needs_engine``.
    """
    import Game
    import Position

    def make(rows: list[str] = STARTING_ROWS):
        assert len(rows) == 8 and all(len(r) == 8 for r in rows), "need an 8x8 diagram"
        return Position.Position(Game.Game().setInitPieces(rows))

    return make
