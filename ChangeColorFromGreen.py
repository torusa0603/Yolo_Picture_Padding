import glob
import os
import shutil
from PIL import Image
import numpy as np
import random
import cv2

type_color = ""
input_folder = "2/TD/"
jpgfiles = glob.glob(F"./images/{input_folder}*.jpg")

foloder_number = ""
savedirname = "3/CC/"
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
b_debug_flag = False
if not(os.path.exists(F"./images/{foloder_number}/{savedirname}")):
    os.mkdir(F"./images/{foloder_number}/{savedirname}")
if not(os.path.exists(F"./labels/{foloder_number}/{savedirname}")):
    os.mkdir(F"./labels/{foloder_number}/{savedirname}")

for f in jpgfiles:
    (dirname, filename) = os.path.split(f)
    (name,ext) = os.path.splitext(filename)

    
    new_img_chcolor = savedirname + F"chcolor_{type_color}" + filename
    new_img_diff_chcolor = savedirname + "chcolor_diff_" + filename
    new_img_diff__sobel_chcolor = savedirname + "chcolor_diff_sobel_" + filename
    new_img_diff__mask_chcolor = savedirname + "chcolor_diff_mask_" + filename

    new_txt_chcolor = savedirname + F"chcolor_{type_color}" + name + ".txt"

    img_ori = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    #print(img.shape)
    #print(img[0])
    img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    #print(img_hsv[0])
    #print(img_hsv.shape)
    
    if (type_color == ""):
        img_list_random_hsv = [[(random.randrange(180), random.randrange(256), random.randrange(256)) if ((pix[0] > 30) and (pix[0] < 80) and (pix[1] > 50)) else pix for pix in colum] for colum in img_hsv]
    elif (type_color == "red_"):
        img_list_random_hsv = [[(random.randrange(0, 15, 1), random.randrange(256), random.randrange(256)) if ((pix[0] > 30) and (pix[0] < 80) and (pix[1] > 50)) else pix for pix in colum] for colum in img_hsv]
    elif (type_color == "blue_"):
        img_list_random_hsv = [[(random.randrange(90, 130, 1), random.randrange(256), random.randrange(256)) if ((pix[0] > 30) and (pix[0] < 80) and (pix[1] > 50)) else pix for pix in colum] for colum in img_hsv]
    elif (type_color == "yellow_"):
        img_list_random_hsv = [[(random.randrange(20, 25, 1), random.randrange(256), random.randrange(256)) if ((pix[0] > 30) and (pix[0] < 80) and (pix[1] > 50)) else pix for pix in colum] for colum in img_hsv]
    
    img_numpy_random_hsv = np.array(img_list_random_hsv)
    #print(img_numpy_random_hsv[0])
    #print(img_numpy_random_hsv.shape)
    img_numpy_random_bgr = cv2.cvtColor(img_numpy_random_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    if b_debug_flag:
        img_diff = cv2.absdiff(img_ori, img_numpy_random_bgr)
        img_diff_gray = cv2.cvtColor(img_diff, cv2.COLOR_BGR2GRAY)
        img_diff_gray = 255 - img_diff_gray
        img_diff_average = cv2.blur(img_diff_gray, (3,3))
        img_diff_average = cv2.blur(img_diff_average, (3,3))
        ret, img_thresh = cv2.threshold(img_diff_average, 250, 255, cv2.THRESH_BINARY)

        img_thresh_closing = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        img_diff_thresh_closing = cv2.morphologyEx(img_thresh_closing, cv2.MORPH_CLOSE, kernel, iterations=3)
        img_diff_thresh_closing_rgb = cv2.cvtColor(img_diff_thresh_closing, cv2.COLOR_GRAY2BGR)
        img_diff_thresh_closing_rgb_mask = img_diff_thresh_closing_rgb / 255
        img_ori_mask = img_ori * img_diff_thresh_closing_rgb_mask

        img_diff_sobel = cv2.Sobel(src=img_thresh, ddepth=cv2.CV_32F,dx=1,dy=1,ksize=1)
        img_diff_sobel_closing = cv2.morphologyEx(img_diff_sobel, cv2.MORPH_CLOSE, kernel, iterations=3)
        img_list_diff_sobel_closing__rgb = [[(0, 0, 0) if (pix == 0) else (0, 0, 255) for pix in colum] for colum in img_diff_sobel_closing]
        img_numpy_diff_sobel_closing_rgb = np.array(img_list_diff_sobel_closing__rgb)
        img_numpy_diff_sobel_closing_mask_rgb = cv2.cvtColor(img_diff_sobel_closing, cv2.COLOR_GRAY2BGR)
        img_numpy_diff_sobel_closing_mask_bin = img_numpy_diff_sobel_closing_mask_rgb / 255
        img_ori_cut = img_ori * (1 - img_numpy_diff_sobel_closing_mask_bin)
        img_append_edge = img_ori_cut + img_numpy_diff_sobel_closing_rgb

        cv2.imwrite(F"images/{foloder_number}/" + new_img_diff_chcolor, img_diff)
        cv2.imwrite(F"images/{foloder_number}/" + new_img_diff__mask_chcolor, img_ori_mask)
        cv2.imwrite(F"images/{foloder_number}/" + new_img_diff__sobel_chcolor, img_append_edge)
    
    cv2.imwrite(F"images/{foloder_number}/" + new_img_chcolor, img_numpy_random_bgr)

    shutil.copy(F"./labels/{input_folder}/{name}.txt", F"./labels/{foloder_number}/{new_txt_chcolor}")
    