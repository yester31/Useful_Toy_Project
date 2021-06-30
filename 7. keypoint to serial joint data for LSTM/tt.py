# --------------------------------------------------------
# Detected objects Crop and Save by class
# Licensed under The MIT License
# Written by Derek
# 2021-06-27 ~ ...
# --------------------------------------------------------'
import math

import cv2, os, time

'''
COCO_KEYPOINT_INDEXES = {
    0: 'nose',
    1: 'left_eye',
    2: 'right_eye',
    3: 'left_ear',
    4: 'right_ear',
    
    5: 'left_shoulder',         -> 5
    6: 'right_shoulder',        -> 2
    7: 'left_elbow',            -> 6
    8: 'right_elbow',           -> 3
    9: 'left_wrist',            -> 7
    10: 'right_wrist',          -> 4
    11: 'left_hip',             -> 11
    12: 'right_hip',            -> 8
    13: 'left_knee',            -> 12
    14: 'right_knee',           -> 9
    15: 'left_ankle',           -> 13
    16: 'right_ankle'           -> 10
}
'''


def get_dist(x1, y1, x2, y2):
    if x1 == 0. or x2 == 0.:
        return 0.
    else:
        return math.sqrt(math.pow((x2 - x1), 2)+math.pow((y2 - y1), 2))

def get_deg(x1, y1, x2, y2):
    if x1 == 0. or x2 == 0.:
        return 0.
    dx = x2 - x1
    dy = y2 - y1
    rad = math.atan2(dy,dx)
    degree = math.degrees(rad)
    if (degree < 0.):
        degree += 360.
    return degree


def keypoint_to_jointdata(output_dir_path, input_dir_path, video_name):
    boc = time.time()




    print('====================================================================================')
    #print('{}th images to {} video done!'.format(len(images_list), video_name_ext))
    print('Duration time is {} [sec]'.format(time.time() - boc))
    print('====================================================================================')



if __name__ == "__main__":

    get_deg(1, 2, 3, 4)
