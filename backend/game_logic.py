#!/usr/bin/env python
import numpy as np
import os
from os import path
import json
import asyncio
import server
from time import sleep
import grid

class Player:
    def __init__(self, human, uid, x, y, team_id):
        self.human = human 
        self.uid = uid
        self.x = x
        self.y = y
        self.team_id = team_id
        self.alive = True
        self.winner = False

class Game:
    def __init__(self, **kwargs):
        self.board = self.generate_map()
        self.actions = {
                "move_left"  : self.move_player_left,
                "move_right" : self.move_player_right,
                "move_up"    : self.move_player_up,
                "move_down"  : self.move_player_down,
                "message"    : self.player_message,
                "push_left"  : self.push_player_left,
                "push_right" : self.push_player_right,
                "push_up"    : self.push_player_up,
                "push_down"  : self.push_player_down,
                }
        self.players = {}
        self.tick_update_list = []

        #0 - Setup
        #1 - Game running
        #2 - Game finished
        self.state = -1
        self.start_countdown = 2
        self.alive_count = 0        
        self.teamcount = 1
        self.team_alive = {}

    def add_human_player(self, id_val, id_team, pos):
        self.players[id_val] = Player(True, id_val, int(pos[0]), int(pos[1]), id_team)

    def add_ai_player(self, id_val):
        self.players[id_val] = Player(False, id_val, 5, 5, id_val)

    async def setup(self, connections):
        print(f"connections: {connections}")
        coords = grid.create_players(self.board, len(connections),len(connections))
        for team, players in coords.items():
            for pos, pid in zip(players, [p for p, v in connections.items() if v["team"] == team]):
                self.add_human_player(pid, team, pos)
                if team in self.team_alive:
                    self.team_alive[team] += 1
                else:
                    self.team_alive[team] = 1
                print("SENDING MAP")
                await connections[pid]["sock"].send( json.dumps({"response" : "map",
                                    "response_data" : self.handle_request(pid, "map")[1],
                                    "update" : None,
                                    "positions" : self.get_positions()
                                    }))

    def handle_message(self, id_val, message):
        print("message :", message)
        request_resp = [None, None]
        if message["request"] != None:
            request_resp = self.handle_request(id_val, message["request"])
        if message["action"] != None:
            self.handle_action(id_val, message["action"])
        return request_resp

    def handle_request(self, id_val, request):
        if request == "map":
            return ["map", self.board.tolist()]
            
    def handle_action(self, id_val, action):
        self.actions[action](self.players[id_val])

    def get_positions(self):
        deets = []
        for ids, p in self.players.items():
            deets.append({"id":p.uid,"x":p.x,"y":p.y,"team_id":p.team_id})
        return deets

    #def get_update(self):
    #    return self.tick_update_list

    def draw_grid(self):
        render_copy = self.board.copy()
        for uid, p in self.players.items():
            render_copy[p.x][p.y] = 1
        return render_copy

    def generate_map(self):
        return np.loadtxt("map_4060.txt")

    def run_die(self, pid):
        pid.alive = False
        self.team_alive[pid.team_id] -= 1
        
        alive_track = 0
        winner_id = None
        for team, count in self.team_alive.items():
            if count > 0:
                alive_track += 1
                winner_id = team

            if alive_track == 2:
                return
        if alive_track == 1:
            for p,v in self.players.items():
                if v.team_id == winner_id:
                    v.winner = True

    def run_push(self, player, x, y, direction):
        pushed = None
        for p,v in self.players.items():
            if v.x == x and v.y == y:
                pushed = v
                break

        if pushed == None:
            return

        if direction == 1:
            self.move_player_left(v)
        elif direction == 2:
            self.move_player_right(v)
        elif direction == 3:
            self.move_player_up(v)
        elif direction == 4:
            self.move_player_down(v)

        if self.board[x][y] == 0:
            return True
        else:
            return False


    def check_space(self, player, x, y, direction):
        val = self.board[x][y]
        pos = self.get_positions()
        if val == -2:# or :
            return False
        elif (x,y) in [(p['x'], p['y']) for p in pos]:
            return self.run_push(player, x, y, direction)
        elif val == -1:
            self.run_die(player)
            return True
        elif val == 0:
            return True

    def move_player_left(self, player):
        print("Moving left")
        if self.check_space(player, player.x, player.y-1, 1):
            player.y -= 1

    def move_player_right(self, player):
        print("Moving right")
        if self.check_space(player, player.x, player.y+1, 2):
            player.y += 1

    def move_player_up(self, player):
        print("Moving up")
        if self.check_space(player, player.x-1, player.y, 3):
            player.x -= 1

    def move_player_down(self, player):
        print("Moving down")
        if self.check_space(player, player.x+1, player.y, 4):
            player.x += 1

    def player_message(self, player, message):
        print(f"Message: {message}")

    def push_player_left(self, player):
        print("Pushing left")

    def push_player_right(self, player):
        print("Pushing right")

    def push_player_up(self, player):
        print("Pushing up")

    def push_player_down(self, player):
        print("Pushing down")

def load_config(path):
    with open(path) as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    config = load_config("./config.json") 
    game = Game(config=config)
    server.run_server("127.0.0.1", 5678, game)
    

