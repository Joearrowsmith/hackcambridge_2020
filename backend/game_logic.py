#!/usr/bin/env python
import numpy as np
import os
from os import path
import json
import asyncio
import server
from time import sleep

class Game:

    def __init__(self, **kwargs):
        self.board = self.generate_map()

    def generate_map(self):
        return np.loadtxt("grid_example.txt")

def load_config(path):
    with open(path) as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    config = load_config("./config.json") 
    game = Game(config=config)
    print(game.board)
    #server.run_server("127.0.0.1", 5678, game)
    

