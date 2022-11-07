import os
import numpy as np
import multi_channel
import argparse


def save_multiarray_onezip(name, array_imgs, array_mask):
    name = name + '.npz'
    np.savez(name, a = array_imgs, b = array_mask)


#path = "E:\\New_Tree\\Practice_Tree_New\\tree3band"
#folders = [path + '/image', path + '/mask']

def read_file(folders, band):
    images = os.listdir(folders[0])
    masks = os.listdir(folders[1])

    img_list = []
    mask_list = []

    for m in masks:
        if m.endswith('.tif'):
            mask_list.append(m)

    for m in mask_list:
        only_file_name = m.replace('.tif', '')
        #print(only_file_name)
        lists = []
        for img in images:
            #print(img)
            #000000937_13.tif #一張 tif 圖被拆成好幾個 band 的 tif 圖
            #000000937_20.tif #ex: 如左邊, 000000937 就被拆成 3 個 tif 圖
            #000000937_32.tif
            if only_file_name in img:
                lists.append(img)
                #print(len(lists))

            if len(lists) == int(band):
                    img_list.append(lists)
                    #print(img_list)
                    break
            
    return img_list, mask_list

def write_file(folders, img_list, mask_list):
    combined_object = zip(img_list, mask_list)
    for imgs, mask in combined_object:
        #print(mask)
        #print(imgs)
        numpy_array_mask = multi_channel.merge_test(folders[1] + '/' + mask) #mask tif file to numpy array
        #print(len(numpy_array_mask))
        
        numpy_array_list = []
        for img in imgs:
            numpy_array_list.append(multi_channel.merge_test(folders[0] + '/' + img))
        #print(len(numpy_array_list))
        array_full_img = np.dstack(numpy_array_list)
        #print(len(array_full_img))
        name = folders[1] + '/' + mask
        #print(name)
        name = name.replace('mask', 'datas/npz')
        name = name.replace('.tif', '')
        print(name)
        save_multiarray_onezip(name, array_full_img, numpy_array_mask)
      

def setup(path):
    try:
        os.mkdir(path + '/datas')
    except FileExistsError:
        print("folder exist")
    try:
        os.mkdir(path + '/datas/npz/')
    except FileExistsError:
        print("folder exist")

#print(lists)
def main():
    print("start!!!!")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    parser.add_argument("band", type=str, help="輸入資料夾通道數")
    args = parser.parse_args()
    path = args.path
    band = args.band
    folders = [path + '/image', path + '/mask']

    setup(path)
    img_list, mask_list = read_file(folders, band)
    #print(len(img_list)) #938
    #print(len(mask_list)) #938
    #print((img_list))
    #print("#############################################")
    #print((mask_list))
    write_file(folders, img_list, mask_list)  


if __name__ == '__main__':
    main()
