import os
import glob
import random

'''
3. train & val 나누기 (통합 파일에서 랜덤으로 나누기 or 각 폴더 별 랜덤으로 나누기)
output:
output/train/train.txt
output/train/val.txt
'''

# 해당 리스트 파일에서 클래스별 수 반환
def getClassCount(list_file_path, label):
    print(list_file_path)
    label_count_dict = {}
    for i, v in enumerate(label):
        label_count_dict[v] = 0

    f = open(list_file_path, 'r', encoding='utf-8')
    lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        label_count_dict[label[int(line.split(',')[-1].strip())]] += 1
    f.close()
    print(label_count_dict)
    print('Total count : {}'.format(count))
    print()
    return label_count_dict, count

def showClassCount(save_path, label):
    for paths in [x for x in glob.iglob(save_path + '/**', recursive=True)]:
        paths = paths.replace('\\', '/')
        if paths.split('.')[-1] == 'txt':
            getClassCount(paths, label)

# tot_train.txt에서 입력한 비율로 train, val 리스트를 랜덤하게 나누기
def spliteDataset1(save_path, train, val):
    if not os.path.exists(save_path + '/train/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/train/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/train/'))

    ratio = val / (train+val)
    train_file = open(save_path + '/train/train.txt', 'w', encoding='utf-8')
    val_file = open(save_path + '/train/val.txt', 'w', encoding='utf-8')

    f = open(save_path + '/tot_train/tot_train.txt', 'r', encoding='utf-8')
    data_path_list = f.readlines()
    f.close()
    count = len(data_path_list)

    val_n = int(count * ratio + 0.5)
    train_n = int(count - val_n)

    val_loc = random.sample(range(1, count), val_n)
    val_path = []

    for n in range(val_n):
        val_path.append(data_path_list[val_loc[n]])
    train_path = data_path_list
    for a in range(val_n):
        train_path.remove(val_path[a])

    for i, v in enumerate(train_path):
        train_file.writelines(v)

    for i, v in enumerate(val_path):
        val_file.writelines(v)

    train_file.close()
    val_file.close()

# 차수 별로 (거의)동일하게 val 값 추출
def spliteDataset2(save_path, train, val):
    if not os.path.exists(save_path + '/train/'):  # 저장할 폴더가 없다면
        os.makedirs(save_path + '/train/')  # 폴더 생성
        print('make directory {} is done'.format(save_path + '/train/'))

    train_file = open(save_path + '/train/train.txt', 'w', encoding='utf-8')
    val_file = open(save_path + '/train/val.txt', 'w', encoding='utf-8')
    ratio = val / (train + val)

    for txt in [x for x in glob.iglob(save_path + '/list_file/*.txt')]:
        txt = txt.replace('\\', '/')
        flag = txt.split('/')[-1].split('.')[0].split('_')[-1]
        if flag == 'train':
            f = open(txt, 'r', encoding='utf-8')
            data_path_list = f.readlines()
            f.close()
            count = len(data_path_list)

            val_n = int(count * ratio + 0.5)
            train_n = int(count - val_n)

            val_loc = random.sample(range(1, count), val_n)
            val_path = []

            for n in range(val_n):
                val_path.append(data_path_list[val_loc[n]])
            train_path = data_path_list
            for a in range(val_n):
                train_path.remove(val_path[a])

            for i, v in enumerate(train_path):
                train_file.writelines(v)

            for i, v in enumerate(val_path):
                val_file.writelines(v)

    train_file.close()
    val_file.close()


if __name__ == '__main__':
    label = ['cat', 'dog']
    save_path = 'output'
    #spliteDataset1(save_path, 8, 2)
    spliteDataset2(save_path, 8, 2)
    showClassCount(save_path, label)



