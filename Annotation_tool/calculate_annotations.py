import xml.etree.ElementTree as ET
import os
import shutil
from collections import Counter
from shutil import copy
from os import walk
from os.path import join

'''
This script can be use to calculate annotation instances of a folder and all of its subfolder
It create a temp directory, at each iteration move some xmls to a temp directory then calculate the instances 
Print the calculation report in console
'''


print('This script would calculate annonations in the input folder, also all sub folders of the input folder\n')

path = input("Please enter input folder path:\n")

#Build temp directory
os.mkdir("ajsildjiglajsiwqiovzsjlleivjsbafczwjwioj")
current_path = os.getcwd()
to_path = os.path.join( current_path,"ajsildjiglajsiwqiovzsjlleivjsbafczwjwioj")

print('calculating all the annonations in the input folder...')

#Clean temp directory
shutil.rmtree(to_path)
os.mkdir(to_path)

#in different cases, you can use different class definition
classes = ["total","person", "car", "motorbike", "bus", "truck", "bike", "Normal", "Fall", "not_clear"]

objects = []
    
labels = []

finished = True


#read all xml content in a directory
def read_content(xml_file: str):
    global finished

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
           print(filename, xmin, ymin, xmax, ymax, area)
           finished = False
           break
        labels.append("total")

        
#perform a os walk in the main directory
for root, dirs, files in walk(path):
  for f in files:
    fullpath = join(root, f)

    ming=os.path.splitext (fullpath)
    str=ming[1]
    if str==".xml":
        from_path = os.path.join(path, fullpath)
        copy(from_path,to_path)

files = os.listdir(to_path)
for f in files:
    fullpath = os.path.join(to_path, f)
    read_content(fullpath)
if finished:

    print('----Annonations in input folder:\n')
    print('    ',Counter(labels),'\n')
    shutil.rmtree(to_path)
    os.mkdir(to_path)
    labels=[]

print('Calcuating sub folder annonations...\n\n')

#perform a os walk in sub dirs
for root, dirs, files in walk(path):

  for d in dirs:
    dirpath = join(root,d)

    for root2, dirs2, files2 in walk(dirpath):
      for f in files2:

        fullpath = join(root2, f)
        ming=os.path.splitext (fullpath)
        str=ming[1]
        if str==".xml":
            from_path = os.path.join(fullpath)
            copy(from_path,to_path)

    files3 = os.listdir(to_path)
    for f in files3:

      readpath = os.path.join(to_path, f)

      if os.path.isfile(readpath):

          read_content(readpath)
      elif os.path.isdir(readpath):
        continue

    if finished:
      if Counter(labels)==Counter():
        pass
      else:
        print('----Sub folder data path:\n','    ',dirpath)
        print('----Sub folder annonations:\n\n','    ',Counter(labels))
        print('\n')
        labels=[]
        shutil.rmtree(to_path)
        os.mkdir(to_path)


#remove temp dir
shutil.rmtree(to_path)
print('all the folders has been calculated\n')


