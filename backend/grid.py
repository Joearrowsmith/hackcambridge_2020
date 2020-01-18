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
    map_game = plot_random_paths(size, window_size, grid, 10)
    return map_game


def create_players(map_game_master, n_teams, n_players_per_team):
    assert n_teams < 5, "Error: Code cannot handle this amount of teams. Get a better developer!"
    assert n_teams > 1, "Error: Number of teams needs to be larger than 1!"
    map_game = map_game_master.copy()

    # Divide board into n_teams equal pieces:
    N = map_game.shape[0]

    # Define all the x and y coordinates
    y_coords = np.tile(np.arange(N), N).reshape(N, N)
    x_coords = y_coords.copy().T

    if n_teams == 2:
        teams_dict = {1: [], 2: []}
        # Divide grid in to two:
        x_coords1 = np.arange(N//2+1)
        x_coords2 = np.arange(N//2+1, N)

        i1 = n_players_per_team
        i2 = n_players_per_team

        while i1 > 0:
            id1 = (np.random.choice(x_coords1), np.random.choice(np.arange(N)))
            if (map_game[id1] == 0) and (map_game[id1] != 1):
                map_game[id1] = 1
                i1 -= 1
                teams_dict[1].append(id1)

        while i2 > 0:
            id2 = (np.random.choice(x_coords2), np.random.choice(np.arange(N)))
            if (map_game[id2] == 0) and (map_game[id2] != 1):
                map_game[id2] = 1
                i2 -= 1
                teams_dict[2].append(id2)

    elif n_teams == 3:
        teams_dict = {1: [], 2: [], 3: []}
        # Divide grid in to two:
        x_coords1 = np.arange(N//2+1)
        x_coords2 = np.arange(N//2+1, N)
        y_coords1 = np.arange(N//2+1)
        y_coords2 = np.arange(N//2+1, N)

        i1 = n_players_per_team
        i2 = n_players_per_team
        i3 = n_players_per_team

        while i1 > 0:
            id1 = (np.random.choice(x_coords1), np.random.choice(y_coords1))
            if (map_game[id1] == 0) and (map_game[id1] != 1):
                map_game[id1] = 1
                i1 -= 1
                teams_dict[1].append(id1)

        while i2 > 0:
            id2 = (np.random.choice(x_coords1), np.random.choice(y_coords2))
            if (map_game[id2] == 0) and (map_game[id2] != 1):
                map_game[id2] = 1
                i2 -= 1
                teams_dict[2].append(id2)

        while i3 > 0:
            id3 = (np.random.choice(x_coords2), np.random.choice(np.arange(N)))
            if (map_game[id3] == 0) and (map_game[id3] != 1):
                map_game[id3] = 1
                i3 -= 1
                teams_dict[3].append(id3)

    elif n_teams == 4:
        teams_dict = {1: [], 2: [], 3: [], 4: []}
        # Divide grid in to two:
        x_coords1 = np.arange(N//2+1)
        x_coords2 = np.arange(N//2+1, N)
        y_coords1 = np.arange(N//2+1)
        y_coords2 = np.arange(N//2+1, N)

        i1 = n_players_per_team
        i2 = n_players_per_team
        i3 = n_players_per_team
        i4 = n_players_per_team

        while i1 > 0:
            id1 = (np.random.choice(x_coords1), np.random.choice(y_coords1))
            if (map_game[id1] == 0) and (map_game[id1] != 1):
                map_game[id1] = 1
                i1 -= 1
                teams_dict[1].append(id1)

        while i2 > 0:
            id2 = (np.random.choice(x_coords2), np.random.choice(y_coords1))
            if (map_game[id2] == 0) and (map_game[id2] != 1):
                map_game[id2] = 1
                i2 -= 1
                teams_dict[2].append(id2)

        while i3 > 0:
            id3 = (np.random.choice(x_coords1), np.random.choice(y_coords2))
            if (map_game[id3] == 0) and (map_game[id3] != 1):
                map_game[id3] = 1
                i3 -= 1
                teams_dict[3].append(id3)

        while i4 > 0:
            id4 = (np.random.choice(x_coords2), np.random.choice(y_coords2))
            if (map_game[id4] == 0) and (map_game[id4] != 1):
                map_game[id4] = 1
                i4 -= 1
                teams_dict[4].append(id4)
    return teams_dict


def map_shrink(map_game):
    N = map_game.shape[0]
    boundary_index = np.where(map_game == -2)[0][0]
    boundary_index

    b1 = boundary_index + 1
    b2 = - (b1 + 1)

    map_game[b1, b1:-b1] = -2  # TOP
    map_game[b1:-b1, b1] = -2  # LEFT
    map_game[b1:-b1, b2] = -2  # LEFT
    map_game[b2, b1:-b1] = -2  # BOTTOM

    map_game[b1-1, :] = -1  # TOP
    map_game[:, b1-1] = -1  # LEFT
    map_game[:, b2+1] = -1  # LEFT
    map_game[b2+1, :] = -1  # BOTTOM
    return map_game



if __name__ == "__main__":
    map_game = generate_random_map(size=100)
    figure = plt.figure(figsize=(10, 10))
    plt.imshow(map_game, cmap='gray')
    plt.show()

    for i in range(10):
        map_game = map_shrink(map_game)
        figure = plt.figure(figsize=(10, 10))
        plt.imshow(map_game, cmap='gray')
        plt.show()
