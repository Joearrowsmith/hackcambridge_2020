import numpy as np
import matplotlib.pyplot as plt


def create_empty_grid(N, window_size):
    border_id = window_size//2 - 1
    grid = - np.ones((N + 2*border_id, N + 2*border_id), dtype=np.int32)

    # Filling borders:
    grid[border_id:-border_id, border_id] = -2
    grid[border_id, border_id:-border_id] = -2
    grid[border_id:-border_id, - (border_id + 1)] = -2
    grid[- (border_id + 1), border_id:-border_id] = -2
    return grid


def plot_random_paths(N, window_size, grid, n_walks):
    border_id = window_size//2 - 1
    map_inner = grid[border_id+1:-border_id-1, border_id+1:-border_id-1].copy()
    sub_coords1 = (N//2) * np.ones((n_walks), dtype=np.int32)
    sub_coords2 = (N//2 + 1) * np.ones((n_walks), dtype=np.int32)
    coords1 = np.array([sub_coords1, sub_coords1]).T
    coords2 = np.array([sub_coords2, sub_coords2]).T
    coords3 = np.array([sub_coords1, sub_coords2]).T
    coords4 = np.array([sub_coords2, sub_coords1]).T
    possible_moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    # Getting initial positions:
    grid[coords1[:, 0], coords1[:, 1]] = np.zeros(n_walks, dtype=np.int32)
    grid[coords2[:, 0], coords2[:, 1]] = np.zeros(n_walks, dtype=np.int32)
    grid[coords3[:, 0], coords3[:, 1]] = np.zeros(n_walks, dtype=np.int32)
    grid[coords4[:, 0], coords4[:, 1]] = np.zeros(n_walks, dtype=np.int32)
    while True:
        moves_choices = np.random.randint(0, high=4, size=n_walks, dtype=np.int32)
        moves_turn = np.array([possible_moves[i] for i in moves_choices])
        coords1 += moves_turn
        coords2 += moves_turn
        coords3 += moves_turn
        coords4 += moves_turn
        neg_bool = ((coords1 < 0).sum() + (coords2 < 0).sum()
                    + (coords3 < 0).sum() + (coords4 < 0).sum())
        over_bool = ((coords1 >= N-2).sum() + (coords2 >= N-2).sum()
                    + (coords3 >= N-2).sum() + (coords4 >= N-2).sum())
        if neg_bool or over_bool:
            break
        map_inner[coords1[:, 0], coords1[:, 1]] = np.zeros(n_walks, dtype=np.int32)
        map_inner[coords2[:, 0], coords2[:, 1]] = np.zeros(n_walks, dtype=np.int32)
        map_inner[coords3[:, 0], coords3[:, 1]] = np.zeros(n_walks, dtype=np.int32)
        map_inner[coords4[:, 0], coords4[:, 1]] = np.zeros(n_walks, dtype=np.int32)
    grid[border_id+1:-border_id-1, border_id+1:-border_id-1] = map_inner.copy()
    return grid


def generate_random_map(size=100, window_size=9):
    grid = create_empty_grid(size, window_size)
    map = plot_random_paths(size, window_size, grid, 10)
    return map


if __name__ == "__main__":
    map = generate_random_map()
    figure = plt.figure(figsize=(10, 10))
    plt.pcolor(map, cmap='gray')
    plt.show()
