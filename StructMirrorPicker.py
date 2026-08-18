import os
import shutil

ROOT_PATH = '\\\\Ypci5\\I\\CDDVD\\DVD\\r18\\DLtmp3'
REPLACE_DIRNM = 'OutP'
#ROOT_PATH = 'C:\\Wk\\Priv\\Band'
mylist = []
fPathList = []

#def prcess(file_path):
    # 処理を記述


def recursive_file_check(path):
    if os.path.isdir(path):
        # directoryだったら中のファイルに対して再帰的にこの関数を実行
        files = os.listdir(path)
        #直下ファイルのみリスト
        files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
#        flCnt = len(files_file)
        i = 0
        for file in files_file:
            if i == 1:
                break
            fPathList.append(path + "\\" + file)
            i=i+1

        for file in files:
            if os.path.isdir(path + "\\" + file):
#                print(path + "\\" + file + "\n")
                mylist.append(path + "\\" + file)
            recursive_file_check(path + "\\" + file)
#    else:
#        # fileだったら処理
#        process(path)


recursive_file_check(ROOT_PATH)
for mylst in mylist:
#    print(mylst.replace('DLtmp3', REPLACE_DIRNM))
    os.makedirs(mylst.replace('DLtmp3', REPLACE_DIRNM), exist_ok=True)
for f in fPathList:
    print(f)
    shutil.move(f, f.replace('DLtmp3', REPLACE_DIRNM))