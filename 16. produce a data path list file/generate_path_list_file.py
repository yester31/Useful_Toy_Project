import os
import glob

'''
1. 지정 경로의 데이터셋 리스트 파일 만들기
*경로 리스트 파일 예시*
data path1, 클래스 인덱스
data path2, 클래스 인덱스
data path3, 클래스 인덱스

*로직
case1 -> 입력 폴더경로 아래 train or val 폴더가 존재 한다면, 그 안에 data들을 예시와 같은 형식으로 폴더명_train.txt 파일로 생성 (1차, 3차)
case2 -> 입력 폴더경로 아래 test 폴더가 존재 한다면, 그 안에 data들을 예시와 같은 형식으로 폴더명_test.txt 파일로 생성 (1차, 3차)
case3 -> 바로 클래스 폴더가 나오는 경우, 그 안에 data들을 아래 예시와 같은 형식으로 폴더명_train.txt 파일로 생성 (2차)

output:
output/list_file/1차_train.txt
output/list_file/2차_train.txt
output/list_file/3차_train.txt
output/list_file/1차_test.txt
output/list_file/3차_test.txt
'''

def generateFileList(save_path, dir_path, label):
    label_dict = {}
    for i, v in enumerate(label):
        label_dict[v] = i

    paths = [x for x in glob.iglob(dir_path + '/**') if os.path.isdir(x)]
    train_count = 0
    test_count = 0

    if not os.path.exists(save_path + '/list_file/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/list_file/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/list_file/'))

    train_list_file = open(save_path + '/list_file/' + dir_path.split('/')[-1] + '_train.txt', 'w', encoding='utf-8')
    test_list_file = open(save_path + '/list_file/' + dir_path.split('/')[-1] + '_test.txt', 'w', encoding='utf-8')

    for elem in paths:
        sub_dir_name = elem.split('\\')[-1]

        # case1
        if sub_dir_name == 'train' or sub_dir_name == 'val':
            for jpg in [x for x in glob.iglob(elem + '/**', recursive=True)]:
                jpg = jpg.replace('\\', '/')
                if jpg.split('.')[-1] == 'jpg':
                    train_count += 1
                    train_list_file.writelines([f"{jpg}, {label_dict[jpg.split('/')[-2]]}\n"])

        # case2
        elif sub_dir_name == 'test':
            for jpg in [x for x in glob.iglob(elem + '/**', recursive=True)]:
                jpg = jpg.replace('\\', '/')
                if jpg.split('.')[-1] == 'jpg':
                    test_count += 1
                    test_list_file.writelines([f"{jpg}, {label_dict[jpg.split('/')[-2]]}\n"])

        # case3
        else:
            for jpg in [x for x in glob.iglob(elem + '/**', recursive=True)]:
                jpg = jpg.replace('\\', '/')
                if jpg.split('.')[-1] == 'jpg':
                    train_count += 1
                    train_list_file.writelines([f"{jpg}, {label_dict[jpg.split('/')[-2]]}\n"])

    print('train_count : {}, test_count : {}'.format(train_count, test_count))
    train_list_file.close()
    test_list_file.close()

    if train_count == 0:
        if os.path.isfile(train_list_file.name):
            os.remove(train_list_file.name)

    if test_count == 0:
        if os.path.isfile(test_list_file.name):
            os.remove(test_list_file.name)

if __name__ == '__main__':
    label = ['cat', 'dog']
    dir_path = ['dataset/1차', 'dataset/2차', 'dataset/3차']
    save_path = 'output'
    for i, v in enumerate(dir_path):
        generateFileList(save_path, v, label)