import os
import argparse

def read_file(path):
    folder_list = os.listdir(path)
    #print(folder_list)
    all_path_list = []
    for folder in folder_list:
        #print(folder)
        sub_path = path + '/' + folder
        subfolder_list = os.listdir(sub_path)
        #print(subfolder_list)
        subfolder_path_list = []
        for subfolder in subfolder_list:
            img_path = path + '/' + folder + '/' + subfolder
            #print(img_path)
            subfolder_path_list.append(img_path)
        all_path_list.append(subfolder_path_list)
    #print(all_path_list[1])

    zip_list = zip(all_path_list[0], all_path_list[1], all_path_list[2])
    #print(list(zip_list)[0])
    for i, j, k in zip_list:
        #print(i, j, k)
        num = len(os.listdir(i)) + len(os.listdir(j)) + len(os.listdir(k))
        print(num)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    read_file(path)


if __name__ == '__main__':
    main()