import os

'''
This script helps find the missing xml file or missing jpg file of a dataset.
This can be extremely annoying for labelers. 
With this script, you can simply enter the input folder.
And it will print which image or annotaton is missing
'''
input_dir = input("please enter the dir path:\n")

file_list = os.listdir(input_dir)

for f in file_list:
	filename, fileformat = os.path.splitext(f)
	img_path = os.path.join(input_dir, filename+".jpg")
	xml_path = os.path.join(input_dir, filename+".xml")
	if os.path.exists(img_path) & os.path.exists(xml_path):
		pass
	else:
		print(f)