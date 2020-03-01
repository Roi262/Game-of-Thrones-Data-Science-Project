from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import pandas as pd
import numpy as np


import os

offsets = {
    5: {1: {"path": "", "offset": -213},
        2: {"path": "", "offset": -96},
        3: {"path": "", "offset": -90},
        4: {"path": "", "offset": -94},
        5: {"path": "", "offset": -104},
        6: {"path": "", "offset": -106},
        7: {"path": "", "offset": -106},
        8: {"path": "", "offset": -102},
        9: {"path": "", "offset": -148},
        10: {"path": "", "offset": -195}
        },

    6: {1: {"path": "", "offset": -308},
        2: {"path": "", "offset": -178},
        3: {"path": "", "offset": -207},
        4: {"path": "", "offset": -195},
        5: {"path": "", "offset": -200},
        6: {"path": "", "offset": -184},
        7: {"path": "", "offset": -176},
        8: {"path": "", "offset": -251},
        9: {"path": "", "offset": -171},
        10: {"path": "", "offset": -218}
        },
    7: {1: {"path": "", "offset": -79},
        2: {"path": "", "offset": -77},
        3: {"path": "", "offset":  33},
        4: {"path": "", "offset": -33},
        5: {"path": "", "offset": -34},
        6: {"path": "", "offset": -34},
        7: {"path": "", "offset": -69}
        }
}


paths = []

directory = r'/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes'  # add path to tamars files
season = 5
ep = 1
for entry in os.scandir(directory):
    paths.append(entry.path)

print(paths)
    # if ep <= 10:
    #     offsets[season][ep]["path"] = entry.path
    #     ep += 1
    # else:
    #     ep = 1
    #     season += 1

# print("offsets\n\n", offsets)


# {5: {1: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E03 High Sparrow.csv', 'offset': -213}, 2: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E01 The Red Woman.csv', 'offset': -96}, 3: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E06 Beyond The Wall.csv', 'offset': -90}, 4: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E02 The House Of Black And White.csv', 'offset': -94}, 5: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E05 Eastwatch.csv', 'offset': -104}, 6: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E09 Battle of the Bastards.csv', 'offset': -106}, 7: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E02 Home.csv', 'offset': -106}, 8: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E01 Dragonstone.csv', 'offset': -102}, 9: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E10 The Winds of Winter.csv', 'offset': -148}, 10: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E06 Blood of My Blood.csv', 'offset': -195}}, 6: {1: {'path': "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E03 The Queen's Justice.csv", 'offset': -308}, 2: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E02 Stormborn.csv', 'offset': -178}, 3: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E08 Hardhome.csv',
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'offset': -207}, 4: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E04 The Spoils Of War.csv', 'offset': -195}, 5: {'path': "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E10 Mother's Mercy.csv", 'offset': -200}, 6: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E05 Kill The Boy.csv', 'offset': -184}, 7: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E07 The Gift.csv', 'offset': -176}, 8: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E07 The Broken Man.csv', 'offset': -251}, 9: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E03 Oathbreaker.csv', 'offset': -171}, 10: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E08 No One.csv', 'offset': -218}}, 7: {1: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E07 The Dragon And The Wolf.csv', 'offset': -79}, 2: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E04 Sons Of The Harpy.csv', 'offset': -77}, 3: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E06 Unbowed, Unbent, Unbroken.csv', 'offset': 33}, 4: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E04 Book of the Stranger.csv', 'offset': -33}, 5: {'path': '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E05 The Door.csv', 'offset': -34}, 6: {'path': '', 'offset': -34}, 7: {'path': '', 'offset': -69}}}


# FUZZY_THRESH = 85
# LINES_CSV = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/kaggle_cleaned.csv"

# def line_is_in_scene(line, scene_in_one_string):
#     """Checks whether a given line is in the given sentences of a certain scene.
#     check is done as follows:
#     1. create one long string of the scene
#     2. check if line is in the scene with p accuracy

#     Arguments:
#         line {string} -- A line in the script
#         scene_sentences {array of strings} -- an array of strings in a scene
#     """
#     window_size = len(line)
#     i = 0
#     # REMARK: Very brute force solution. not so bad since we only create the table once
#     while i + window_size < len(scene_in_one_string):
#         cur_string = scene_in_one_string[i:i+window_size]
#         if fuzz.ratio(line, cur_string) >= FUZZY_THRESH:
#             return True
#         i += 1
#     return False

# def get_episode_lines(episodes):
#     """

#     Arguments:
#         episodes {[type]} -- a list of episode dataframes

#     Returns:
#         [dictionary] -- {(season, episode): [(speaker, line),...] - list of tuples of speaker and line}
#     """
#     speaker_and_line_dic = {}
#     for episode in episodes:
#         season_num, episode_num = int(episode[0][0]), int(episode[0][1])
#         episode_speakers_and_lines = []
#         names = episode[1]["Name"].tolist()
#         lines = episode[1]["Sentence"].tolist()
#         for i in range(len(lines)):
#             episode_speakers_and_lines.append((names[i], lines[i]))
#         speaker_and_line_dic[(season_num, episode_num)] = episode_speakers_and_lines
#     return speaker_and_line_dic


#     new_table = np.ndarray(shape=(0, LINE_FEATURES_NUM))


# # new_table1 = np.array([[0,0,0,0,0]])
# new_table1 = np.ndarray(shape=(0,5))
# # print(new_table1)
# new_line = [[0, 1, ["er", "er"], ["dfdsd","sdfsdf"], ["dfdsdfsd","sdfsdsdff"]]]

# table = np.append(new_table1, new_line, axis=0)
# print(table)
# k=3

# data = pd.read_csv(LINES_CSV, delimiter=";", header=0)
# df = pd.DataFrame(data)
# gg = df['Season']
# episodes = df.groupby(['Season', 'Episode'])
# g = 9


# get_episode_lines(episodes)
# for episode in episodes:
#     print(episode)
#     g = get_episode_lines(episode)
#     l=0


# with open(LINES_CSV, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in reader:
#             print(', '.join(row))

# print(line_is_in_scene("helo i've comesf for you", "pppppp hello ive come for you sodkfoksdok"))
