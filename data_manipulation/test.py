from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import csv
import pandas as pd
import numpy as np

FUZZY_THRESH = 85
LINES_CSV = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/kaggle_cleaned.csv"

def line_is_in_scene(line, scene_in_one_string):
    """Checks whether a given line is in the given sentences of a certain scene.
    check is done as follows:
    1. create one long string of the scene
    2. check if line is in the scene with p accuracy
    
    Arguments:
        line {string} -- A line in the script
        scene_sentences {array of strings} -- an array of strings in a scene
    """
    window_size = len(line)
    i = 0
    # REMARK: Very brute force solution. not so bad since we only create the table once
    while i + window_size < len(scene_in_one_string):
        cur_string = scene_in_one_string[i:i+window_size]
        if fuzz.ratio(line, cur_string) >= FUZZY_THRESH:
            return True
        i += 1
    return False

def get_episode_lines(episodes):
    """
    
    Arguments:
        episodes {[type]} -- a list of episode dataframes
    
    Returns:
        [dictionary] -- {(season, episode): [(speaker, line),...] - list of tuples of speaker and line}
    """
    speaker_and_line_dic = {}
    for episode in episodes:
        season_num, episode_num = int(episode[0][0]), int(episode[0][1])
        episode_speakers_and_lines = []
        names = episode[1]["Name"].tolist()
        lines = episode[1]["Sentence"].tolist()
        for i in range(len(lines)):
            episode_speakers_and_lines.append((names[i], lines[i]))
        speaker_and_line_dic[(season_num, episode_num)] = episode_speakers_and_lines
    return speaker_and_line_dic





    new_table = np.ndarray(shape=(0, LINE_FEATURES_NUM))


# new_table1 = np.array([[0,0,0,0,0]])
new_table1 = np.ndarray(shape=(0,5))
# print(new_table1)
new_line = [[0, 1, ["er", "er"], ["dfdsd","sdfsdf"], ["dfdsdfsd","sdfsdsdff"]]]

table = np.append(new_table1, new_line, axis=0)
print(table)
k=3

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