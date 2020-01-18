import numpy as np


def create_empty_grid(N, window_size):
    border_id = window_size//2 - 1
    grid = np.zeros((N + 2*border_id, N + 2*border_id), dtype=np.int32)

    # Filling borders:
    grid[border_id:-border_id, border_id] = -2
    grid[border_id, border_id:-border_id] = -2
    grid[border_id:-border_id, - (border_id + 1)] = -2
    grid[- (border_id + 1), border_id:-border_id] = -2

    # Filling outside the borders:
    grid[:, :border_id] = -1
    grid[:, -border_id:] = -1
    grid[:border_id, :] = -1
    grid[-border_id:, :] = -1
    return grid

N = 400
window_size = 9
grid = create_empty_grid(N, window_size)
