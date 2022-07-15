import os
import shutil
import random
import json

'''
This script is use to create a txt file that contain file list of reduced dataset.
Suppose you have the original dataset which have 100 images
Then you relabeled 20 of them. So only 80 images are needed to be relabeled
Then you can use this file to creat a file list of original dataset
Using relabeled dataset filename to eliminate list elements.
You get reduced_dataset.txt
Which is the format that can be accept by extract_dataset.py
'''

#request input
input_dir = input("please enter original folder path:\n")
relabeled_dir = input("please enter relabeled folder path:\n")

input_files_list = os.listdir(input_dir)
relabel_files_list = os.listdir(relabeled_dir)

for i in range(len(relabel_files_list)):
	try:
		input_files_list.remove(relabel_files_list[i-1])
	except:
		print(relabel_files_list[i-1])


with open('reduced_dataset.txt', "w+") as txt:
	json.dump(input_files_list, txt)

print(f'eliminate {len(relabel_files_list)}files, reduced_dataset now has {len(input_files_list)}files')