import os
import glob
import random

'''
2. 여러 리스트 파일을 통합
(2-1. 만약 test가 없다면 위 train 리스트 파일을 이용하여 train & test 리스트 파일 재생성)
output:
output/tot_train/tot_train.txt (1차_train.txt + 2차_train.txt + 3차_train.txt)
output/test/test.txt           (1차_test.txt + 3차_test.txt)
'''

def integrateFilelist(save_path, test_ratio=0.1):
    if not os.path.exists(save_path + '/tot_train/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/tot_train/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/tot_train/'))

    if not os.path.exists(save_path + '/test/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/test/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/test/'))

    tot_train_file = open(save_path + '/tot_train/tot_train.txt', 'w', encoding='utf-8')
    test_file = open(save_path + '/test/test.txt', 'w', encoding='utf-8')

    count_test_file = 0
    count_train_tot = 0
    train_path = []
    for txt in [x for x in glob.iglob(save_path + '/list_file/*.txt')]:
        txt = txt.replace('\\', '/')
        flag = txt.split('/')[-1].split('.')[0].split('_')[-1]

        if flag == 'test':
            count_test_file += 1
            f = open(txt, 'r', encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                test_file.writelines(line)
            f.close()

        elif flag == 'train':
            f = open(txt, 'r', encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                count_train_tot += 1
                tot_train_file.writelines(line)
                train_path.append(line)
            f.close()

    # 만약 train 데이터만 주어진다면 9:1 비율로 test 데이터 리스트 파일 생성
    if count_test_file == 0:
        print('There are no test list file. made test file {} ratio randomly'.format(test_ratio))
        test = int(count_train_tot * test_ratio + 0.5)
        test_loc = random.sample(range(1, count_train_tot), test)
        for n in range(test):
            test_file.writelines(train_path[test_loc[n]])
            train_path.remove(train_path[test_loc[n]])

        tot_train_file.close()
        if os.path.isfile(tot_train_file.name):
            os.remove(tot_train_file.name)
        tot_train_file = open(save_path + '/tot_train/tot_train.txt', 'w', encoding='utf-8')

        for i, v in enumerate(train_path):
            tot_train_file.writelines(v)

    tot_train_file.close()
    test_file.close()

if __name__ == '__main__':

    save_path = 'output'
    integrateFilelist(save_path)
