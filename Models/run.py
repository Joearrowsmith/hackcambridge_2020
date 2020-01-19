
from pomdp_env import MultiAgentEnv
from agent_no_text import DRQNAgent
import numpy as np
import itertools
from collections import deque

import sklearn.preprocessing
import warnings
import json

import asyncio
import websockets

sockets = {}
main_state = ''

warnings.filterwarnings("once")

def gen_teams(num_teams, num_players, death_gamma, model):

    teams = {}
    for t in range(num_teams):
        team = []
        for p in range(num_players):
            agent_env = MultiAgentEnv(death_gamma, model)
            team.append(agent_env)
        teams[f'ai_team_{t}'] = team
    return teams


async def get_state(team_name, player_idx):
    """
    obs_state: [9x9 np.array, 4x20 character message array]
    dead: bool if this agent is dead
    game_over: None unless game over then, team ranking
    
    reply = {"grid" : ,
            "messages" : ["","","",""],
            "dead" : not game.players["player_id"].alive,
            "over" : game.winner,
                        }
    """

    big = np.genfromtxt("map_1010_filled.txt", delimiter=" ", dtype=np.int32)
    fov_9by9 = big[-9:,-9:]    ## need to get this from server
    messages = ['','','','']   ## need to get this from server

    dead, game_over = False, None ## need to get this from server

    #return [main_state['grid'], main_state['messages']], main_state['dead'], main_state['over']
    return [fov_9by9, messages], dead, game_over

async def send_action_to_server(team_name, player_idx, action):
    d = {0: "move_up", 1: "move_down", 2: "move_left", 3: "move_right", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
    action_idx = get_action_idx(action)
    print(action_idx)
    data = json.dumps({"type": "AI", "playerid": player_idx, "team_name": team_name, "action": d[action_idx]})
    await sockets[player_idx].send(data)


def get_action(action_idx):
    action = np.zeros(shape=(10))
    action[action_idx] = 1
    return action


def get_action_idx(action):
    return np.argmax(action)


async def game_loop_send_actions(teams):
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            ## request intention of moves from agents
            action = p_env.act(p_env.state)
            p_env.action = action
            ## send move to send:
            await send_action_to_server(team_name, player_idx, action)


async def game_loop_update_state(teams):
    game_over = True
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            ## get new game state
            state, dead, game_over = await get_state(team_name, player_idx)
            p_env.state = state
            ## calculate score
            output = p_env.step(p_env.action, state, dead, game_over)
            old_state = state
            state, action, reward, done = output
            p_env.add_to_history(old_state, action, reward, state, done)
            if not done:
                game_over = False
    return game_over


async def run_game(websocket, batch_size, epochs, num_teams = 2, num_players = 2, death_gamma=0.9999):
    game_over = False

    model = DRQNAgent(batch_size)
    teams = gen_teams(num_teams, num_players, death_gamma, model)

    no_action = get_action(0)
    ## get initial game state
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            sockets[player_idx] = websocket
            state, dead, game_over = await get_state(team_name, player_idx)
            p_env.state = state

    count = 0
    while not game_over:
        await game_loop_send_actions(teams)
        game_over = await game_loop_update_state(teams)
        count += 1
        if count == 40:
            game_over = True
    assert not await game_loop_update_state(teams)

    combined_histories = []
    for team_name in teams:
        for player_idx, p_env in enumerate(teams[team_name]):
            combined_histories.append(list(p_env.history))
    ## do one training loop
    merged = deque(list(itertools.chain.from_iterable(combined_histories)))
    model.memory = model.memory + merged
    for e in range(epochs):
        model.replay(batch_size)

    return model

async def main():
    uri = "ws://localhost:5678"
    async with websockets.connect(uri) as websocket:
        

        data = json.dumps({"type":"AI", "request":"map", "playerid":"","action":None})
        await websocket.send(data)

        rec = await websocket.recv()
        print(rec)
        if(json.loads(rec)['type'] == 'uID'):
            print('wrong json')
        else:
            main_state = json.loads(rec)
            print('--------------------------------')
            print(main_state)

        await run_game(websocket, 1, 2)
        #print(websocket.recv())

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()


