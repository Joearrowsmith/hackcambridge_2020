#!/usr/bin/env python
import numpy as np
import os
from os import path
import json
import asyncio
import server
from time import sleep

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Game:

    def __init__(self, **kwargs):
        self.board = self.generate_map()
        self.actions = {
                "move_left"  : self.move_player_left,
                "move_right" : self.move_player_right,
                "move_up"    : self.move_player_up,
                "move_down"  : self.move_player_down,
                "message"    : self.handle_message,
                "push_left"  : self.push_player_left,
                "push_right" : self.push_player_right,
                "push_up"    : self.push_player_up,
                "push_down"  : self.push_player_down,
                }
        self.players = {}

    def add_player(self, id_val):
        self.players[id_val] = Player(1, 2)

    def generate_map(self):
        return np.loadtxt("grid_example.txt")

    def move_player_left(self, player):
        print("Moving left")

    def move_player_right(self, player):
        print("Moving right")

    def move_player_up(self, player):
        print("Moving up")

    def move_player_down(self, player):
        print("Moving down")

    def handle_message(self, player, message):
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
    

