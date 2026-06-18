# src/utils/grid_parsers.py
from typing import Any, List, Tuple

import numpy as np


class ARCGrid:
    def __init__(self, raw_frame_list: List[Any]) -> None:
        """
        Rigid 2D Grid Engine. Robustly handles both raw 2D list matrix
        structures and 3D environment channel tensors.
        """
        # Convert to numpy array immediately for spatial processing
        self.matrix = np.array(raw_frame_list, dtype=np.int8)

        # If the environment passes a 3D array (e.g., shape 1xHxW),
        # slice the first layer out to isolate the 2D grid matrix canvas.
        if self.matrix.ndim == 3:
            self.matrix = self.matrix[0]

        # Explicitly unpack the remaining 2D spatial dimensions
        self.height, self.width = self.matrix.shape

    @property
    def unique_colors(self) -> List[int]:
        """Returns all color values present in the current frame (excluding background 0)."""
        colors = np.unique(self.matrix)
        return [int(c) for c in colors if c != 0]

    def find_objects(self) -> List[Tuple[int, int, int, int]]:
        """
        Stub for connected-component bounding box extraction.
        Returns a list of boxes: (min_row, min_col, max_row, max_col)
        """
        return []
