import os
import shutil
import random
import json

'''
The extract_dataset.py helps extract data from the original dataset within the relabeling process.
It recognize the reduced_dataset.txt and will see the original dataset as the reduced list.
This prevent from redundat label on images also preserive memory space by symbolizing reduced dataset by a txt file.
If there's no reduced dataset.txt file exist
We suppose you are extracting for the first time
So the script will create one file for you to utilize.

The folder structure should be like this
|--Dayun_Dataset
|   |--   Original_Dataset				#This is your original folder
|          |-- No1_001.jpg
|          |-- No1_001.xml               
|          `-- ...
|   |--   Checkpoint_0701
|          |-- Reduced_dataset 	        #This is your reduced txt folder     
|          `-- Reduced_dataset.txt      #txt file contains a filelist, indicating which image are already extracted
|										 so that they wouldn't be extracted again       
|          |-- Extracted_dataset	    #This is the extracted folder          
|          |-- Extracted_visualized             
|          |-- Append_dataset                    
|          `-- Relabeled_dataset                
'''

#request input
input_dir = input("please enter original folder path:\n")
reduced_dir = input("please enter folder path that contain reduced dataset.txt:\n")
extracted_dir = input("please enter extracted data path:\n")

#number of images
n_img = int(input("please enter extract number:\n"))

counter = n_img

reduced_txt = os.path.join(reduced_dir, "reduced_dataset.txt")

if os.path.exists(reduced_txt):
	with open(reduced_txt, 'r') as txt:
		jpg_list = json.load(txt)
		print("extracting from a reduced dataset...")
		print(f"reduced dataset contains {len(jpg_list)} images")
		for jpg_item in jpg_list:
			filename, fileformat = os.path.splitext(jpg_item)
			if fileformat != ".jpg":
				jpg_list.remove(jpg_item)
else:
	jpg_list = []
	for f in os.listdir(input_dir):
		filename, fileformat = os.path.splitext(f)
		if fileformat == '.jpg':
			jpg_list.append(f)
	print("extracting from the original dataset...")
	print(f"original dataset contains {len(jpg_list)} images")

shuffled_jpg_list = []

for item in jpg_list:

        shuffled_jpg_list.append(item)

random.shuffle(shuffled_jpg_list)

i = 0

while True:

	filename, file_format = os.path.splitext(shuffled_jpg_list[i])

	img_path = os.path.join(input_dir, shuffled_jpg_list[i])
	img_target = os.path.join(extracted_dir, shuffled_jpg_list[i])

	xml_path = os.path.join(input_dir, filename+".xml")
	xml_target = os.path.join(extracted_dir, filename+".xml")

	shutil.copy(img_path, img_target)
	shutil.copy(xml_path, xml_target)
	jpg_list.remove(shuffled_jpg_list[i])
	counter -= 1
	print(filename)
	i += 1


	if counter == 0:
		print('all files are moved')
		print(f"{n_img}images are extracted from the dataset, the reduced dataset now contain {len(jpg_list)} images")
		break
	elif len(jpg_list) == 0:
		print('running out of images from original dataset')
		print(f"{n_img-counter}images are extracted from the dataset, the reduced dataset now contain {len(jpg_list)} images")
		break

with open(reduced_txt, "w+") as txt:
	json.dump(jpg_list, txt)
