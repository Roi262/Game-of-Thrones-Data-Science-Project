import csv
from os import listdir
from os.path import isfile, join

"""
Create a CSV of episode number to episode name
"""

mypath = "C:\\Users\\Tamar 2\\Dropbox\\uni\\מחט\\final project\\data\\GoT srt files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
prev = " "
with open("list-of-eps.csv", "w") as o:
    w = csv.writer(o)
    for p in onlyfiles:
        s, ep = p.split(" - ")[1].split("x")
        name = p.split(" - ")[2].split('.')[0]
        if ep != prev:
            w.writerow([s, ep, name])
        prev = ep

