import json
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# red , blue, green
color_map = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255),
             (0, 0, 127), (127, 0, 0), (0, 127, 0), (0, 127, 127), (127, 0, 127), (127, 127, 127),
             (0, 127, 255), (255, 127, 0)]

if __name__ == "__main__":

    dataset_label_path = 'D:/dataset/coco2017/annotations/instances_val2017.json'
    with open(dataset_label_path, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        categ_dict = {}
        for c_idx, categ in enumerate(categories):
            categ_dict[categ["id"]] = categ["name"]

        for i_idx, img in enumerate(images):
            img_path = 'D:/dataset/coco2017/val2017/' + img['file_name']

            # numpy 를 이용 하여 이미지 데이터 로드 (경로에 만약 한글이 포함 되어 있다면, cv2.imread()에서 파일을 못 읽음)
            img_array = np.fromfile(img_path, np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            for a_idx, anno in enumerate(annotations):
                if img['id'] == anno['image_id']:
                    bbox = anno['bbox']
                    seg = anno['segmentation']
                    color = color_map[anno['category_id'] % len(color_map)]

                    # PIL을 통하여 이미지에 한글 출력 (cv2.putText()에서 한글 출력 못 함, 빌드 새로 해야함..)
                    pimg = Image.fromarray(image)  # img 배열을 PIL이 처리 가능 하게 변환
                    name = categ_dict[anno['category_id']]  # 해당 category_id의 이름 가져오기
                    ImageDraw.Draw(pimg).text((bbox[0] + 5, bbox[1] + 10), name,
                                              font=ImageFont.truetype("fonts/gulim.ttc", 20),
                                              fill=color)  # 해당 라벨의 이름을 출력

                    # bounding box 출력
                    image = cv2.rectangle(np.array(pimg), (int(bbox[0]), int(bbox[1])),
                                          (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                                          color, 1)
                    # polygon 출력
                    if str(type(seg)) == '<class \'list\'>':
                        for pp_idx in range(len(seg)):
                            for p_idx in range(int(len(seg[pp_idx]) / 2)):
                                image = cv2.circle(image,
                                                   (int(seg[pp_idx][p_idx * 2]), int(seg[pp_idx][p_idx * 2 + 1])), 2,
                                                   color, -1)

            cv2.imshow('results', image)
            if cv2.waitKey() == 27:
                cv2.destroyWindow("results")
                break

        print("done")
