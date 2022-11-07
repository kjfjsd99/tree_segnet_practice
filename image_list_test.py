import os

path = r"E:\New_Tree\Practice_Tree_New\tree3band"
folders = [path + '/image', path + '/mask']


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
    #print(lists)
        if len(lists) == 3:
            img_list.append(lists)
            #print(len(img_list))
            break   

