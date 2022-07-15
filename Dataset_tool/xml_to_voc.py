import xml.etree.ElementTree as ET
import os
import json
import shutil
import random

'''
This script helps convert xml format data into VOC format dataset. 
It is used to train YOLOX
'''

#split ratio
split = [0.6, 0.2, 0.2]

#request input
input_dir = input("please enter input folder path:\n")
target_dir = input('please enter target folder path:\n')


#check if dataset already exist
if os.path.isfile(os.path.join(target_dir, 'datacount.txt')):
    text = open(os.path.join(target_dir, 'datacount.txt'))
    datacount = text.readlines()
    datacount = int(datacount[0])
    print(datacount-1, 'images already exist!\n')
else:                  
    datacount = 1
    print('creating dataset...\n')

#building datastructure, check if the directory already exist
main_dir = os.path.join(target_dir, 'VOC2007')
img_path = os.path.join(main_dir, 'JPEGImages')
anno_path = os.path.join(main_dir, 'Annotations')
sets_path = os.path.join(main_dir, 'ImageSets')
txt_path = os.path.join(sets_path, 'Main')

if os.path.isdir(main_dir):
    print('appending dataset...\n')
else:
    print('making directories...\n')
    os.mkdir(main_dir)
    os.mkdir(anno_path)
    os.mkdir(sets_path)
    os.mkdir(txt_path)
    os.mkdir(img_path)

#identify txt files

train_txt = open(os.path.join(txt_path, 'train.txt'), 'w+', encoding = 'utf8')
val_txt = open(os.path.join(txt_path, 'val.txt'), 'w+', encoding = 'utf8')
test_txt = open(os.path.join(txt_path, 'test.txt'), 'w+', encoding = 'utf8')

# identify all the xml files in the annotations folder (input directory)
xml_paths = []

for root, dirs, files in os.walk(input_dir):
  for f in files:
    fullpath = os.path.join(root, f)
    ming=os.path.splitext (fullpath)
    str=ming[1]
    if str==".xml":
        xml_paths.append(fullpath)

n_samples = len(xml_paths)

#shuffle
random.shuffle(xml_paths)
counter = 0


# loop through each
print('inserting files...\n')
print('generating txts...\n')
for fil in xml_paths:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    jpgname = os.path.splitext(fil)[0]
    jpgpath = os.path.join(f"{jpgname}.jpg")
    
    # check if the label contains the corresponding image file
    if not os.path.exists(jpgpath):
        print(f"{filename} image does not exist!")
        continue
    else:
        #move jpg and xml files
        shutil.copy(os.path.join(jpgpath), os.path.join(img_path, f'{datacount}.jpg'))
        shutil.copy(os.path.join(fil), os.path.join(anno_path, f'{datacount}.xml'))
        if counter/n_samples < split[0]:
            train_txt.write(f'{datacount}\n')
        elif  split[0] <= counter/n_samples < (split[0]+split[1]):
            val_txt.write(f'{datacount}\n')
        elif counter/n_samples >= (split[0]+split[1]):
            test_txt.write(f'{datacount}\n')
                
    counter = counter +1
    datacount = datacount + 1

train_txt.close()
val_txt.close()
test_txt.close()

with open(os.path.join(target_dir, 'datacount.txt'), 'w+', encoding='utf8') as f:
    f.write(json.dumps(datacount))
    
print('finished!\n')
print('dataset now contain', datacount-1, 'images')

