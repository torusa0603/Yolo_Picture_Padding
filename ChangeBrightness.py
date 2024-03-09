import glob
import os
import shutil
from PIL import Image
from PIL import ImageEnhance

input_folder = ""
jpgfiles = glob.glob(F"./images/{input_folder}*.jpg")

foloder_number = ""
savedirname = "CB/"
if not(os.path.exists(F"./images/{foloder_number}/{savedirname}")):
    os.mkdir(F"./images/{foloder_number}/{savedirname}")
if not(os.path.exists(F"./labels/{foloder_number}/{savedirname}")):
    os.mkdir(F"./labels/{foloder_number}/{savedirname}")

for f in jpgfiles:
    (dirname, filename) = os.path.split(f)
    (name,ext) = os.path.splitext(filename)

    new_img_bright = savedirname + "bright_" + filename
    new_img_dark = savedirname +  "dark_" + filename

    new_txt_bright = savedirname + "bright_" + name + ".txt"
    new_txt_dark = savedirname + "dark_" + name + ".txt"

    img = Image.open(f)
    eim = ImageEnhance.Brightness(img)

    eim.enhance(1.6).save(F"images/{foloder_number}/" + new_img_bright)
    eim.enhance(0.6).save(F"images/{foloder_number}/" + new_img_dark)

    shutil.copy(F"./labels/{input_folder}/{name}.txt", F"./labels/{foloder_number}/{new_txt_bright}")
    shutil.copy(F"./labels/{input_folder}/{name}.txt", F"./labels/{foloder_number}/{new_txt_dark}")