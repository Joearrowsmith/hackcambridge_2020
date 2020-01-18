import backend.grid
import Models.grid_functions



MAP = backend.grid.generate_random_map()
MAP_onehot = Models.grid_functions.encode_grid_onehot(MAP)
