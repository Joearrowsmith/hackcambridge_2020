import numpy as np
import sklearn.preprocessing
import warnings
warnings.filterwarnings("ignore")

def encode_grid_onehot(grid, num_categories=7):
    """Encodes Grid using One Hot convention."""
    window_size = grid.shape[0]
    distinct_categories = np.tile(np.arange(7), window_size).reshape(window_size, num_categories)
    enc = sklearn.preprocessing.OneHotEncoder(
                categories=distinct_categories,
                sparse=False,
                dtype=np.int32)
    dense_shape = (window_size, window_size, num_categories)
    grid_encoded = enc.fit_transform(grid+2).reshape(dense_shape)
    return grid_encoded


def main():
    # TEST CASE 1:
    # Void 1st upper layer
    # Boundary 2nd upper layer
    # Random players scattered about
    window_size = 9
    center_index = window_size//2
    GRID = np.zeros((window_size, window_size), dtype=np.int32)
    GRID[0] = -1
    GRID[1] = -2

    GRID[7, 7] = 1
    GRID[7, 8] = 2
    GRID[3, 1] = 3
    GRID[5, 1] = 4
    grid_encoded = encode_grid_onehot(GRID)
    return


if __name__ == "__main__":
    main()
