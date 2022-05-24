import torchvision, torch
from torchvision import transforms
import cv2
import time
from PIL import Image

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

if __name__ == '__main__':
    # train on the GPU or on the CPU, if a GPU is not available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(device)

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    if 0: # one test image run
        file_path = "./dog.jpg"
        #image_pil = Image.open(file_path)
        #image = transform(image_pil)
        image_cv = cv2.imread("./dog.jpg")
        image_cv_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_tensor = transform(image_cv_rgb)
        image_tensor_4d = torch.unsqueeze(image_tensor, 0) # 차원 추가 ex) [x,x,x] -> [1,x,x,x]

        predictions = model(image_tensor_4d.to(device)).cpu()

        boxes = predictions[0]['boxes'].detach().numpy()
        scores = predictions[0]['scores'].detach().numpy()
        labels = predictions[0]['labels'].detach().numpy()

        for i, prob in enumerate(scores):
            if prob > 0.9:
                x0, y0, x1, y1 = boxes[i]
                cv2.rectangle(image_cv,(int(x0),int(y0)),(int(x1),int(y1)),(0,255,0),3)
                cv2.imshow("test", image_cv)
                cv2.waitKey(0)
    else: # webcam run
        video = cv2.VideoCapture(0)
        while video.isOpened():
            success, frame = video.read()
            if success:

                image_cv_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_tensor = transform(image_cv_rgb)
                image_tensor_4d = torch.unsqueeze(image_tensor, 0)  # 차원 추가 ex) [x,x,x] -> [1,x,x,x]

                boc = time.time()
                predictions = model(image_tensor_4d.to(device))
                eoc = time.time()

                fps = 1 / (eoc-boc)
                boxes = predictions[0]['boxes'].cpu().detach().numpy()
                scores = predictions[0]['scores'].cpu().detach().numpy()
                labels = predictions[0]['labels'].cpu().detach().numpy()

                for i, prob in enumerate(scores):
                    if prob > 0.98:
                        x0, y0, x1, y1 = boxes[i]
                        cv2.rectangle(frame, (int(x0), int(y0)), (int(x1), int(y1)), (0, 255, 0), 3)
                        cv2.putText(frame, inst_classes[labels[i]], (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

                    cv2.putText(frame, f"fps = {fps:.2f}", (15 , frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)

                cv2.imshow("test", frame)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit

            else:
                print("video is wrong!")
                break
