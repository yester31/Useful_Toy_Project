from generate_path_list_file import *

label = ['cat', 'dog']
label_dict = {}
for i, v in enumerate(label):
    label_dict[v] = i

if __name__ == '__main__':

    dir_path = ['dataset/1차', 'dataset/2차', 'dataset/3차']
    save_path = 'output'
    for i, v in enumerate(dir_path):
        generateFileList(save_path, v)

