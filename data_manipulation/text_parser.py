import csv
import pickle
import glob
import pandas as pd
from os import path
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from join_srt_and_scenes import get_scenes_lines_dic, offsets

NUM_OF_SEASONS = 7
LINES_CSV = "../data/Game of Thrones/kaggle_cleaned.csv"
# LINES_CSV = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/data/Game of Thrones/kaggle_cleaned.csv"

# best fuzzy ratio
FUZZY_THRESH = 75
LINE_FEATURES_NUM = 7


def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


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
        cur_string = scene_in_one_string[i:i + window_size]
        if fuzz.ratio(line, cur_string) >= FUZZY_THRESH:
            return True
        i += 1
    return False


def get_one_string(scene_sentences):
    """
    Arguments:
        scene_sentences {[type]} -- [description]
    
    Returns:
        [string] -- all sentences in the scene as one long string
    """
    scene_in_one_string = ''
    for sentence in scene_sentences:
        scene_in_one_string += ' '
        scene_in_one_string += sentence
    return scene_in_one_string


def clean_csv(scenes, lines_in_ep, season, episode):
    """This function cleans (removes) all lines from the Kaggle csv file 
    that do not exist in the srt subtitles files. This happens for example where there is 
    text in fantasy language in the kaggle file that is not in the srt files.
    
    Arguments:
        scenes {[type]} -- [description]
        lines_in_ep {[type]} -- [description]
        season {[type]} -- [description]
        episode {[type]} -- [description]
    
    Returns:
        [list] -- a list of all verified lines that show up in both datasets
    """
    pickle_dir = '../pickles/'
    if season < 4:
        pickle_path = pickle_dir + \
            'verified_lines_season_{}_episode_{}'.format(season, episode)
    else:
        pickle_path = pickle_dir + \
            'verified_lines: season{}, episode {}'.format(season, episode)

    if path.exists(pickle_path):
        return load_pickle(pickle_path)

    verified_lines = []
    for (speaker, line) in lines_in_ep:
        for scene_id, (scene_sentences, scene_characters) in enumerate(scenes):
            scene_in_one_string = get_one_string(scene_sentences)
            if line_is_in_scene(line, scene_in_one_string):
                verified_lines.append((speaker, line))
                break
    save_pickle(verified_lines, pickle_path)
    return verified_lines


def text_join(scenes, lines_in_ep, season, episode):
    """
    Arguments:
        scenes {[([sentences], [characters]),...]} -- all the scenes in the episode. list of tuples. each tuple represents a scene,
         and  holds a list of sentences in the scene, and a list of characters in the scene
        lines_in_episode {[(speaker, line)]} -- list of tuples of speaker and line
    """
    new_table = np.ndarray(shape=(0, LINE_FEATURES_NUM))

    lines_in_ep = clean_csv(scenes, lines_in_ep, season, episode)

    line_id = 0
    for scene_id, (scene_sentences, scene_characters) in enumerate(scenes):
        if line_id == len(lines_in_ep):
            break
        scene_in_one_string = get_one_string(scene_sentences)
        line = lines_in_ep[line_id][1]
        while line_is_in_scene(line, scene_in_one_string):
            new_line = np.array([[season, episode, scene_id, line_id, lines_in_ep[line_id][0],
                                  lines_in_ep[line_id][1], scene_characters]])
            new_table = np.append(new_table, new_line, axis=0)
            line_id += 1
            if line_id == len(lines_in_ep):
                break
            line = lines_in_ep[line_id][1]
    return new_table


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
        speaker_and_line_dic[(season_num, episode_num)
                             ] = episode_speakers_and_lines
    return speaker_and_line_dic


def create_final_csv():
    """function that creates the final merged and cleaned csv file, from the kaggle dataset, and the 
    subtitles in scenes dataset.
    """
    table = np.ndarray(shape=(0, LINE_FEATURES_NUM))
    data = pd.read_csv(LINES_CSV, delimiter=";", header=0)
    df = pd.DataFrame(data)
    episodes = df.groupby(['Season', 'Episode'])
    speaker_and_line_dic = get_episode_lines(episodes)
    scenes_lines_dic = get_scenes_lines_dic()

    for season in offsets.keys():
        for episode in offsets[season].keys():
            scenes = scenes_lines_dic[(season, episode)]
            lines = speaker_and_line_dic[(season, episode)]
            episode_table = text_join(
                scenes=scenes, lines_in_ep=lines, season=season, episode=episode)
            table = np.append(table, episode_table, axis=0)
            print(season, episode)
            # fname = 'joint_lines_with_scenes_{}_{}.csv'.format(season, episode)
            # pd.DataFrame(episode_table).to_csv(fname)

    fname_all_seasons = 'joint_lines_with_scenes_season.csv'
    pd.DataFrame(table).to_csv(fname_all_seasons)


def add_header(header, csv_file_path):
    """adds a header to the csv file
    
    Arguments:
        header {[type]} -- [description]
        csv_file_path {[type]} -- [description]
    """
    with open(csv_file_path, newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        data.pop(0)
    with open('part2_data_lines_with_scenes.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


# create_final_csv()
header = ['rowID', 'Season', 'Episode', 'Scene',
          'Line in Episode', 'Speaker', 'Line', 'Characters']
add_header(header, 'Part_2/part2_data_cleaned.csv')
