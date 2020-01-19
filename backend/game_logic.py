#!/usr/bin/env python
import numpy as np
import os
from os import path
import json
import asyncio
import server
from time import sleep

class Player:
    def __init__(self, uid, x, y, team_id):
        self.uid = uid
        self.x = x
        self.y = y
        self.team_id = team_id

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

    def add_human_player(self, id_val):
        self.players[id_val] = Player(id_val, 5, 5, id_val)

    def handle_message(self, id_val, message):
        print("message :", message)
        request_resp = (None, None)
        if message["request"] != None:
            request_resp = self.handle_request(id_val, message["request"])
        if message["action"] != None:
            self.handle_action(id_val, message["action"])
        return request_resp

    def handle_request(self, id_val, request):
        if request == "map":
            return "map", self.board
            
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
        return np.loadtxt("map_1010_filled.txt")

    def move_player_left(self, player):
        print("Moving left")
        player.y -= 1

    def move_player_right(self, player):
        print("Moving right")
        player.y += 1

    def move_player_up(self, player):
        print("Moving up")
        player.x -= 1

    def move_player_down(self, player):
        print("Moving down")
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
    

