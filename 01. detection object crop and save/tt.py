# --------------------------------------------------------
# Detected objects Crop and Save by class
# Licensed under The MIT License
# Written by Derek
# 2021-06-26
# --------------------------------------------------------'
import os, cv2, uuid, time
import numpy as np

# deep learning 모델에 결과로 detection된 객체들의 이미지를 파일로 클래스 별로 저장하는 예제 코드
# 각 frame에서 detection된 객체들의 객체 별 box, class id 이용하여 분류 저장

'''
    생성되는 디렉토리 구조 
    - root dir - sub_root_dir - class_name0 - frame0_0_uuid
                                            - frame0_1_uuid
                              - class_name1 - frame0_0_uuid 
                              - class_name2 - frame0_0_uuid 
                                                                              
               - sub_root_dir - class_name1 - frame0_0_uuid
'''

class_name_table = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

def save_box_img(object_class_lsit, object_box_list, frame_id, frame, video_name, dir_root_path = './dataset') :
    boc = time.time()

    unique_number = str(uuid.uuid1())                       # 유니크 숫자 생성
    if os.path.exists(dir_root_path) is False:              # 이미지를 저장할 최상위 폴더가 없다면
        os.makedirs(dir_root_path)                          # 최상위 폴더 생성
        print('make directory {} is done'.format(dir_root_path))

    dir_sub_root_path = os.path.join(dir_root_path, video_name)  # 해당 영상(video_name)에 대한 이미지를 저장할 폴더 경로
    if os.path.exists(dir_sub_root_path) is False:               # 해당 영상에 대한 폴더가 없다면
        os.makedirs(dir_sub_root_path)                           # 해당 영상에 대한 폴더 생성
        print('make directory {} is done'.format(dir_sub_root_path))

    for oidx, class_id in enumerate(object_class_lsit):                 # 모델에서 찾은 객체 리스트
        class_name = class_name_table[int(class_id)]                    # 해당 객체 클래스 이름
        dir_class_path = os.path.join(dir_sub_root_path , class_name)   # 클래스 폴더 경로
        image_file_name = '{}_{}_{}.jpg'.format(frame_id, oidx, unique_number) # 이미지 파일 이름{프레임 번호}_{해당 프레임 객체 인식번호}_{유니크값}.jpg
        image_file_path = os.path.join(dir_class_path, image_file_name) # 클래스 폴더 경로

        x1, y1 = int(object_box_list[oidx, 0]), int(object_box_list[oidx, 1])
        x2, y2 = int(object_box_list[oidx, 2]), int(object_box_list[oidx, 3])
        croped_object_image = frame[y1:y2,x1:x2] # y1 y2 x1 x2

        if os.path.exists(dir_class_path):                      # 해당 클래스 폴더가 있으면
            cv2.imwrite(image_file_path, croped_object_image)   # 그냥 저장
        else :                                                  # 해당 클래스 폴더가 없으면
            os.makedirs(dir_class_path)                         # 클래스 폴더 생성 후
            print('make directory {} is done'.format(dir_class_path))
            cv2.imwrite(image_file_path, croped_object_image)   # 저장

        print('({}/{}) save file {} is done'.format(oidx,len(object_class_lsit), image_file_path))

    print('====================================================================================')
    print('Detected object image crop and save process is done')
    print('Duration time is {} [sec]'.format(time.time() - boc))
    print('====================================================================================')

if __name__ == "__main__":

    #yolov5s 결과 예시(원본 frame 이미지 사이즈로 리사이즈 및 패딩 처리 후)
    #                    x1            y1           x2          y2           prob       class_id
    pred = np.array([[2.00000e+00, 3.47000e+02, 4.56000e+02, 6.82000e+02, 9.38516e-01, 2.00000e+00],
                    [5.88000e+02, 4.04000e+02, 8.81000e+02, 6.32000e+02, 9.18750e-01, 2.00000e+00],
                    [5.75000e+02, 3.99000e+02, 6.24000e+02, 4.41000e+02, 8.62566e-01, 2.00000e+00],
                    [6.11000e+02, 3.99000e+02, 6.91000e+02, 4.53000e+02, 7.66945e-01, 2.00000e+00],
                    [9.80000e+02, 3.90000e+02, 1.04700e+03, 4.23000e+02, 7.01548e-01, 2.00000e+00],
                    [4.37000e+02, 3.71000e+02, 5.59000e+02, 4.83000e+02, 6.38990e-01, 7.00000e+00],
                    [6.34000e+02, 3.28000e+02, 6.41000e+02, 3.45000e+02, 5.99452e-01, 9.00000e+00],
                    [5.45000e+02, 3.24000e+02, 5.59000e+02, 3.40000e+02, 5.74450e-01, 9.00000e+00],
                    [8.09000e+02, 3.94000e+02, 8.25000e+02, 4.32000e+02, 5.48406e-01, 0.00000e+00],
                    [5.52000e+02, 3.89000e+02, 5.79000e+02, 4.34000e+02, 5.12884e-01, 2.00000e+00],
                    [6.65000e+02, 3.40000e+02, 7.46000e+02, 4.10000e+02, 4.92299e-01, 7.00000e+00],
                    [7.93000e+02, 3.96000e+02, 8.06000e+02, 4.14000e+02, 4.88801e-01, 0.00000e+00],
                    [7.71000e+02, 3.90000e+02, 7.84000e+02, 4.09000e+02, 4.52478e-01, 0.00000e+00],
                    [9.04000e+02, 3.95000e+02, 9.23000e+02, 4.18000e+02, 4.35165e-01, 0.00000e+00],
                    [5.56000e+02, 3.25000e+02, 5.64000e+02, 3.40000e+02, 3.84715e-01, 9.00000e+00],
                    [8.24000e+02, 4.00000e+02, 8.37000e+02, 4.38000e+02, 3.59820e-01, 0.00000e+00],
                    [7.01000e+02, 4.29000e+02, 7.47000e+02, 4.64000e+02, 3.52281e-01, 0.00000e+00],
                    [6.65000e+02, 3.39000e+02, 7.46000e+02, 4.09000e+02, 3.46599e-01, 5.00000e+00],
                    [1.01900e+03, 3.89000e+02, 1.03900e+03, 4.11000e+02, 3.08561e-01, 0.00000e+00],
                    [7.57000e+02, 3.86000e+02, 7.70000e+02, 4.08000e+02, 2.78430e-01, 0.00000e+00],
                    [6.33000e+02, 3.73000e+02, 6.67000e+02, 4.02000e+02, 2.56180e-01, 7.00000e+00]])

    frame = cv2.imread('NY_720x1280.jpg')   # 해당 frame image (예시) NY_720x1280.jpg
    object_class_lsit = pred[:,5]           # class id list
    object_box_list = pred[:,0:4]           # box list (x1 y1 x2 y2)
    video_name = 'video_name'               # 영상 이름 (영상별로 구별하여 저장하고 싶은 경우 사용, 폴더명과 파일명에 포함됨)
    frame_id = 0                            # 해당 프레임 id (몇 번째 frame인지)
    dir_root_path = './dataset'             # 이미지를 저장할 최상위 폴더 경로 선택

    save_box_img(object_class_lsit, object_box_list, frame_id, frame, video_name, dir_root_path)



