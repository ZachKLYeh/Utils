import xml.etree.ElementTree as ET
import os
import shutil
from collections import Counter
from shutil import copy

'''
This script manage to reduce redundant data from the dataset
stragies:
1. Only keep images contain lacked classes(ex. truck bus bike person)
2. Select only one frame from countinous several frames
3. Use model to predict dataset(using 0.5 confidence threshold)
   find objects that is predicted as 0.5-0.6 confidence
'''

input_dir = input("Please enter input folder path:\n")
output_dir = input("Please enter output folder path:\n")

#in different cases, you can use different class definition
classes = ["total","person", "car", "motorbike", "bus", "truck", "bike"]
finished = True

#read a xml file then append labels
def read_content(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    filename = root.find('filename').text
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)

    objects = []

    for items in root.iter('object'):
        
        name = items.find("name").text
        objects.append(name)
        
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

        if(xmin < 0 or xmin > width or ymin < 0 or ymin > height or
           xmax <= 0 or xmax > width or ymax <= 0 or ymax > height or
           area < 100):
           print(filename, xmin, ymin, xmax, ymax, area)
           finished = False
           break

    return objects

        
#perform a os walk in the main directory
file_list = os.listdir(input_dir)
reduced_list = file_list
counter = 0
move_counter = 0

for file in file_list:
  filepath = os.path.join(input_dir, file)
  filename, fileformat = os.path.splitext(file)
  counter += 1
  if fileformat==".xml":
      objs = read_content(filepath)
      img_path = os.path.join(input_dir, filename+".jpg")
      img_target = os.path.join(output_dir, filename+".jpg")
      xml_path = filepath
      xml_target = os.path.join(output_dir, file)
      if ("truck" in objs) or ("bus" in objs) or ("person" in objs) or ("bike" in objs):
        shutil.copy(img_path, img_target)
        shutil.copy(xml_path, xml_target)
        move_counter += 1
        
print(counter, "images are scanned")
print(move_counter, 'images are moved')



