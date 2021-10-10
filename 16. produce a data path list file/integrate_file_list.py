import os
import glob
from main import *

'''
2. 여러 리스트 파일을 통합
(2-1. 만약 test가 없다면 위 train 리스트 파일을 이용하여 train & test 리스트 파일 재생성)
output:
output/tot_train/tot_train.txt (1차_train.txt + 2차_train.txt + 3차_train.txt)
output/test/test.txt           (1차_test.txt + 3차_test.txt)
'''

def integrateFilelist(save_path):
    if not os.path.exists(save_path + '/tot_train/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/tot_train/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/tot_train/'))

    if not os.path.exists(save_path + '/test/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/test/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/test/'))

    tot_train_file = open(save_path + '/tot_train/tot_train.txt', 'w', encoding='utf-8')
    test_file = open(save_path + '/test/test.txt', 'w', encoding='utf-8')

    list_file_dir_path = save_path + '/list_file'
    for txt in [x for x in glob.iglob(list_file_dir_path + '/*.txt')]:
    #for txt in list_file_dir_path.glob('*.txt'):  # 경로 안에 txt파일 하나씩 선택
        print(txt)



if __name__ == '__main__':

    save_path = 'output'
    integrateFilelist(save_path)
