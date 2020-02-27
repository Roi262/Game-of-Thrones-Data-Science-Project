import json
import csv
from os import listdir
from os.path import isfile, join
from fuzzywuzzy import fuzz, process

# tamars computer
scenes_json = "C:\\Users\\Tamar 2\\Dropbox\\uni\\מחט\\final project\\data\\GoT srt files\\scenes-timestamps.json"
# File with all scenes and their timestamps
kaggle_file = "C:\\Users\\Tamar 2\\Dropbox\\uni\\מחט\\final project\\data\\GoT srt files\\got_scripts_breakdown.csv"
# File from Kaggle, connects line to speaker

# rois computer
# scenes_json = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/scenes_timestamps.json"


clean_kaggle_f = "clean_kaggle_file.csv"


def create_scenes_timestamps_csv():
    """""Process the scenes json file - get relevant info into csv"""
    with open(scenes_json, 'r') as k, open("scenes_timestamps.csv", 'w') as outfile:
        w = csv.writer(outfile)
        data = json.load(k)
        for ep in data["episodes"]:
            s = ep["seasonNum"]
            epNum = ep["episodeNum"]
            scene_num = 0
            for scene in ep["scenes"]:
                start_ts = scene["sceneStart"]
                end_ts = scene["sceneEnd"]
                characters = scene["characters"]
                w.writerow([s, epNum, scene_num, start_ts, end_ts, characters])
                scene_num += 1


def cache_ep_names():
    output = {}
    with open("list_of_eps_with_names.csv", 'r') as names:
        line = names.readline()
        while line:
            line = line.lower().split(",")
            ep_name = line[2].split('\n')[0]
            output[ep_name] = (line[0], line[1])
            names.readline()
            line = names.readline()
    return output


def clean_kaggle_file():
    ep_names = cache_ep_names()
    with open(kaggle_file, 'r') as k, open("clean_kaggle_file.csv", 'w') as o:
        w = csv.writer(o, delimiter=";")
        k.readline()
        line = k.readline()
        while line:
            line = line.split(';')
            ep_name, quote, character = line[2], line[3], line[4]
            ep_num = ep_names[ep_name]
            w.writerow([ep_num[0], ep_num[1], character, quote])
            line = k.readline()


# THIS FUNCTION DOESN'T WORK YET
def match_character_to_quote():
    with open(clean_kaggle_f, 'r') as k, open("everything_except_scene_num.csv", "w") as out:
        k_line = k.readline().split(';')
        character, k_quote = k_line[2], k_line[3]
        my_path = "C:\\Users\\Tamar 2\\Dropbox\\uni\\מחט\\final project\\GoT quotes tayloring\\str to csv"
        all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
        w = csv.writer(out)
        for p in all_files:
            s_num, ep_num = p.split(" - ")[1].split("x")
            with open("str to csv\\" + p, 'r') as in_csv:
                for line in in_csv:
                    if line.strip():
                        line = line.split(';')
                        srt_quote = line[3]
                        if fuzz.partial_ratio(srt_quote, k_quote) > 75:
                            print(character)
                            print(srt_quote)
                            print()
                            w.writerow([s_num, ep_num, line[1], line[2], character, srt_quote])
                            if fuzz.partial_ratio(k_quote[-len(srt_quote):], srt_quote) > 90:
                                k.readline()
                                k_line = k.readline().split(';')
                                character, k_quote = k_line[2], k_line[3]


match_character_to_quote()


