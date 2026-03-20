_This project has been created as part of the 42 curriculum by ipykhtin and khabdall._

# A-Maze-ing

> Generate, display, and explore procedurally created mazes — with a hidden **42** inside.

---

## Description

**A-Maze-ing** is a Python 3 project that:

- Reads a simple `KEY=VALUE` configuration file.
- Generates a maze (perfect or imperfect) using an **iterative depth-first / recursive-backtracker** algorithm.
- Embeds a pixel-art **"42"** glyph of fully enclosed cells near the centre of the maze.
- Writes the maze to a hex-encoded output file along with the shortest path.
- Launches an interactive **terminal renderer** with ANSI colours, path display, and palette cycling.

---

## Instructions

### Requirements

- Python 3.10 or later
- No third-party runtime dependencies (stdlib only)

### Install dev tools

```bash
make install
# or manually:
pip install flake8 mypy build
```

### Run

```bash
python3 a_maze_ing.py config.txt
# or:
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint          # flake8 + mypy standard flags
make lint-strict   # flake8 + mypy --strict
```

### Clean

```bash
make clean
```

### Build the pip package

```bash
make build-pkg
# Produces mazegen-1.0.0-py3-none-any.whl and mazegen-1.0.0.tar.gz
# in the project root.
```

### Install the package from the wheel

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

---

## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are comments.
All keys are case-insensitive.

| Key           | Type           | Required | Description                             | Example                |
| ------------- | -------------- | -------- | --------------------------------------- | ---------------------- |
| `WIDTH`       | integer ≥ 2    | ✔        | Number of cell columns                  | `WIDTH=20`             |
| `HEIGHT`      | integer ≥ 2    | ✔        | Number of cell rows                     | `HEIGHT=15`            |
| `ENTRY`       | `x,y`          | ✔        | Zero-indexed entry coordinates          | `ENTRY=0,0`            |
| `EXIT`        | `x,y`          | ✔        | Zero-indexed exit coordinates           | `EXIT=19,14`           |
| `OUTPUT_FILE` | string         | ✔        | Path to the hex-encoded output file     | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `True`/`False` | ✔        | Perfect maze (unique path) or imperfect | `PERFECT=True`         |
| `SEED`        | integer        | optional | Fixed seed for reproducibility          | `SEED=42`              |

### Default config (`config.txt`)

```ini
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Output file format

```
<hex row 0>
<hex row 1>
...
<hex row HEIGHT-1>
                       ← empty line
<entry_x>,<entry_y>
<exit_x>,<exit_y>
<shortest path: NESW letters>
```

Each cell is one uppercase hex digit (0–F) encoding which walls are **closed** (bit = 1):

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Example: `A` = `1010₂` → East and West walls closed.

---

## Interactive controls

After launch the renderer displays a menu:

```
=== A-Maze-ing ===
  1. Re-generate a new maze
  2. Show/Hide path from entry to exit
  3. Rotate maze wall colours
  4. Quit
```

- **E** (magenta) = entry cell
- **X** (red) = exit cell
- **▓▓▓** (grey) = "42" pattern cells
- **·** (cyan) = shortest-path cells (when path is shown)

---

## Maze generation algorithm

**Recursive Backtracker (iterative DFS)**

1. All walls start closed (every cell value = 0xF).
2. The "42" pattern cells are stamped as fully-enclosed obstacles.
3. Starting from the entry cell, an iterative DFS is run:
   - At each step a random unvisited neighbour (not a pattern cell) is chosen.
   - The shared wall between the current cell and the chosen neighbour is removed.
   - The neighbour is pushed onto the stack.
   - When no unvisited neighbours remain, the algorithm backtracks.
4. Any cells unreachable from the entry (e.g. surrounded by pattern cells) are
   connected by linking them to the nearest visited cell.
5. For **imperfect** mazes, ≈12 % of remaining interior walls are removed
   (skipping any removal that would create a 3×3 open area or break the "42" pattern).
6. All outer-border walls are sealed.
7. All walls adjacent to pattern cells are forced to be consistent.
8. BFS finds the shortest path from entry to exit.

### Why recursive backtracker?

- Produces **long, winding corridors** — visually satisfying and challenging to solve.
- Simple to implement iteratively, avoiding Python's recursion limit for large mazes.
- Guaranteed to produce a **spanning tree** (perfect maze) with no isolated regions.
- Easily extended to imperfect mazes by adding extra passages after carving.
- Well-known, well-studied, and efficient: O(W × H) time and space.

---

## Reusable module (`mazegen`)

The entire maze-generation logic lives in `mazegen/__init__.py` and is packaged as a
standalone pip-installable wheel (`mazegen-*.whl`).

### Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    perfect=True,
    seed=42,
)
gen.generate()

# Hex-encoded rows (for file output)
for y in range(gen.height):
    print(gen.get_hex_row(y))

# Shortest path as direction letters
print("".join(gen.solution))   # e.g. "SSEENNEESSE..."

# Raw grid (list[list[int]], each value 0-15)
grid = gen.grid
cell_value = grid[0][0]        # top-left cell

# "42" pattern cells
for cx, cy in gen.pattern_cells:
    print(f"Pattern cell at ({cx}, {cy})")

# Was the pattern embedded?
if gen.pattern_placed:
    print("42 pattern embedded successfully.")
```

### Custom parameters

```python
gen = MazeGenerator(
    width=50,
    height=40,
    entry=(0, 0),
    exit_=(49, 39),
    perfect=False,   # imperfect: extra passages allowed
    seed=None,       # None → different maze every run
)
```

### Accessing the structure

```python
from mazegen import NORTH, EAST, SOUTH, WEST

cell = gen.grid[y][x]
has_north_wall = bool(cell & NORTH)   # True if North wall is closed
has_east_wall  = bool(cell & EAST)
```

---

## Team and project management

### Roles

| Team member | Responsibilities                                                |
| ----------- | --------------------------------------------------------------- |
| \<login1\>  | Maze generation algorithm, BFS path-finding, pip package setup  |
| \<login2\>  | Terminal renderer, interactive loop, ANSI colour system         |
| \<login3\>  | Config parser & validator, output file writer, Makefile, README |

### Planning

**Week 1** — Requirements analysis, algorithm selection, project scaffolding.  
**Week 2** — Core maze generator (`MazeGenerator` class), "42" pattern, output format.  
**Week 3** — Terminal renderer, interactive menu, colour palettes, edge-case handling.  
**Week 4** — Lint / mypy clean-up, pip package, README, peer reviews and fixes.

The timeline mostly held; the "42" pattern placement and the 3×3 open-area check
took longer than anticipated because of the need to keep pattern cells coherent with
their neighbours.

### What worked well

- Switching from recursive to iterative DFS early avoided stack-overflow issues.
- Separating the generator (`mazegen/`) from the CLI (`a_maze_ing.py`) made unit
  testing straightforward.
- Type hints + mypy caught several off-by-one errors before runtime.

### What could be improved

- The 3×3 open-area check in imperfect mode rescans the whole grid on each removed
  wall; a localised check would be faster for very large mazes.
- A graphical MLX renderer would look better than the terminal ASCII version.
- Multiple algorithm choices (Kruskal, Prim) would be a good bonus.

### Tools used

- **Python 3.10** — main language
- **flake8** — style linting
- **mypy** — static type checking
- **build** / **setuptools** — pip package construction
- **Git** — version control
- **Claude (Anthropic)** — used to brainstorm the project structure, generate
  boilerplate docstrings, and cross-check the hex encoding against the spec.
  All generated code was reviewed, tested, and understood before inclusion.

---

## Resources

- [Maze generation — Jamis Buck's excellent blog series](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Recursive backtracker explanation](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Wikipedia: Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Python `random` module docs](https://docs.python.org/3/library/random.html)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### AI usage

Claude (Anthropic) assisted with:

- Drafting docstrings and README sections.
- Reviewing the hex bit-encoding logic against the spec.
- Suggesting the BFS parent-tracking approach for memory-efficient path reconstruction.
- Reviewing flake8/mypy compliance of the code.

All AI-generated suggestions were manually reviewed, tested, and understood before
inclusion in the project. No code was blindly copy-pasted.
