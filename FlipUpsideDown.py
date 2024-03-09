import glob
import os
from PIL import Image

input_folder = "RS/"
jpgfiles = glob.glob(F"./images/{input_folder}*.jpg")

foloder_number = ""
savedirname = "2/TD/"
if not(os.path.exists(F"./images/{foloder_number}/{savedirname}")):
    os.mkdir(F"./images/{foloder_number}/{savedirname}")
if not(os.path.exists(F"./labels/{foloder_number}/{savedirname}")):
    os.mkdir(F"./labels/{foloder_number}/{savedirname}")

for f in jpgfiles:
    (dirname, filename) = os.path.split(f)
    (name,ext) = os.path.splitext(filename)

    new_img = savedirname + "TD_" + filename
    new_txt = savedirname + "TD_" + name + ".txt"

    img = Image.open(f)
    imgLR = img.transpose(Image.FLIP_TOP_BOTTOM)
    imgLR.save(F"images/{foloder_number}/{new_img}")

    txt_file = open(F"./labels/{input_folder}/{name}.txt", "r")
    lines = txt_file.read().replace("\r\n","\n").split('\n')

    txt_outfile = open(F"./labels/{foloder_number}/{new_txt}", "w")

    for line in lines:
        if(line != ""):
            elems = line.split(" ")
            txt_outfile.write(elems[0] + " " + elems[1] + " " + str(1-float(elems[2])) + " " + elems[3] + " " + elems[4] + '\n')