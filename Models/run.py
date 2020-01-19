
from pomdp_env import MultiAgentEnv
from agent_no_text import DRQNAgent
import numpy as np

def gen_teams(num_teams, num_players, death_gamma, model):
    teams = {}
    for t in range(num_teams):
        team = []
        for p in range(num_players):
            agent_env = MultiAgentEnv(death_gamma, model)
            team.append(agent_env)
        teams[f'ai_team_{t}'] = team
    return teams


def get_state(team_name, player_idx, action):
    """
    obs_state: [9x9 np.array, 4x20 character message array]
    dead: bool if this agent is dead
    game_over: None unless game over then, team ranking
    """
    big = np.genfromtxt("map_1010_filled.txt", delimiter=" ", dtype=np.int32)
    fov_9by9 = big[-9:,-9:]    ## need to get this from server
    messages = ['','','','']   ## need to get this from server

    dead, game_over = False, None     ## need to get this from server

    return [fov_9by9, messages], dead, game_over


def get_action(action_idx):
    action = np.zeros(shape=(10))
    action[action_idx] = 1
    return action


def get_action_idx(action):
    return np.argmax(action)


def run_game(batch_size, num_teams = 3, num_players = 2, death_gamma=0.9999):
    game_over = False

    model = DRQNAgent(batch_size)
    teams = gen_teams(num_teams, num_players, death_gamma, model)

    no_action = get_action(0)
    ## get initial game state
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            state, dead, game_over = get_state(team_name, player_idx, no_action)
            p_env.state = state

    while not game_over:

        for team_name in teams:
            for player_idx, p_env in enumerate(teams[team_name]):
                ## request intention of moves from agents
                action = p_env.act(p_env.state)
                p_env.action = action

                ## send move to send:



        ## execute the moves (send to server) and calculate the score and get new game state

        # save the game state from training

        ## check if game is over
        break

    ## do one training loop

    ## or return list sampled states experienced from each agent.


run_game(4)
