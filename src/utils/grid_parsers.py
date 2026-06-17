# src/utils/grid_parsers.py
from typing import List, Tuple

import numpy as np


class ARCGrid:
    def __init__(self, raw_frame_list: List[List[int]]):
        # Convert to numpy array immediately for faster spatial slicing
        self.matrix = np.array(raw_frame_list, dtype=np.int8)
        self.height, self.width = self.matrix.shape

    @property
    def unique_colors(self) -> List[int]:
        """Returns all colors present in the current frame (excluding background 0)."""
        colors = np.unique(self.matrix)
        return [int(c) for c in colors if c != 0]

    def find_objects(self) -> List[Tuple[int, int, int, int]]:
        """
        Stub for connected-component or bounding-box extraction.
        Returns a list of bounding boxes: (min_row, min_col, max_row, max_col)
        """
        # TODO: Jules / Antigravity can implement real flood-fill or clustering here later
        return []
