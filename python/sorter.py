import argparse
from datetime import datetime
from distutils.file_util import move_file
from genericpath import exists, isfile
import os

def create_if_not_exists(path):
    if (not os.path.exists(path)):
        print("Creating folder: " + path)
        os.mkdir(path)

def main():
    parser = argparse.ArgumentParser(description='Organize pictures into dated folders')
    parser.add_argument('path', help='Location of images to organize.')
    args = parser.parse_args()
    path = args.path[:-1]
    for file in os.listdir(path):
        file_path = path + "\\" + file
        if (isfile(file_path)):
            creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
            year_path = path + "\\" + str(creation_date.year)
            month_path = year_path + "\\" + str(creation_date.month).zfill(2)
            target_path = month_path + "\\" + file
            create_if_not_exists(year_path)
            create_if_not_exists(month_path)
            move_file(file_path, target_path)
            
    return

if __name__ == '__main__':
    main()