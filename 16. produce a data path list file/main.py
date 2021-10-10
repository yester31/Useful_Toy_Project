from generate_path_list_file import *
from integrate_file_list import *
from splite_train_val import *

label = ['cat', 'dog']
label_dict = {}
for i, v in enumerate(label):
    label_dict[v] = i

if __name__ == '__main__':

    dir_path = ['dataset/1차', 'dataset/2차', 'dataset/3차']
    save_path = 'output'

    # 1. 지정 경로의 데이터셋 리스트 파일 만들기
    for i, v in enumerate(dir_path):
        generateFileList(save_path, v)

    # 2. 여러 리스트 파일을 통합
    integrateFilelist(save_path)

    # 3. train & val 나눠기 (통합 파일에서 랜덤으로 나눠기 or 각 폴더 별 랜덤으로 나눠기)
    #splite_dataset_1(save_path, 8, 2)
    splite_dataset_2(save_path, 8, 2)

    # 4. 눠어진 클래스 별 수 출력
    showClassCount(save_path)