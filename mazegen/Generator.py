import os
from typing import List, Set, Tuple, Optional, Dict
from collections import deque
from .Constants import (DELTA, MIN_H, MIN_W, OPPOSITE, P2, P4, PAT_H, PAT_W,
                        Direction, Parent, LETTER)
from .Maze import Maze
import time


class MazeGenerator(Maze):
    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit_: Tuple[int, int], perfect: bool = True,
                 seed: Optional[int] = None,
                 animation: Optional[bool] = False) -> None:
        super().__init__(width, height, entry, exit_, perfect, seed)
        self.animation = animation
        self.WEST = Direction.WEST

    def generate(self) -> None:
        self._place_pattern()
        self._carve_passage()
        self.solution = self._bfs_shortes_path()

    def get_hex_row(self, y: int) -> str:
        return "".join(format(self.grid[y][x], "X") for x in range(self.width))

    def _place_pattern(self) -> None:
        if self.width < MIN_W or self.height < MIN_H:
            self.pattern_placed = False
            return

        px: int = max(2, (self.width - PAT_W) // 2)
        py: int = max(2, (self.height - PAT_H) // 2)

        cells: Set[Tuple[int, int]] = set()

        for row in range(PAT_H):
            for col in range(3):
                if P4[row][col]:
                    cells.add((px + col, py + row))

            for col in range(3):
                if P2[row][col]:
                    cells.add((px + 4 + col, py + row))

        cells.discard(self.entry)
        cells.discard(self.exit_)
        self.pattern_cells = cells
        for cx, cy in self.pattern_cells:
            self.grid[cy][cx] = (
                Direction.NORTH | Direction.EAST | Direction.SOUTH | self.WEST
            )
        self.pattern_placed = True

    def _clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _carve_passage(self) -> None:

        blocked: Set[Tuple[int, int]] = set(self.pattern_cells)
        visited: Set[Tuple[int, int]] = set(blocked)

        def _dfs(sx: int, sy: int) -> None:
            stack: List[Tuple[int, int]] = [(sx, sy)]
            visited.add((sx, sy))
            while stack:
                x, y = stack[-1]
                dirs = [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]
                self.rand_num_gen.shuffle(dirs)
                advanced = False
                for d in dirs:
                    dx, dy = DELTA[d]
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in visited
                    ):
                        self.grid[y][x] &= ~d
                        self.grid[ny][nx] &= ~OPPOSITE[d]

                        if self.animation:
                            from .Renderer import render_maze
                            self._clear()
                            render_maze(self, True, 0)  # it must be updated
                            time.sleep(0.1)

                        visited.add((nx, ny))
                        stack.append((nx, ny))
                        advanced = True
                        break
                if not advanced:
                    stack.pop()

        _dfs(*self.entry)
        for cy in range(self.height):
            for cx in range(self.width):
                if (cx, cy) in visited:
                    continue

                for d in [
                    Direction.NORTH,
                    Direction.SOUTH,
                    Direction.EAST,
                    Direction.WEST,
                ]:
                    dx, dy = DELTA[d]
                    nx, ny = cx + dx, cy + dy
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) in visited
                        and (nx, ny) not in blocked
                    ):
                        self.grid[cy][cx] &= ~d
                        self.grid[cy][cx] &= ~OPPOSITE[d]
                        _dfs(cx, cy)
                        break

    def _bfs_shortes_path(self) -> List[str]:

        parent: Dict[Tuple[int, int], Parent] = {self.entry: None}
        queue: deque[Tuple[int, int]] = deque([self.entry])

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit_:

                path: List[str] = []
                current: Tuple[int, int] = (x, y)

                while parent[current] is not None:
                    prev_cell, letter = parent[current]  # type: ignore[misc]
                    path.append(letter)
                    current = prev_cell
                path.reverse()
                return path

            for d, (dx, dy) in DELTA.items():
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in parent
                    and not (self.grid[y][x] & d)
                ):
                    parent[(nx, ny)] = ((x, y), LETTER[d])
                    queue.append((nx, ny))

        return []
