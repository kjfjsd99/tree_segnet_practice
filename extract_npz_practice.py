import os
import argparse
import numpy as np

def read_file(path):
    data_lsits = os.listdir(path)
    return data_lsits


def extract(data_path, type):   
    loaded_npz = np.load(data_path)
    #print(data_path)
    name = data_path.replace('.npz','')
    name_label = name.replace(type, type + '_label')
    #print(name)
    loaded_image = loaded_npz['a']
    loaded_mask = loaded_npz['b']

    np.save(name, loaded_image)
    np.save(name_label, loaded_mask)
    

    

def setup(path, folder_type):
    for d_floder in folder_type:
        try:
            os.mkdir(path + '/' + d_floder + '_label')
        except FileExistsError:
            print("file already exists!!!") 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    folder_type = ['train', 'test', 'val']
    setup(path, folder_type)

    for d_floder in folder_type:
        data_lists = read_file(path + '/' + d_floder)
        #print(len(data_lists))
        for data in data_lists:
            extract(path + '/' + d_floder + '/' + data, d_floder)
            os.remove(path + '/' + d_floder + '/' + data)


if __name__ == '__main__':
    main()