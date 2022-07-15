import numpy as np
import os
import cv2

"""
This script is used to compare detection result of different model on same set of images
For example, I trained model 1 and model 2 to detect image set 1
then use the detect.py in yolov5 to generate visualized detection result.
By using this script, we can concatenate two visualized images(But then must have same file name)
So we can easily see the difference between different models
"""

input_path1 = input("please enter No.1 input folder:\n")
input_path2 = input("please enter No.2 input folder:\n")

output_path = input("please enter output path:\n")


files = os.listdir(input_path1)

for f in files:
	img_path1 = os.path.join(input_path1, f)
	img_path2 = os.path.join(input_path2, f)
	
	img1 = cv2.imdecode(np.fromfile(img_path1, dtype=np.uint8), -1)
	img2 = cv2.imdecode(np.fromfile(img_path2, dtype=np.uint8), -1)

	outimg = np.concatenate([img1, img2], axis=0)
	#outimg = cv2.cvtColor(outimg, cv2.COLOR_BGR2RGB)

	outimg_path = os.path.join(output_path, f)

	cv2.imencode('.jpg', outimg)[1].tofile(outimg_path)
	print(f)