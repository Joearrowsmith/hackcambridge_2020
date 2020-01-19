
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

def get_state(team_name, player_idx):
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

def send_action_to_server(team_name, player_idx, action):

    ## sends action to server
    pass


def get_action(action_idx):
    action = np.zeros(shape=(10))
    action[action_idx] = 1
    return action

def get_action_idx(action):
    return np.argmax(action)

def game_loop_send_actions(teams):
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            ## request intention of moves from agents
            action = p_env.act(p_env.state)
            p_env.action = action
            ## send move to send:
            send_action_to_server(team_name, player_idx, action)


def game_loop_update_state(teams):
    game_over = True
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            ## get new game state
            state, dead, game_over = get_state(team_name, player_idx)
            p_env.state = state
            ## calculate score
            output = p_env.step(p_env.action, state, dead, game_over)
            old_state = state
            state, action, reward, done = output
            p_env.model.remember(old_state, action, reward, state, done)
            if not done:
                game_over = False
    return game_over

def run_game(batch_size, num_teams = 3, num_players = 2, death_gamma=0.9999):
    game_over = False

    model = DRQNAgent(batch_size)
    teams = gen_teams(num_teams, num_players, death_gamma, model)    

    ## get initial game state
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            state, dead, game_over = get_state(team_name, player_idx)
            p_env.state = state

    while not game_over:
        game_loop_send_actions(teams)
        game_over = game_loop_update_state(teams)
    assert not game_loop_update_state(teams)    
        

    
    ## do one training loop

    ## or return list sampled states experienced from each agent.
        

run_game(4)