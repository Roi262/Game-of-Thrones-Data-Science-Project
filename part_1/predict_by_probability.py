from collections import defaultdict
import csv
import numpy as np
from random import choice

kaggle_file = "/cs/usr/tamar.yov/Desktop/final_project/" \
              "Data-Science---Final-Project/data/Game of Thrones/kaggle_cleaned.csv"
TOP_CHARACTERS_AMOUNT = 30


def find_top_characters(reader):
    speaker_counter = defaultdict(int)
    for line in reader:
        if line:
            speaker = line[2]
            line = line[3].split(" ")
            speaker_counter[speaker] += len(line)

    top = [(e[0], e[1]) for e in sorted(speaker_counter.items(), key=lambda x:x[1], reverse=True)]
    return top


def get_vase():
    with open(kaggle_file, 'r') as k:
        reader = csv.reader(k, delimiter=';')
        counts = np.asarray([int(t[1]) for t in find_top_characters(reader)])
        total = np.sum(counts)
        vase = []
        for ind in range(30):
            for _ in range(counts[ind]):
                vase.append(ind)
        return vase


vase = get_vase()
accuracy = []
for epoch in range(100):
    successes = 0
    for _ in range(10000):
        speaker = choice(vase)
        prediction = choice(vase)
        if speaker == prediction:
            successes += 1
    accuracy.append(successes / 100)

print(str(sum(accuracy)/100))
