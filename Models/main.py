
## state : agent recieves 7x7 grid of the world in one hot representation and the message from a given location.
## reward : if agent dies recieves -3. If near by player dies recieve -1. If agent recieves a 
"""
end rewards:
    - survive + 10
    - team win + 20
    - second place + 10
    - third place + 0
    - forth and below place - 10

intermediate rewards:
- explore reward ratios:
    - selfish bot: 
        - self die: -3, team die: -1
    - helpful bot:
        - self die: -1, team die: -3
        - friend being attacked: -1
    - neutral bot:
        - self die: -2, team die: -2
- aggressive bot: 
    - successful attack: +1
- scared bot: 
    - being attacked: -1
"""

def get_map():
    state =[]
    size = 9
    for i in range(size):
        state.append([-1]*size)
    return state
    
from gym import Env

class MultiAgentEnv(gym.Env):

if __name__=="__main__":


