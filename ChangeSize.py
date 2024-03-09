import glob
import os
import shutil
from PIL import Image

input_folder = ""
jpgfiles = glob.glob(F"./images/{input_folder}*.jpg")

foloder_number = ""
savedirname = "RS/"
magnification_large = 1.2
magnification_small = 0.8
if not(os.path.exists(F"./images/{foloder_number}/{savedirname}")):
    os.mkdir(F"./images/{foloder_number}/{savedirname}")
if not(os.path.exists(F"./labels/{foloder_number}/{savedirname}")):
    os.mkdir(F"./labels/{foloder_number}/{savedirname}")


for f in jpgfiles:
    (dirname, filename) = os.path.split(f)
    (name,ext) = os.path.splitext(filename)

    new_img_large = savedirname + F"resize_{int(magnification_large * 10):02}_" + filename
    new_img_small = savedirname + F"resize_{int(magnification_small * 10):02}_" + filename
    new_txt_large = savedirname + F"resize_{int(magnification_large * 10):02}_" + name + ".txt"
    new_txt_small = savedirname + F"resize_{int(magnification_small * 10):02}_" + name + ".txt"

    img = Image.open(f)
    img_resize_large = img.resize((int(img.width * magnification_large), int(img.height * magnification_large)))
    img_resize_small = img.resize((int(img.width * magnification_small), int(img.height * magnification_small)))
    img_resize_large.save(F"images/{foloder_number}/{new_img_large}")
    img_resize_small.save(F"images/{foloder_number}/{new_img_small}")

    shutil.copy(F"./labels/{input_folder}/{name}.txt", F"./labels/{foloder_number}/{new_txt_large}")
    shutil.copy(F"./labels/{input_folder}/{name}.txt", F"./labels/{foloder_number}/{new_txt_small}")