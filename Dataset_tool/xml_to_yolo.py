import xml.etree.ElementTree as ET
import os
import json
import shutil
import random
import re

'''
This script has to usage:
1. Create yolo format dataset
2. Append existing yolo format dataset with new images

The input folder can only contain jpg and xml files with corresponding names:
The target folder will generate a yolo format dataset like this
|--Target folder
|   |--   train              
|          |-- images
|          |-- annotations
|   |--   val              
|          |-- images
|          |-- annotations 
|   |--   test              
|          |-- images
|          |-- annotations
|   |--   datacount.txt     #This contains the datacount, when appending dataset we can accumulate datacount
|   |--   classes.txt

if the target folder already exist, then the program will append the existing dataset with the input dir                
also, you can change the split ratio here.               
'''

#split ratio for train, val, test 
split = [0.7, 0.1, 0.2]
classes =  ["person", "car", "motorbike", "bus", "truck", "bike"]

#transfrom funciton
def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

#request input
input_dir = input("please enter input folder path:\n")
target_dir = input('please enter target folder path:\n')


#check if dataset already exist, if there is, append the dataset
if os.path.isfile(os.path.join(target_dir, 'datacount.txt')):
    text = open(os.path.join(target_dir, 'datacount.txt'))
    datacount = text.readlines()
    datacount = int(datacount[0])
    print(datacount-1, 'images already exist!\n')
else:                  
    datacount = 1
    print('creating dataset...\n')

#building train/val/test datastructure, check if the directory already exist

train_path = os.path.join(target_dir, 'train')
train_img_path = os.path.join(train_path, 'images')
train_label_path = os.path.join(train_path, 'labels')
val_path = os.path.join(target_dir, 'val')
val_img_path = os.path.join(val_path, 'images')
val_label_path = os.path.join(val_path, 'labels')
test_path = os.path.join(target_dir, 'test')
test_img_path = os.path.join(test_path, 'images')
test_label_path = os.path.join(test_path, 'labels')

if os.path.isdir(train_path):
    print('appending dataset...\n')
else:
    print('making directories...\n')
    os.mkdir(train_path)
    os.mkdir(train_img_path)
    os.mkdir(train_label_path)
    os.mkdir(val_path)
    os.mkdir(val_img_path)
    os.mkdir(val_label_path)
    os.mkdir(test_path)
    os.mkdir(test_img_path)
    os.mkdir(test_label_path)


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
print(f'inserting {n_samples} files...\n')

for fil in xml_paths:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    print(filename)
    filename_nochinese = re.sub("[\u4e00-\u9fa5]", "", filename)
    jpgname = os.path.splitext(fil)[0]
    jpgpath = os.path.join(f"{jpgname}.jpg")

    
    # check if the label contains the corresponding image file
    if not os.path.exists(jpgpath):
        print(f"{filename} image does not exist!")
        continue
    else:
        if counter/n_samples < split[0]:
            shutil.copy(os.path.join(jpgpath), os.path.join(train_img_path, f'{filename_nochinese}.jpg'))
        elif  split[0] <= counter/n_samples < (split[0]+split[1]):
            shutil.copy(os.path.join(jpgpath), os.path.join(val_img_path, f'{filename_nochinese}.jpg'))
        elif counter/n_samples >= (split[0]+split[1]):
            shutil.copy(os.path.join(jpgpath), os.path.join(test_img_path, f'{filename_nochinese}.jpg'))
            
    result = []

    # parse the content of the xml file
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        label = obj.find("name").text
        # check for new classes and append to list
        if label not in classes:
            #classes.append(label)
            continue
        else:
            index = classes.index(label)
            pil_bbox = [int(x.text) for x in obj.find("bndbox")]
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([f"{x}" for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

    if result:
        # generate a YOLO format text file for each xml file
        if counter/n_samples < split[0]:
            with open(os.path.join(train_label_path, f"{filename_nochinese}.txt"), "w+", encoding="utf-8") as f:
                f.write("\n".join(result))
        elif  split[0] <= counter/n_samples < (split[0]+split[1]):
            with open(os.path.join(val_label_path, f"{filename_nochinese}.txt"), "w+", encoding="utf-8") as f:
                f.write("\n".join(result))
        elif counter/n_samples >= (split[0]+split[1]):
            with open(os.path.join(test_label_path, f"{filename_nochinese}.txt"), "w+", encoding="utf-8") as f:
                f.write("\n".join(result))
    counter = counter +1
    datacount = datacount + 1
    
with open(os.path.join(target_dir, 'classes.txt'), 'w+', encoding='utf8') as f:
    f.write(json.dumps(classes))

with open(os.path.join(target_dir, 'datacount.txt'), 'w+', encoding='utf8') as f:
    f.write(json.dumps(datacount))
    
print('finished!\n')
print('dataset now contain', datacount-1, 'images')

