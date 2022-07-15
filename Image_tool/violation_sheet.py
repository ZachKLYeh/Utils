#Note: This script should be run in python3.6

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

'''
This script creates a violation script by several images and descriptions
'''

print("please enter input folder path:")
folder = input(r"")
violation = input("請輸入違規描述第一行:\n")
violation2 = input("請輸入違規描述第二行:\n")
print('請輸入車牌座標:(格式:x1 x2 y1 y2)')
coordinates = input("")
numbers = list(map(int, coordinates.split()))
print("開始合成圖片...")

img_list = []
for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder,filename))
    if img is not None:
        img_list.append(img)

h, w, c = img_list[0].shape

image3_crop = cv2.resize(img_list[3][numbers[2]:numbers[3], numbers[0]:numbers[1], :], dsize=(w, h))
image3_rect = cv2.rectangle(img_list[3], (numbers[0], numbers[2]), (numbers[1], numbers[3]), (0, 255, 0),10)
image3_large_rect = cv2.resize(image3_rect, dsize=(w*2, h*2))

base_array = np.concatenate([img_list[0], img_list[1]], axis=0)
base_array = np.concatenate([base_array, image3_large_rect], axis=1)
base_array2 = np.concatenate([img_list[2], img_list[3]], axis=1)
base_array2 = np.concatenate([base_array2, image3_crop], axis=1)
total_base_array = np.concatenate([base_array, base_array2], axis=0)

total_base_img_resized = cv2.resize(total_base_array, dsize=(w,h))

init_coordinate = 15
append = 150
font_size = 55
line_distance = 5

final_base_array = np.zeros((h+append, w, c), dtype = np.uint8)
final_base_array[append:h+append,:,:] = total_base_img_resized

imageRGB = cv2.cvtColor(final_base_array, cv2.COLOR_BGR2RGB)
final_img = Image.fromarray(imageRGB, 'RGB')
title_font = ImageFont.truetype('SimSun.ttf', font_size)
image_editable = ImageDraw.Draw(final_img)
image_editable.text((init_coordinate,init_coordinate), violation, (255, 255, 0), font=title_font)
image_editable.text((init_coordinate,init_coordinate+font_size+line_distance), violation2, (255, 255, 0), font=title_font)

print("\n圖片合成完成,即將彈出窗口")

plt.imshow(final_img)
plt.show()
final_img.show()

