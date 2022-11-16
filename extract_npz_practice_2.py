import os
import argparse
import numpy as np

def read_file(path):
    list_folder = os.listdir(path)
    for type_folder in list_folder:
        if type_folder.endswith('_label'):
            continue
        read_path = path + '/' + type_folder
        npz_list = os.listdir(read_path)

        for npz_file in npz_list:
            name_path = path + '/' + type_folder + '/' + npz_file
            nameA = name_path.replace('.npz','')
            nameB = nameA.replace(type_folder, type_folder + '_label')

            loaded_npz = np.load(name_path)
            loaded_img = loaded_npz['a']
            loaded_mask = loaded_npz['b']
            np.save(nameA, loaded_img)
            np.save(nameB, loaded_mask)


def remove_file(path):
    list_folder = os.listdir(path)
    for type_folder in list_folder:
        read_path = path + '/' + type_folder
        npz_list = os.listdir(read_path)

        for np_file in npz_list:
            if np_file.endswith('.npz'):
                os.remove(path + '/' + type_folder + '/' + np_file)
        #print(npz_list)


def setup(path):
    if not os.path.exists(path + '/train_label'):
        os.mkdir(path + '/train_label')
    else:
        print("file exists")
    if not os.path.exists(path + '/test_label'):
        os.mkdir(path + '/test_label')
    else:
        print("file exists")
    if not os.path.exists(path + '/val_label'):
        os.mkdir(path + '/val_label')
    else:
        print("file exists") 



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    setup(path)
    read_file(path)
    remove_file(path)

if __name__ == '__main__':
    main()