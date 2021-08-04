# --------------------------------------------------------
# squence images to video file
# Licensed under The MIT License
# Written by Derek
# 2021-06-27
# --------------------------------------------------------
import cv2, os, time

'''
    연속 또는 무작위 다수 이미지 파일을 영상으로 만들기 
    데이터셋 출처 : https://motchallenge.net/data/MOT16/
'''

def imgs_to_video(output_dir_path, input_dir_path, video_name):
    boc = time.time()

    if not os.path.exists(output_dir_path):                         # 비디오를 저장할 폴더가 없다면
        os.makedirs(output_dir_path)                                # 폴더 생성
        print('make directory {} is done'.format(output_dir_path))

    video_name_ext = '{}.mp4'.format(video_name)                    # 비디오 파일 이름{input folder name}.mp4
    video_save_path = os.path.join(output_dir_path, video_name_ext) # 저장될 비디오 경로
    images_list = os.listdir(input_dir_path)                        # 이미지 파일 이름 리스트 불러오기

    first_image_path = os.path.join(input_dir_path, images_list[0]) # 첫번째 이미지 파일 경로
    first_image = cv2.imread(first_image_path)                      # 첫번째 이미지 로드
    height, width, layers = first_image.shape                       # 이미지 사이즈
    size = (width, height)                                          # 저장할 비디오 사이즈
    fps = 30                                                        # 저장할 비디오 fps
    out = cv2.VideoWriter(video_save_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size) # 비디오로 쓰기 위해 비디오 객체 생성

    for idx, image_name in enumerate(images_list):              # 이미지 저장 폴더에서 하나씩 꺼내오기
        img_path = os.path.join(input_dir_path, image_name)     # 각 이미지 파일 경로
        image = cv2.imread(img_path)                            # 이미지 로드
        out.write(image)                                        # 비디오 객체에 이미지 쓰기
        print('({}/{}) image to {} video'.format(idx, len(images_list), video_name_ext))

    out.release()                                               # 비디오 객체 메모리 해제

    print('====================================================================================')
    print('{}th images to {} video done!'.format(len(images_list), video_name_ext))
    print('Duration time is {} [sec]'.format(time.time() - boc))
    print('====================================================================================')

if __name__ == "__main__":

    input_dir_path = './MOT16-14/img1'   # 이미지들 저장 경로
    output_dir_path = './videos'         # 저장될 비디오 경로
    video_name = 'MOT16-14'              # 생성할 비디오 이름

    imgs_to_video(output_dir_path, input_dir_path, video_name)