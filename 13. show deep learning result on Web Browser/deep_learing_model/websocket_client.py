import asyncio
import websockets
import cv2
import base64
import numpy as np
import json
import torch, torchvision
import time
from torchvision import transforms
from datetime import datetime

inst_classes = [
    '__background__',
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]
transform = transforms.Compose([
    transforms.ToTensor(),
])
def timestamp() :
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

async def connect(ip, port, wsid, wstype,model):

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

            # python client 코드에서 웹소켓을 통해 영상을 웹으로 전달하는 로직

            capture = cv2.VideoCapture(0)  # 웹캠
            while 1 :

                ret, frame = capture.read()
                image_cv_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_tensor = transform(image_cv_rgb)
                image_tensor_4d = torch.unsqueeze(image_tensor, 0)  # 차원 추가 ex) [x,x,x] -> [1,x,x,x]

                boc = time.time()
                predictions = model(image_tensor_4d.to(device))
                eoc = time.time()

                fps = 1 / (eoc - boc)
                boxes = predictions[0]['boxes'].cpu().detach().numpy()
                scores = predictions[0]['scores'].cpu().detach().numpy()
                labels = predictions[0]['labels'].cpu().detach().numpy()

                for i, prob in enumerate(scores):
                    if prob > 0.99:
                        x0, y0, x1, y1 = boxes[i]
                        cv2.rectangle(frame, (int(x0), int(y0)), (int(x1), int(y1)), (0, 255, 0), 3)
                        cv2.putText(frame, inst_classes[labels[i]], (int(x0), int(y0)-5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2)

                    cv2.putText(frame, f"fps = {fps:.2f}", (15, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 2)

                cv2.imshow("python", frame)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit

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

        except:
            print("error!!!")
            return 0

if __name__ == "__main__":

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.to(device)
    model.eval()

    ip = 'localhost'
    port = 8000
    wsid = 1
    wstype = 'pyc'
    asyncio.get_event_loop().run_until_complete(connect(ip, port, wsid, wstype,model))
    asyncio.get_event_loop().run_forever()
