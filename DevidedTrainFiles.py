import glob
import os
import random
import shutil

def rand_ints_nodup(start, end, number):
  ns = []
  while len(ns) < number:
    n = random.randint(start, end)
    if not n in ns:
      ns.append(n)
  return ns

def replace_specialchar_to_underbar(str_path):
    str_path = str_path.replace('-', '_')
    str_path = str_path.replace('.', '_')
    return str_path

def main():
    serch_folder_name = ""
    path = F"./*/{serch_folder_name}"
    insert_folder_names = ("valid", "train")
    file_path_lists = glob.glob("{}/**".format(path), recursive=True)
    list_jpg_file_name = []
    list_jpg_file_path = []
    list_txt_file_path = []

    for file_path in file_path_lists:
        if (os.path.isfile(file_path)):
            base_dir, file_name = os.path.split(file_path)
            file_without_ext, ext = os.path.splitext(file_name)
            if (ext == ".jpg"):
                list_jpg_file_name.append(file_without_ext)
                list_jpg_file_path.append(file_path)
            elif (ext == ".txt"):
                list_txt_file_path.append(file_path)

    print(F"Count_JPG : {len(list_jpg_file_path)}")
    print(F"Count_TXT : {len(list_txt_file_path)}")

    if(not(len(list_jpg_file_path)==len(list_txt_file_path))):
        print("Matching_Error")
        return -1

    list_jpg_file_name.sort()
    list_jpg_file_path.sort()
    list_txt_file_path.sort()

    list_jpg_file_name = list(map(replace_specialchar_to_underbar, list_jpg_file_name))

    valid_list_number = sorted(rand_ints_nodup(0, len(list_jpg_file_path), int(len(list_jpg_file_path) * 0.2)))
    print(len(valid_list_number))
    print(valid_list_number)

    for insert_folder_name in insert_folder_names:
        if not(os.path.exists(F"./{insert_folder_name}/")):
            os.mkdir(F"./{insert_folder_name}/")
        if not(os.path.exists(F"./{insert_folder_name}/images/")):
            os.mkdir(F"./{insert_folder_name}/images/")
        if not(os.path.exists(F"./{insert_folder_name}/labels/")):
            os.mkdir(F"./{insert_folder_name}/labels/")

    for num in range(len(list_jpg_file_path)):
        if num in valid_list_number:
            shutil.copy2(list_jpg_file_path[num], F"./{insert_folder_names[0]}/images/{list_jpg_file_name[num]}.jpg")
            shutil.copy2(list_txt_file_path[num], F"./{insert_folder_names[0]}/labels/{list_jpg_file_name[num]}.txt")
            print(list_jpg_file_path[num])
            print(list_txt_file_path[num])
            print(list_jpg_file_name[num])
        else:
            shutil.copy2(list_jpg_file_path[num], F"./{insert_folder_names[1]}/images/{list_jpg_file_name[num]}.jpg")
            shutil.copy2(list_txt_file_path[num], F"./{insert_folder_names[1]}/labels/{list_jpg_file_name[num]}.txt")

    return 0

if __name__ == "__main__": 
    main()