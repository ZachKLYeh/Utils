import os
import cv2
import xml.etree.cElementTree as ET
import numpy as np

'''
This script can help generating visualized result of annotations. This is simply for PM or supervisors to 
see you labeling result rather than installing labelimg.
'''
 
input_path = input("please enter input folder:\n")

visualized_path = input("please enter visualized folder:\n")

_COLORS = np.array(
    [
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098,
        0.929, 0.694, 0.125,
        0.494, 0.184, 0.556,
        0.466, 0.674, 0.188,
        0.301, 0.745, 0.933,
    ]
).astype(np.float32).reshape(-1, 3)

CLASSES = [
    "person", 
    "car", 
    "motorbike", 
    "bus", 
    "truck", 
    "bike"
]

filelist = os.listdir(input_path)
for f in filelist:
	filename, fileformat = os.path.splitext(f)
	img_path = os.path.join(input_path, filename+'.jpg')
	xml_path = os.path.join(input_path, filename+'.xml')
	img = cv2.imdecode(np.fromfile(os.path.join(input_path, f), dtype=np.uint8), -1)
	if img is None:
		continue
	print(img_path)
	
	tree = ET.parse(xml_path)
	root = tree.getroot()
    
	for items in root.iter('object'):
		name = items.find("name").text
		ymin = int(items.find("bndbox/ymin").text)
		xmin = int(items.find("bndbox/xmin").text)
		ymax = int(items.find("bndbox/ymax").text)
		xmax = int(items.find("bndbox/xmax").text)

		for id in range(6):
			if CLASSES[id] == name:
				cls_id = id

		color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()
		text = '{}'.format(CLASSES[cls_id])
		txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
		font = cv2.FONT_HERSHEY_SIMPLEX

		txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
		cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)

		txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()
		cv2.rectangle(
		    img,
		    (xmin, ymin + 1),
		    (xmin + txt_size[0] + 1, ymin + int(1.5*txt_size[1])),
		    txt_bk_color,
		    -1
		)
		cv2.putText(img, text, (xmin, ymin + txt_size[1]), font, 0.4, txt_color, thickness=1)
		
	flag=0
	flag=cv2.imencode('.jpg', img)[1].tofile(os.path.join(visualized_path,filename+'.jpg'))
	if(flag):
		print(filename,"done")
print("all done ====================================")