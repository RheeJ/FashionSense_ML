import sys
import numpy
import csv
import os
import shutil

filename = "int_data.csv"
images = "images"
formal_path = "formal"
not_formal = "not_formal"

with open(filename, 'rb') as csvfile:
    array = []
    i = 0
    for line in csv.reader(csvfile, dialect="excel"):
        if i < 200:
            line = map(int, line)
            array.append(line[26])
            i += 1

i = 0
path = 'images/'
for file in os.listdir(images):
    print file
    src = path + file
    if array[i] == 1:
        shutil.copyfile(src, 'formal/' + file)
    else:
        shutil.copyfile(src, 'not_formal/' + file)
    i += 1