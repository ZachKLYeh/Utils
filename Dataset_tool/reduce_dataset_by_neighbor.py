import xml.etree.ElementTree as ET
import os
import shutil
import random

input_dir = input("Please enter input folder path:\n")
output_dir = input("Please enter output folder path:\n")

#in different cases, you can use different class definition
classes = ["person", "car", "motorbike", "bus", "truck", "bike"]
sensitive_classes = ["bus", "truck", "bike", "person"]
extreme_sensitive_classes = ["bus", "truck", "", ""]

#read a xml file then append labels
def read_content(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    objects = []

    for items in root.iter('object'):
        name = items.find("name").text
        objects.append(name)

    return objects

#compare two xml file and decide which to discard
def compare(xml1, xml2, input_dir = input_dir):
    xml1_objects = read_content(os.path.join(input_dir, xml1))
    xml2_objects = read_content(os.path.join(input_dir, xml2))
    print(f"compair {xml1} vs {xml2}")
    #detect which xml has more label on sensitive classes(which is lacked)
    for i in range(len(sensitive_classes)):
        if xml1_objects.count(extreme_sensitive_classes[i])>0 and xml1_objects.count(extreme_sensitive_classes[i])>0:
            print(f'both xmls are kept because they all have very sensitive classes')
            return "none"
        elif xml1_objects.count(sensitive_classes[i]) > xml2_objects.count(sensitive_classes[i]):
            print(f"discard {xml2} due to", sensitive_classes[i])
            return xml2
            break
        elif xml1_objects.count(sensitive_classes[i]) < xml2_objects.count(sensitive_classes[i]):
            print(f"discard {xml1} due to", sensitive_classes[i])
            return xml1
            break
    #if the sensitive classes are the same, then compair label instances
    if len(xml1_objects) > len(xml2_objects):
        print(f"discard {xml2} due to label instance")
        return xml2
    elif len(xml1_objects) < len(xml2_objects):
        print(f"discard {xml1} due to label instance")
        return xml1
    #if the label instances are the same, shows that they are extremely smilar, random discard one
    else:
        out = random.choice([xml1, xml2])
        print(f"discard random {out} due to they are smiliar")
        return out


        
#scan the directory
file_list = os.listdir(input_dir)

#get xml list
xml_list = []
for file in file_list:
    filename, fileformat = os.path.splitext(file)
    if fileformat == ".xml":
        xml_list.append(file)

#create a reduced xml_list for deletion
reduced_xml_list = xml_list

i = 0
loop_finished = False

while(loop_finished == False):
    if 0 < int(reduced_xml_list[i+1][-7:-4]) - int(reduced_xml_list[i][-7:-4]) <= 2:
        print('distance',int(reduced_xml_list[i+1][-7:-4]) - int(reduced_xml_list[i][-7:-4]), end= ':')
        discard_xml = compare(reduced_xml_list[i+1], reduced_xml_list[i])
        print("\n")
        if discard_xml == "none":
            i += 1
        else:
            reduced_xml_list.remove(discard_xml)
    else:
        i += 1

    try:
        int(reduced_xml_list[i+1][-7:-4]) - int(reduced_xml_list[i][-7:-4])
    except:
        loop_finished = True

print(len(reduced_xml_list), "are selected")
print("moving files...")

for i in range(len(reduced_xml_list)):
    filename, _ = os.path.splitext(reduced_xml_list[i])
    img_source = os.path.join(input_dir, filename+".jpg")
    img_target = os.path.join(output_dir, filename+".jpg")
    xml_source = os.path.join(input_dir, reduced_xml_list[i])
    xml_target = os.path.join(output_dir, reduced_xml_list[i])
    shutil.copy(img_source, img_target)
    shutil.copy(xml_source, xml_target)


        



