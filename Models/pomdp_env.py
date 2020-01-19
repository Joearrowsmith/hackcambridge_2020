
## state : agent recieves 7x7 grid of the world in one hot representation and the message from a given location.
## reward : if agent dies recieves -3. If near by player dies recieve -1. If agent recieves a 
"""
end rewards:
    - survive + 5
    - team win + 10
    - second place + 5
    - third place + 0
    - forth and below place - 5

intermediate rewards:
- explore reward ratios:
    - selfish bot: 
        - self die: -3, team die: -1
    - helpful bot:
        - self die: -1, team die: -3
        - friend being attacked: -1
    - neutral bot:
        - self die: -2, team die: -2
## Implement below if enough time
- aggressive bot: 
    - successful attack: +1
- scared bot: 
    - being attacked: -1
"""
  
import gym
import numpy as np
from collections import deque
import sklearn.preprocessing

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

class MultiAgentEnv(gym.Env):
    def __init__(self, death_gamma, model, histlen=100, lstm_time_input=26, bot_type=None):
        self.model = model
        self.bot_type = bot_type
        self.fov = (9,9)
        self.action_space = gym.spaces.Discrete(10)
        self.observation_space = gym.spaces.Box(low=-2, high=4, shape=self.fov, dtype=np.int32)
        ##char_max = 4  
        ##self.observation_text = gym.spaces.Box(low=0, high=char_max, shape=8, dtype=np.int32)
        self.history = deque(maxlen=histlen)
        self.time_history = deque(maxlen=lstm_time_input)
        self.death_gamma = death_gamma
        self.death = None # {obs_state, reward, step_number}
        self.step_num = 0

        self.state = None
        self.action = None

    def add_to_history(self, state, action, reward, next_state, done):
        ## convert state to onehot
        one_hot_next_state = encode_grid_onehot(next_state[0])
        time_state = list(self.time_history)
        self.time_history.append([one_hot_next_state])#, next_state[1]])
        next_time_state = list(self.time_history)
        if len(self.time_history) == self.time_history.maxlen: 
            self.history.append((time_state[:-1], action, reward, next_time_state[1:], done))

    def calculate_reward(self, die=False, team_die=False, 
                         bot_type=None):
        current_reward = 0
        if bot_type == "selfish":
            if die:
                current_reward -= 3
            if team_die:
                current_reward -= 1
        elif bot_type == "helpful":
            if die:
                current_reward -= 1
            if team_die:
                current_reward -= 3
        elif bot_type == "neutral":
            if die:
                current_reward -= 2
            if team_die:
                current_reward -= 2
        return current_reward

    def get_team_reward(self, game_over):
        current_reward = 0
        assert type(game_over) is dict
        position = game_over['team_position']
        survived = game_over['survived']
        assert position > 0
        if position == 1:
            current_reward += 10
        else:
            assert survived == False, "not possible for losing team to have a playing left"
            if position == 2:
                current_reward += 5
            elif position == 3:
                current_reward += 0
            else:
                current_reward -= 5
        if survived:
            current_reward += 5 
        assert current_reward <= 15
        return current_reward  

    def act(self, state):
        return self.model.act(state)

    def step(self, action, obs_state, dead, game_over):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        output = None
        reward = None
        if self.death:
            ## player known to be dead, dont append till game over
            output = None
        else:
            reward = self.calculate_reward(dead, False)
            if dead:
                ## player detected dead, dont append till game over
                self.death['step_num'] = self.step_num
                self.death['obs_state'] = obs_state
                self.death['reward'] = reward
                self.death['action'] = action
                output = None
            else:
                ## not dead
                output = obs_state, action, reward, False

        if output is None:
            assert dead, "for a non output player must be dead"

        if game_over:
            ## need to get final reward from team
            team_reward = self.get_team_reward(game_over=game_over)
            if self.death:
                final_reward = (self.death['reward'] + team_reward * self.death_gamma**(self.step_num - self.death['step_num'])) ## this will reduce the reward, a longer time results in less reward.
            else:
                final_reward = team_reward
            return self.death['obs_state'], self.death['action'], final_reward, True
        self.step_num += 1
        return output


if __name__=="__main__":
    agent_env = MultiAgentEnv(None)
    print(agent_env.action_space.sample())

