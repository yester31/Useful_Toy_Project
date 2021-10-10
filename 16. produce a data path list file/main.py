from generate_path_list_file import *
from integrate_file_list import *
from splite_train_val import *

if __name__ == '__main__':
    label = ['cat', 'dog']
    dir_path = ['dataset/1차', 'dataset/2차', 'dataset/3차']
    save_path = 'output'

    # 1. 지정 경로의 데이터셋 리스트 파일 만들기
    for i, v in enumerate(dir_path):
        generateFileList(save_path, v, label)

    # 2. 여러 리스트 파일을 통합
    integrateFilelist(save_path)

    # 3. train & val 나눠기 (통합 파일에서 랜덤으로 나눠기 or 각 폴더 별 랜덤으로 나눠기)
    #spliteDataset1(save_path, 8, 2)
    spliteDataset2(save_path, 8, 2)

    # 4. 눠어진 클래스 별 수 출력
    showClassCount(save_path, label)