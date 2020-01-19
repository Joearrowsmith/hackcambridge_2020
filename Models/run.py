
from pomdp_env import MultiAgentEnv
from agent_no_text import DRQNAgent

def gen_teams(num_teams, num_players, death_gamma, model):
    teams = {}
    for t in range(num_teams):
        team = []
        for p in range(num_players)
            agent_env = MultiAgentEnv(death_gamma, model)
            team.append(agent_env)
        teams[f'ai_team_{t}'] = team

def get_state(team_name, player_idx):
    fov_9by9 = ## need to get this from server
    messages = ['','','','']
    return [fov_9by9, messages]

def run_game(num_teams = 3, num_players = 2):
    game_over = False

    model = DQNAgent()
    teams = gen_teams(num_teams, num_players, model)    

    ## get initial game state

    


    while not game_over:

        ## send game state and request intention of moves from agents

        ## execute the moves (send to server) and calculate the score and get new game state

        # save the game state from training

        ## check if game is over
        pass
    ## do one training loop

    ## or return list sampled states experienced from each agent.
        

