import asyncio, websockets
import datetime, uuid, sys
import random, string, json

connections = {}

async def main(websocket, path):
    # a unique id for the connection
    ws_id = id(websocket)
    if ws_id not in connections:
        uID = str(uuid.uuid4())
        connections[id(websocket)] = {
            'sock' : websocket,
            'uID' : uID,
        }
    #    await websocket.send(game


    print(f"Responding to {ws_id}")

    # Unique ID for the game
    uIDJson = json.dumps({'type': 'uID', 'uID': ws_id})
    await websocket.send(uIDJson)
    

    try:
        async for message in websocket:
            print(message)

            #data = json.loads(message)

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

def run_server(serverIP, port, game):
    print('Starting socket server....')
    print(f'Running on http://{serverIP}:{port}')
    start_server = websockets.serve(main, serverIP, port)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.create_task(status())
    asyncio.get_event_loop().run_forever()
