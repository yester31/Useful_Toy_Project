import os, json, time
import pandas as pd
import numpy as np
from ensemble_boxes import *
from tqdm import tqdm
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

id_matching = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31, 32,
               33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
               60, 61, 62, 63, 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90]

def load_csv(path):
    if os.path.isfile(path):  # path 파일이 있다면
        with open(path, 'r', encoding='UTF-8') as csvf:
            data = pd.read_csv(csvf)
        return data
    else:
        print('path is wrong')

def convert_format_step2(labels_list, scores_list, boxes_list, data, index, h, w):
    pstring = data['PredictionString'][index]
    if type(pstring) is float and np.isnan(pstring):  # 해당 이미지에 대한 결과가 없다면 리턴
        return

    n_pstring = np.array(pstring.split(' '))
    n_pstring = np.delete(n_pstring, len(n_pstring) - 1)

    for idx in range(len(n_pstring) // 6):
        idx6 = idx * 6
        label = float(id_matching[int(n_pstring[idx6])])
        score = float(n_pstring[idx6 + 1])
        x1 = float(n_pstring[idx6 + 2]) / w
        y1 = float(n_pstring[idx6 + 3]) / h
        x2 = float(n_pstring[idx6 + 4]) / w
        y2 = float(n_pstring[idx6 + 5]) / h

        labels_list.append(label)
        scores_list.append(score)
        boxes_list.append([x1, y1, x2, y2])

def convert_format_step1(labels_lists, scores_lists, boxes_lists, weights, data, row_idx, model_idx, h, w, weights_size):
    labels_list = []
    scores_list = []
    boxes_list = []
    convert_format_step2(labels_list, scores_list, boxes_list, data, row_idx, h, w)
    if len(labels_list) != 0:
        weights.append(weights_size[model_idx])
        labels_lists.append(labels_list)
        scores_lists.append(scores_list)
        boxes_lists.append(boxes_list)

def do_ensemble(save_path, datas, weights_size):
    with open(save_path, 'wt', encoding='UTF-8') as coco:
        ann = []
        start0 = time.time()
        for row_idx in tqdm(range(len(datas[0]))):
            image_id = data0['image_id'][row_idx]
            w = data0['width'][row_idx]
            h = data0['height'][row_idx]

            labels_lists = []
            scores_lists = []
            boxes_lists = []
            weights = []

            for model_idx in range(len(datas)):
                convert_format_step1(labels_lists, scores_lists, boxes_lists, weights, datas[model_idx], row_idx,
                                     model_idx, h, w, weights_size)

            if len(labels_lists) == 0:
                continue
            else:
                # boxes, scores, labels = nms(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.5) # 0.439
                # boxes, scores, labels = soft_nms(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.5, sigma=0.1, thresh=0.0001) # 0.440
                # boxes, scores, labels = non_maximum_weighted(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.5, skip_box_thr=0.0001) # 0.447
                # boxes, scores, labels = weighted_boxes_fusion(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.5, skip_box_thr=0.0001) # 0.454
                # boxes, scores, labels = weighted_boxes_fusion(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.6, skip_box_thr=0.001) # 0.459
                boxes, scores, labels = weighted_boxes_fusion(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.7, skip_box_thr=0.001)  # 0.460
                # boxes, scores, labels = weighted_boxes_fusion(boxes_lists, scores_lists, labels_lists, weights=weights, iou_thr=0.8, skip_box_thr=0.001) # 0.459

                for c_idx in range(len(labels)):
                    ann += [{'image_id': int(image_id),
                             'category_id': int(labels[c_idx]),
                             'bbox': [boxes[c_idx][0] * w,
                                      boxes[c_idx][1] * h,
                                      (boxes[c_idx][2] - boxes[c_idx][0]) * w,
                                      (boxes[c_idx][3] - boxes[c_idx][1]) * h],
                             'score': float(scores[c_idx]), }]

        json.dump(ann, coco)
    print('{} images, duration time : {} [sec]'.format(len(data0), time.time() - start0))


if __name__ == '__main__':

    # 1. file load
    path0 = 'outputs/submission20.csv'  # 40.631
    path1 = 'outputs/submission21.csv'  # 42.036
    path2 = 'outputs/submission22.csv'  # 43.047
    data0 = load_csv(path0)
    data1 = load_csv(path1)
    data2 = load_csv(path2)
    datas = []
    datas.append(data0)
    datas.append(data1)
    datas.append(data2)

    # 2. format convert & ensemble
    weights_size = [1, 2, 3]
    save_path = 'outputs/ensemble.json'
    do_ensemble(save_path, datas, weights_size)

    # 3. evaluate COCO AP
    coco_gt = COCO('outputs/instances_val2017.json')
    image_ids = sorted(coco_gt.getImgIds())
    coco_dt = coco_gt.loadRes(save_path)
    coco_eval = COCOeval(coco_gt, coco_dt, 'bbox')
    coco_eval.params.imgIds = image_ids
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()
