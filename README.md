<p align="center">
  <img src="qChess_logo.ico" alt="Quantum Chess logo" width="96">
</p>

# Quantum Chess

### A chess variant that lets players embrace some of the principles of Quantum Mechanics.

Quantum Chess is a variant of classical chess adding quantum properties. In the game, pieces can sometimes be in two places at once — quantum superposition. This happens when you make a **quantum move**: two classical moves played at once, after which the precise position of that piece is no longer known.

A piece's position is only defined when an **observation** happens — when someone captures a quantum piece, or when a quantum piece captures another. At that moment there is a 50% chance of it being in each of its two positions.

This also enables **quantum entanglement**. If a quantum piece has some probability of being at one square, there is also a probability that it is *not* there, so a sliding piece may pass through it. In that case the sliding move may or may not have happened — it depends on where the earlier quantum piece finally collapses. The two moves are entangled.

**To win, you must capture the enemy king.** There is no check, no checkmate and no stalemate: because a king may exist in superposition, the game can only be decided by actually removing it from the board.

---

## Project context

This implementation is the software component of the author's final degree
project (*Trabajo de Fin de Grado*). The accompanying thesis —
`TFG Alejandro Martín Auden.pdf`, in Spanish — is the authoritative reference
for the quantum rule set and, in particular, for the **quantum move evaluation
formula** that `ChessUtils.evalMoveFormula` implements. Consult it before
changing any of the evaluation code.

---

## Requirements

| Dependency | Notes |
|---|---|
| Python 3.10+ | `validator.py` uses `match`/`case` (3.10+). Developed and verified on **3.11** |
| [`python-chess`](https://pypi.org/project/chess/) | FEN parsing and check detection |
| [`stockfish`](https://pypi.org/project/stockfish/) | Python wrapper around the Stockfish binary |
| `tkinter` | GUI. Ships with CPython on Windows/macOS; on Debian/Ubuntu install `python3-tk` |
| Stockfish 15 binary | **Not** included — see below |

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install chess stockfish
```

### Installing the Stockfish engine

The engine binary is a ~48 MB native executable and is **not** part of this
repository (see `.gitignore`). Download the build for your platform from
[stockfishchess.org/download](https://stockfishchess.org/download/) and place it at:

```
Stockfish/stockfish_15_x64_avx2.exe
```

That path is currently hard-coded in `utils.py`, relative to the process working
directory — so **run the app from the repository root**. If you are on macOS or
Linux, or you keep the binary elsewhere, update the `Stockfish(path=...)` call
in `utils.py`.

Without the binary the modules fail at import time: the engine is constructed at
module level, not on demand.

---

## Running

**Graphical interface (recommended):**

```bash
python GUI.py
```

Pick *Play against Stockfish* (then choose a colour) or *Play with a friend*.

**Text interface:**

```bash
python loop.py
```

`loop.py` starts a game immediately on import — it is a script, not a module.

---

## How to play

### Move notation

Moves use **UCI notation**: origin square followed by destination square.

| Kind | Example | Meaning |
|---|---|---|
| Classical move | `b5d3` | Move the piece on b5 to d3 |
| Quantum move | `b5d3, b5e2` | Split the piece on b5 across d3 **and** e2 |
| Promotion | `e7e8q` | Promote to queen (`q`, `r`, `b`, `n`) |

Both halves of a quantum move must start from the same square, and **neither
half may be a capture** — a capture is an observation, which is precisely what a
quantum move avoids.

Each player gets a limited budget of quantum moves per game
(`Game.QMovesAllowed`, default **3**). Collapsing a superposition refunds budget.

### In the GUI

- Click a piece, then click its destination.
- For a quantum move: press **Enter Quantum Mode**, then click the piece, then
  each of the **two** destination squares.
- Squares and pieces drawn in **violet** are in superposition.

### Text commands (`loop.py`)

| Command | Effect |
|---|---|
| `Help` | Show command details |
| `Rules` | Show the Quantum Chess rules |
| `Evaluate` | Evaluate the current position. Positive favours white, negative favours black |
| `Evaluate move` | Prompts for a move, then rates it |
| `Hint` | Ask the engine what to play |
| `Over` | End the game |
| `Reset` | Restart the game |

---

## Architecture

### Module map

| Module | Responsibility |
|---|---|
| `Game.py` | Game state: the position, move list, flags, quantum-move budgets, entanglement links, win detection. The top-level API — `move`, `qMove`, `evaluate`, `moveHint` |
| `Position.py` | The board and the **superposition tree** (see below). Applies moves, collapses superpositions, renders the board |
| `Move.py` | `Move` and `QuanticMove`. Validity and capture detection, dispatching across the position tree |
| `Piece.py` | A single piece: its class character, whether it is in superposition, and the move indices it is entangled with |
| `validator.py` | Pure classical chess legality, per piece type. Operates only on plain, non-quantum positions |
| `utils.py` | `ChessUtils`: Stockfish bridge, evaluation, hints, interference detection, flag updates |
| `GUI.py` | Tkinter front-end |
| `loop.py` | Console front-end |
| `reporter.py` | Work in progress: exhaustive legal-move generation. Not wired into the game |

### The superposition tree

The single most important idea in the codebase: **a position is a tree, not a
board.** Three node types, all sharing the `Position` interface, so callers can
treat any node uniformly:

```
Position          leaf  — a concrete 8x8 board (listRows), the only node with real pieces
AbstractPosition  1 child  — one classical move applied; adds a level to the tree
QuanticPosition   2 children — a superposition; position0 and position1 are two
                              parallel worlds that evolve independently
```

Every move adds exactly **one level at the bottom** of the tree, and merging
preserves depth. This yields the invariant the collapse machinery depends on:

> **The tree level of a superposition equals the ordinal of the move that created it.**

That is why `Piece.listMoves` can store plain move numbers and
`Position.mergePosition(index, choice)` can find the right node by descending
`index` levels from the root. If you change how moves build the tree, you must
preserve this invariant, and it should stay covered by a regression test in
`tests/`.

Reading a square via `getWhatIsOnSquare` walks down the tree; on a
`QuanticPosition` it returns whichever branch has a piece there, preferring
`position0`.

### Collapse and entanglement

- A **quantum move** (`Game.qMove`) splits the current leaf into a
  `QuanticPosition` and tags the pieces on both destination squares with the
  ordinal of that move (`Piece.listMoves`).
- A **capture involving a quantum piece** (`Game.move`) is an observation:
  `mergePosition` picks one branch at random (`random.randint(0, 1)`) and
  discards the other, for that superposition and every one entangled with it.
- **Interference** (`ChessUtils.getInterference`) finds pieces sitting between a
  slider's origin and destination. If such a piece is in superposition, the
  slide is entangled with it — the slide happens only in the worlds where that
  square is empty.
- `Game.linked` tracks which squares hold mutually entangled pieces, so
  collapsing one collapses the whole group.
- `Game.deQuantify` runs after every move: a piece that ended up identical in
  both branches is no longer in superposition and is written back as an
  ordinary piece.

### Game flags

`Game.flagList` is the FEN tail as a list — `[turn, castlingRights,
enPassantTarget, halfmoveClock, fullmoveNumber]`, initialised to
`["w", "KQkq", "-", "0", "1"]`. `Position.boardToFen` combines it with the board
to produce the FEN handed to Stockfish. FEN can only be produced for a
non-quantum position; asking a `QuanticPosition` for one raises.

### Engine integration

Stockfish understands classical chess only, so quantum positions are evaluated
by **evaluating each branch of the tree separately and averaging**
(`ChessUtils.evalNMove`, `evalPosition`). Candidate quantum moves are
constructed by `ChessUtils.optimize`, which pairs up strong classical moves that
share an origin square. `ChessUtils.evalMoveFormula` then scores a quantum move
from both halves plus the opponent's best replies to each.

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests live in `tests/`. Two things are worth knowing before adding to them:

**Most tests do not need the Stockfish binary.** `validator.py` imports only
`math`, and `Piece.py` imports nothing, so the classical rule logic can be
exercised anywhere. `tests/conftest.py` provides a `stub_board` fixture — an
engine-free stand-in built from an 8-row ASCII diagram, rank 8 first:

```python
def test_something(stub_board):
    board = stub_board([
        "....k...", "........", "........", "........",
        "........", "........", "........", "....K..R",
    ])
```

Tests that genuinely need the engine take the `real_board` fixture and must be
marked `@pytest.mark.needs_engine`; they skip themselves when the binary is
missing. This matters because `utils.py` constructs Stockfish at *module* level,
so `import Game` fails outright without it — which is the case on a fresh clone
and in CI.

**Set `PYTHONHASHSEED=0` when chasing an ordering bug.** Several code paths
de-duplicate with `set()`, whose iteration order varies per process, so results
can differ between otherwise identical runs. CI pins the seed to 0 so such
failures are reproducible rather than intermittent:

```powershell
$env:PYTHONHASHSEED = "0"; pytest    # PowerShell
```

CI runs the suite on Python 3.10 / 3.11 / 3.12 (`.github/workflows/tests.yml`).

---
