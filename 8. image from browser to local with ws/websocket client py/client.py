import asyncio
import websockets
import cv2
import base64
import numpy as np
import json
from datetime import datetime

def timestamp() :
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

async def connect(ip, port, wsid, wstype):

    # 웹 소켓에 접속
    async with websockets.connect("ws://{}:{}/wsid={}&wstype={}".format(ip, port,wsid, wstype)) as websocket:
        try:
            if websocket.open == True:
                init_websocket_msg = {
                    'optype': 'init_websocket',
                    'wsid': wsid,
                    'wstype': wstype,
                    'msg': 'Hello Server ? I am py',
                    'timestamp': timestamp()
                }
                jsonString = json.dumps(init_websocket_msg) # json 객체를 인코딩하여 string으로 만듬
                await websocket.send(jsonString)

            # 전달 받은 base64로 인코딩된 frame을 이미지로 변환하여 opencv로 영상 형태로 출력
            while 1 :
                data = await websocket.recv()
                jsonObject = json.loads(data) # json 디코딩 (string 형태의 데이터를 json 객체로 만듬)
                optype = jsonObject.get("optype") # dic 데이터 형식으로 호출

                if optype == "input":
                    raw_frame = jsonObject.get("frame")
                    step1 = str(raw_frame.split(',')[1])
                    step2 = base64.b64decode(step1)
                    step5 = np.frombuffer(step2, np.uint8)
                    frame = cv2.imdecode(step5, cv2.IMREAD_COLOR)
                    cv2.imshow('(3) python_code', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
                    result, encimg = cv2.imencode('.jpg', frame, encode_param)
                    if False == result:
                        print('could not encode image!')

                    # 이미지를 String 형태로 변환(인코딩)시키는 과정
                    encoded_output = base64.b64encode(encimg).decode('utf-8')
                    output_msg = {
                        'optype': 'output',
                        'wsid': wsid,
                        'wstype': wstype,
                        'frame': encoded_output,
                        'timestamp': timestamp()
                    }
                    jsonString = json.dumps(output_msg) # json 객체를 인코딩하여 string으로 만듬
                    await websocket.send(jsonString)

                else:
                    print("[ERROR]  메시지 : {}".format(data))

            # python client 코드에서 웹소켓을 통해 영상을 전달하는 로직
            '''
            capture = cv2.VideoCapture(0)  # 웹캠
            while 0 :
                ret, frame = capture.read()
                frame = cv2.resize(frame, dsize=(350, 260), interpolation=cv2.INTER_AREA)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
                result, encimg = cv2.imencode('.jpg', frame, encode_param)
                if False == result:
                    print('could not encode image!')

                # 이미지를 String 형태로 변환(인코딩)시키는 과정
                encoded = base64.b64encode(encimg).decode('utf-8')
                input_msg = {
                    'optype': 'output',
                    'wsid': wsid,
                    'wstype': wstype,
                    'frame': encoded,
                    'timestamp': timestamp()
                }
                jsonString = json.dumps(input_msg)  # json 객체를 인코딩하여 string으로 만듬
                await websocket.send(jsonString)
            '''
        except:
            print("error!!!")
            return 0

if __name__ == "__main__":

    ip = 'localhost'
    port = 8000
    wsid = 1
    wstype = 'pyc'
    asyncio.get_event_loop().run_until_complete(connect(ip, port, wsid, wstype))
    asyncio.get_event_loop().run_forever()
