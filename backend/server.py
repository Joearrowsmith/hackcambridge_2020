import asyncio, websockets
import datetime, uuid, sys
import random, string, json

connections = {}

async def main(game, websocket, path):
    # a unique id for the connection
    ws_id = id(websocket)
    if game.state in (-1, 0) and ws_id not in connections:
        uID = str(uuid.uuid4())
        connections[ws_id] = {
            'sock' : websocket,
            'uID' : uID,
            'message' : {},
            'human' : None,
            'team' : game.teamcount,
        }
        #hacky af
        game.teamcount += 1

    # Unique ID for the game
    uIDJson = json.dumps({'type': 'uID', 'uID': ws_id})
    await websocket.send(uIDJson)
    

    try:
        async for message in websocket:
            print(f"New action: {message}")
            if validate_message(message):
                print("valid message")
                connections[ws_id]["message"] = json.loads(message)
            else:
                print("invalid message")

            '''
            can do a json data type with a type field
            if(data['type'] == 'xx'):
                await sample(data)
            '''
    except:
        pass

#async def status():
#    while True:
#        print(connections)
#        for ws_id, vals in connections.items():
#            await vals["sock"].send(vals["uID"])
#        await asyncio.sleep(3)

def ai_check(message):
    try:
        mess = json.loads(message)
    except json.decoder.JSONDecodeError as e:
        return False
    
    if "ai" in mess:
        return True
    else:
        return False
    

def validate_message(message):
    try:
        mess = json.loads(message)
    except json.decoder.JSONDecodeError as e:
        return False

    if "playerid" in mess:
        return True
    else:
        return False

def clear_queue():
    for _, v in connections.items():
        v["message"] = {}
    
async def game_tick(game):
    while True:
        if game.state == -1:
            if len(connections) >= 2:
                game.state = 0

            print("state -1")
            await asyncio.sleep(1)
        elif game.state == 0:
            print("state 0")
            if game.start_countdown == 0:
                await game.setup(connections)
                game.state = 1
            else:
                game.start_countdown -= 1
                clear_queue()
                await asyncio.sleep(1)
        elif game.state == 1:
            responses = {}
            for player_id, vals in connections.items():
                mess = vals["message"]
                if "playerid" in mess:
                    responses[player_id] = game.handle_message(player_id, mess)
                else:
                    responses[player_id] = [None, None]

                vals["message"] = {}

            #update = game.get_update()
            player_positions = game.get_positions()
            grids = game.generate_all_grids()

            for player_id, resp in responses.items():
                kill = None
                if not game.players[player_id].alive:
                    resp[0] = "status"
                    resp[1] = "death"
                    kill = player_id

                if game.players[player_id].winner:
                    resp[0] = "status"
                    resp[1] = "winner"

                

                if game.players[player_id].human:
                    reply = {"response" : resp[0],
                             "response_data" : resp[1],
                             "update" : None,
                             "positions" : player_positions
                            }
                else:
                    reply = {"grid" : game.get_9x9(player_id, grids[game.players["player_id"].team_id],
                             "messages" : ["","","",""],
                             "dead" : not game.players["player_id"].alive,
                             "over" : game.winner,
                            }

                print(reply)
                try:
                    await connections[player_id]["sock"].send(json.dumps(reply))
                except websockets.exceptions.ConnectionClosedOK:
                    pass

                if kill != None:
                    del connections[kill]

            #game.shrink_counter -= 0.05
            #if game.shrink_counter < 0:
            #    print("SHRINK")
            #    game.shrink()
            #    game.shrink_counter = 5
            #    
            #    for pid, vals in connections.items():
            #        await connections[pid]["sock"].send( json.dumps({
            #                            "response" : "map",
            #                            "response_data" : game.handle_request(pid, "map")[1],
            #                            "update" : None,
            #                            "positions" : game.get_positions()}))

                

            await asyncio.sleep(0.05)


def run_server(serverIP, port, game):
    print('Starting socket server....')
    print(f'Running on http://{serverIP}:{port}')
    start_server = websockets.serve(lambda x, y:main(game, x, y), serverIP, port)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    #loop.create_task(status())
    loop.create_task(game_tick(game))
    asyncio.get_event_loop().run_forever()
