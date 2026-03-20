import random
from typing import List, Optional, Set, Tuple

from .Constants import Direction


class Maze:

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ):
        if width < 2 or height < 2:
            raise ValueError("Maze dimensions must be at least 2×2.")
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(f"Entry {entry} is outside the maze bounds.")
        if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
            raise ValueError(f"Exit {exit_} is outside the maze bounds.")
        if entry == exit_:
            raise ValueError("Entry and exit must be different cells.")
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit_: Tuple[int, int] = exit_
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed
        self.WEST = Direction.WEST

        self.rand_num_gen: random.Random = random.Random(seed)

        self.grid: List[List[int]] = [
            [Direction.NORTH | Direction.EAST | Direction.SOUTH | self.WEST]
            * width
            for _ in range(height)
        ]

        self.pattern_cells: Set[Tuple[int, int]] = set()
        self.solution: List[str] = []
        self.pattern_placed: bool = False
