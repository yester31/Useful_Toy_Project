# --------------------------------------------------------
# Detected objects Crop and Save by class
# Licensed under The MIT License
# Written by Derek
# 2021-06-27
# --------------------------------------------------------
import asyncio, websockets

'''
    간단한 파이썬 웹소켓 클라이언트 구현
'''

async def connect():

    # 웹 소켓에 접속을 합니다.
    async with websockets.connect("ws://localhost:8000") as websocket:
        # 웹 소켓 서버로 부터 메시지가 오면 콘솔에 출력
        while True :
            client_msg = input('> [client] ')
            await websocket.send(client_msg)

            server_msg = await websocket.recv()
            print('< [server] {}'.format(server_msg))



asyncio.get_event_loop().run_until_complete(connect())

