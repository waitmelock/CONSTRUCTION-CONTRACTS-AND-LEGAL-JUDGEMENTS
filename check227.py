from glob import glob
import sys
import os
import re
import shutil

current_path= "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/data/"
new_folder_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/check227-2/"

if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

paths = glob(current_path+'*.txt')
print("處理檔案: ",paths)
dic = {}

for i, path in enumerate(paths):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
        if '民法第227條之二' in text:
            print(f"'民法第227條之二' found in file {path}")
            shutil.copy(path, new_folder_path)
        else:
            print(f"'民法227條' not found in file {path}")