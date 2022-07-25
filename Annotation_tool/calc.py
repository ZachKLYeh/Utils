import xml.etree.ElementTree as ET
import os
import shutil
from collections import Counter
from shutil import copy
from os import walk
from os.path import join

#input path and temp path
input_dir_path = input("\n> Please enter input folder path:\n")
temp_dir = os.path.join("temp_dir_for_xml_calculation")
temp_dir_path = os.path.join(os.getcwd(), temp_dir)

#
line = "--------------------------------------------------------------------------------------------"

#Build temp directory
try:
  shutil.rmtree(temp_dir_path)
  os.mkdir(temp_dir_path)
except:
  os.mkdir(temp_dir_path)

print('\n> Calculating all the label instances in the input folder...\n')

#in different cases, you can use different class definition
classes = ["total","person", "car", "motorbike", "bus", "truck", "bike", "Normal", "Fall", "not_clear"]
objects = []
labels = []
duplicate = 0
dirpath = ""
finished = True

#read all xml content in a directory
def read_content(xml_file: str, dirpath):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    list_with_all_boxes = []

    filename = root.find('filename').text
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)

    for items in root.iter('object'):

        name = items.find("name").text

        if name not in classes:

            print(filename, name, "Not in classes")
            finished = False

            break

        ymin, xmin, ymax, xmax = None, None, None, None
        ymin = int(items.find("bndbox/ymin").text)
        xmin = int(items.find("bndbox/xmin").text)
        ymax = int(items.find("bndbox/ymax").text)
        xmax = int(items.find("bndbox/xmax").text)

        area = (xmax - xmin) * (ymax - ymin)
        labels.append(name)

        if(xmin < 0 or xmin > width or ymin < 0 or ymin > height or
           xmax <= 0 or xmax > width or ymax <= 0 or ymax > height or
           area < 100):

           print('a label has invalid format')
           print(dirpath+'\\', filename, xmin, ymin, xmax, ymax, area)

           break

        labels.append("total")

        
#perform a os walk in the main directory
for root, dirs, files in walk(input_dir_path):

  for f in files:

    fullpath = join(root, f)
    filename, fileformat = os.path.splitext(f)

    if fileformat==".xml":

        src_path = os.path.join(input_dir_path, fullpath)

        if os.path.exists(os.path.join(temp_dir_path, f)):

          duplicated_temp_path = os.path.join(temp_dir_path, f"{filename}_{duplicate}{fileformat}")
          duplicate+=1
          copy(src_path,duplicated_temp_path)

        else:

          copy(src_path, temp_dir_path)

files = os.listdir(temp_dir_path)

for f in files:

    fullpath = os.path.join(temp_dir_path, f)
    read_content(fullpath, dirpath)

if finished:

    print(line)
    print('----input folder path:')
    print('      ', input_dir_path)
    print('----label instances:')
    print('      ',Counter(labels))
    print(line, '\n')

    shutil.rmtree(temp_dir_path)
    os.mkdir(temp_dir_path)
    labels=[]

print('> Calcuating each sub folder label instances...\n')
print(line)

#perform a os walk in sub dirs
for root, dirs, files in walk(input_dir_path):

  for d in dirs:

    dirpath = join(root, d)

    for root2, dirs2, files2 in walk(dirpath):

      for f in files2:

        fullpath = join(root2, f)
        filename,fileformat=os.path.splitext (f)

        if fileformat==".xml":

            src_path = os.path.join(fullpath)

            if os.path.exists(os.path.join(temp_dir_path, f)):

              duplicated_temp_path = os.path.join(temp_dir_path,f"{filename}_{duplicate}{fileformat}")
              duplicate+=1
              copy(src_path, duplicated_temp_path)

            else:

              copy(src_path, temp_dir_path)

    files3 = os.listdir(temp_dir_path)

    for f in files3:

      readpath = os.path.join(temp_dir_path, f)

      if os.path.isfile(readpath):

          read_content(readpath, dirpath)

      elif os.path.isdir(readpath):

        continue

    if finished:

      if Counter(labels)==Counter():

        pass

      else:

        print('----Sub folder data path:')
        print('      ', dirpath)
        print('----Sub folder label instances:')
        print('      ', Counter(labels))
        print(line)
        
        labels=[]
        shutil.rmtree(temp_dir_path)
        os.mkdir(temp_dir_path)

print("\n")

#remove temp dir
shutil.rmtree(temp_dir_path)
print('> All the folders has been counted\n')


