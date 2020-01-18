#!/usr/bin/env python
import asyncio, websockets
import datetime, uuid, sys
import random, string, json

gameState = {}
serverIP = '127.0.0.1'

# Port number to use
if (len(sys.argv) > 1):
    serverPort = sys.argv[1]
else:
    serverPort = 5678

print('Starting socket server....')
print('Running on http://'+str(serverIP)+':'+str(serverPort))


async def main(websocket, path):
    # a unique id for the connection
    uID = str(uuid.uuid4())
    gameState[id(websocket)] = {
        'sock' : websocket,
        'uID' : uID,
    }

    socketID = id(websocket)

    # Unique ID for the game
    uIDJson = json.dumps({'type': 'uID', 'uID': socketID})
    await websocket.send(uIDJson)
    

    try:
        async for message in websocket:

            data = json.loads(message)

            '''
            can do a json data type with a type field
            if(data['type'] == 'xx'):
                await sample(data)
            '''

    finally:

        del gameState[id(websocket)]


start_server = websockets.serve(main, serverIP, int(serverPort))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()