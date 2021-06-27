# --------------------------------------------------------
# Detected objects Crop and Save by class
# Licensed under The MIT License
# Written by Derek
# 2021-06-27
# --------------------------------------------------------
import asyncio
import websockets

'''
    간단한 파이썬 웹소켓 서버 구현
    클라이언트로 부터 메시지를 받으면 번갈아 가며 주고 받을수 있음.
'''

async def simpleServer(websocket, path):

    client_msg = await websocket.recv()
    print('< [client] {}'.format(client_msg))

    resp = input('> [server] ')
    await websocket.send(resp)


port = 8000
start_server = websockets.serve(simpleServer, "localhost", port) # 웹소켓 객체 생성
print('Server on localhost:{}'.format(port))
asyncio.get_event_loop().run_until_complete(start_server)        # 비동기로 웹소켓 실행
asyncio.get_event_loop().run_forever()