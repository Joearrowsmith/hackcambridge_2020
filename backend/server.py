import asyncio, websockets
import datetime, uuid, sys
import random, string, json

connections = {}

async def main(game, websocket, path):
    # a unique id for the connection
    ws_id = id(websocket)
    if ws_id not in connections:
        uID = str(uuid.uuid4())
        game.add_human_player(ws_id) 
        connections[ws_id] = {
            'sock' : websocket,
            'uID' : uID,
            'message' : "",
        }


    print(f"Responding to {ws_id}")
    

    # Unique ID for the game
    uIDJson = json.dumps({'type': 'uID', 'uID': ws_id})
    await websocket.send(uIDJson)
    

    try:
        async for message in websocket:
            print(f"New action: {message}")
            connections[ws_id]["message"] = message

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

async def game_tick(game):
    while True:
        responses = {}
        for player_id, vals in connections.items():
            responses[player_id] = game.handle_message(player_id, vals["message"])

        #update = game.get_update()
        player_positions = game.get_positions()

        for player_id, resp in responses.items():
            reply = {"response" : resp[0],
                     "response_data" : resp[1],
                     "update" : None
                     "positions" : player_positions
                     }

            connections[player_id]["sock"].send(reply)

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
