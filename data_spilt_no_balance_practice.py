import os, random, shutil
import argparse

def spilt_file(path):
    o_files = os.listdir(path)
    #print(files[0])
    files = os.listdir(path + '/' + o_files[0])
    #print(files[0])
    files_number = len(files)
    #print(files_number)
    rate = lists_rate[0]
    pick_number_test = int(files_number*rate)
    picked_sample_test = random.sample(files, pick_number_test)
    #print(len(picked_sample))
    
    '''
    root = 'dstfolder/slave1'
    for filename in listdir(join(root, 'slave')):
    move(join(root, 'slave', filename), join(root, filename))
    rmdir(join(root, 'slave'))
    '''
    for filename in picked_sample_test:
        shutil.move(os.path.join(path, o_files[0], filename) , os.path.join(path, 'test', filename))
    
    #test
    ##################################################################################
    files = os.listdir(path + '/' + o_files[0])
    #print(files_number)
    rate = lists_rate[1]
    pick_number_val = int(files_number*rate)
    picked_sample_val = random.sample(files, pick_number_val)

    for filename in picked_sample_val:
        shutil.move(os.path.join(path, o_files[0], filename) , os.path.join(path, 'val', filename))
    
    #val
    ##################################################################################

    files = os.listdir(path + '/' + o_files[0])

    for filename in files:
        shutil.move(os.path.join(path, o_files[0], filename) , os.path.join(path, 'train', filename))
    os.rmdir(os.path.join(path, o_files[0]))
    
    #train
    ##################################################################################

def setup(path):
    if not os.path.exists(path + '/train'):
        os.mkdir(path + '/train')
    else:
        print("file exists")
    if not os.path.exists(path + '/test'):
        os.mkdir(path + '/test')
    else:
        print("file exists")
    if not os.path.exists(path + '/val'):
        os.mkdir(path + '/val')
    else:
        print("file exists") 

def main():
    setup(path)
    spilt_file(path)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="輸入資料夾路徑")
    args = parser.parse_args()
    path = args.path
    lists_rate = [0.2, 0.1]
    main()
