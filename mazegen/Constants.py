from enum import IntEnum
from typing import Dict, List, Tuple, Optional

# ---------------------------------------------------------------------------
# Direction constants using Enum for clarity
# ---------------------------------------------------------------------------


class Direction(IntEnum):
    NORTH = 1  # bit 0
    EAST = 2  # bit 1
    SOUTH = 4  # bit 2
    WEST = 8  # bit 3


# Opposite directions lookup
OPPOSITE: Dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

# Movement deltas for each direction (dx, dy)
DELTA: Dict[Direction, Tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
}

# Short letter representation for directions
LETTER: Dict[Direction, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W",
}

# ---------------------------------------------------------------------------
# Pixel-art maze patterns (1 = wall, 0 = passage)
# ---------------------------------------------------------------------------

P4: List[List[int]] = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

P2: List[List[int]] = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

# Dimensions for patterns
PAT_H: int = 5  # rows in each glyph
PAT_W: int = 7  # 3 cols + 1 gap + 3 cols
MIN_W: int = PAT_W + 6  # minimum maze width to embed pattern
MIN_H: int = PAT_H + 6  # minimum maze height to embed pattern

Parent = Optional[Tuple[Tuple[int, int], str]]
