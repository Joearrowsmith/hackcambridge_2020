
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

def get_map(fov_size=9):
    map = np.zeros(fov_size, fov_size)
    map -= 1
    return map
    
from gym import Env

class MultiAgentEnv(gym.Env):
    def __init__(self, bot_type):
        self.bot_type = bot_type
        self.fov = (9,9)

        self.action_space = spaces.Discrete(11)
        self.observation_space = spaces.Box(low=-2, high=4, shape=self.fov, dtype=np.int32)
        
        self.obs_state = None

        self.death_step_num = None

        self.steps_beyond_done = None
        self.reward = 0
        self.tick = 0

    def calculate_reward(self, die=False, team_die=False, 
                         game_over=None, bot_type=None):
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
        
        if game_over != None:
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
                    current_reward += 2
                else:
                    current_reward -= 0
            if survived:
                current_reward += 5        
        return current_reward

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        prev_ob_state = self.obs_state

        self.obs_state, dead, game_over = get_next_obs_state(action)
        ## need to apply a decayed game reward for depending on how long the game lasts after they die

        if self.death_step_num is None:
            if dead:
                self.death_step_num = tick
            
        else:

        done = ## detect dead, check matched with server dead
        done =  x < -self.x_threshold \
                or x > self.x_threshold \
                or theta < -self.theta_threshold_radians \
                or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0
        
        self.tick += 1
        return np.array(self.obs_state), reward, done, {}






if __name__=="__main__":
    print(get_map())

    agent_env = MultiAgentEnv(None)
    print(agent_env.action_space.sample())

