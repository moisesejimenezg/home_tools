import argparse
from datetime import datetime
from distutils.file_util import move_file
from genericpath import isfile
from hashlib import new
import os

class File:
    def __init__(self, filepath):
        #print("Processing: " + filepath)
        self.filepath = filepath
        self.name = self.__extract_name()
        self.size = self.__extract_size()
        self.valid_date = False
        self.creation_date_string = self.__extract_date()

    def __extract_name(self):
        parts = self.filepath.split("\\")
        name = parts[-1]
        #print("Name: " + name)
        return name
    def __extract_size(self):
        size = os.path.getsize(self.filepath)
        #print("Size: " + str(size))
        return size
    def __extract_date(self):
        if "IMG_" in self.name:
            parts = self.name.split("_")
            if len(parts) == 3:
                self.valid_date = True
                return parts[1]
        elif "IMG-" in self.name:
            parts = self.name.split("-")
            if len(parts) == 3:
                self.valid_date = True
                return parts[1]

def process_file_by_size(path, file, files):
    file_path = path + "\\" + file
    if (isfile(file_path)):
        size = os.path.getsize(file_path)
        key = file + str(size)
        if (key not in files):
            files[key] = [file_path]
        else:
            files[key].append(file_path)
    else:
        for child in os.listdir(file_path):
            files = process_file_by_size(file_path, child, files)
    return files

def strip_suffix(file, suffix):
    if (suffix in file):
        parts = file.split(suffix)
        return parts[0] + parts[1]

def process_file(path, file, files):
    file_path = path + "\\" + file
    if (isfile(file_path)):
        new_file = File(file_path)
        if (new_file.valid_date):
            key = new_file.name
            if (key not in files):
                files[key] = [new_file]
            else:
                files[key].append(new_file)
    else:
        for child in os.listdir(file_path):
            files = process_file(file_path, child, files)
    return files

def check_for_duplicates(files, destination_folder, move = False):
    duplicates = []
    for key, value in files.items():
        if (len(value) > 1):
            duplicates.append(value[0])
            print(key + " has " + str(len(value)) + " duplicates.")
            for file in value:
                print(value)
                if "google backup" in file:
                    if (move):
                        filename = file.split("\\")[-1]
                        target = destination_folder + "\\" + filename
                        move_file(file, target)
                        print("Moved: " + file)
                        print("To: " + target)
    print("Found " + str(len(duplicates)) + " duplicates.")

def delete_suffixed(files, suffix, remove = False):
    duplicates = []
    for key, value in files.items():
        if (len(value) > 1):
            duplicates.append(value[0])
            print(key + " has " + str(len(value)) + " duplicates.")
            print(value)
            for file in value:
                if suffix in file:
                    print("File to delete")
                    print(file)
                    if (remove):
                        os.remove(file)
    print("Found " + str(len(duplicates)) + " duplicates.")

def process_duplicates(files, target):
    for values in files:
        if len(values) == 2:
            if values[0].size >= values[1].size:
                move_file(values[0].filepath, target)
                os.remove(values[1].filepath)
            else:
                move_file(values[1].filepath, target)
                os.remove(values[0].filepath)

def main():
    parser = argparse.ArgumentParser(description='Organize pictures into dated folders')
    parser.add_argument('path', help='Location of images to organize.')
    args = parser.parse_args()
    path = args.path
    files = {}
    for file in os.listdir(path):
        files = process_file(path, file, files)
    duplicates = []
    for key, values in files.items():
        if len(values) > 1:
            duplicates.append(values)
    print("Found " + str(len(duplicates)) + " duplicates.")
    process_duplicates(duplicates, path + "\\unsorted")
    return

if __name__ == '__main__':
    main()