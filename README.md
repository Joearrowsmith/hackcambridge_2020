# hackcambridge_2020

## Running a local session:
1. Run `backend/game_logic.py` with Python 3.6. Because we were lazy, path issues means you should launch this file from the repo root (the directory this README is in)
2. Open `public/index.html` in a browser to connect to the server 

Note that the default uses port 5678 on localhost, you will need to change the source code in `backend/server.py` and `public/static/js/gamelogic.js` to reflect your desired port.
The server requires two or more players to connect to the server before the game commences. After two players connect, a 5 second countdown runs to give time for other players to join. 

The game can only be served on a localhost. To access this between multiple computers, a service to share localhost is required. During development we used [ngrok](https://ngrok.com/), but cannot vouch for reliability or security. After starting an ngrok session, a url will be given that will connect to the host's localhost. Other computers wishing to connect to this server will need to edit the address in their copy of `public/static/js/gamelogic.js` to reflect the ngrok address. Note that the `http` or `https` in the ngrok address should be replaced with `ws` or `wss` as websockets rather than http are being used. 

## References

- OpenAI - Hide and Seek paper
- DRQN - https://arxiv.org/pdf/1507.06527.pdf
