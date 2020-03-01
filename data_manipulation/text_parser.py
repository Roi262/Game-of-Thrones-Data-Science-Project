import csv
import pickle
import pandas as pd
from os import path
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from join_srt_and_scenes import get_scenes_lines_dic, offsets

NUM_OF_SEASONS = 7
LINES_CSV = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/kaggle_cleaned.csv"

# TODO find best ratio
FUZZY_THRESH = 75
LINE_FEATURES_NUM = 5


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
    scene_in_one_string = ''
    for sentence in scene_sentences:
        scene_in_one_string += ' '
        scene_in_one_string += sentence
    return scene_in_one_string

# TODO make this run faster
def clean_csv(scenes, lines_in_ep, season, episode):
    pickle_path = 'verified_lines: season{}, episode {}'.format(season, episode)
    if path.exists(pickle_path):
        return load_pickle(pickle_path)

    verified_lines = []
    for (speaker, line) in lines_in_ep:
        for scene_id, (scene_sentences, scene_characters) in enumerate(scenes):
            scene_in_one_string = get_one_string(scene_sentences)
            # if line == 'No':
            #     j=0
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
        # scene_lines_counter = 0
        # TODO may be a problem here, not enough lines are added
        if line_id == len(lines_in_ep):
                break
        scene_in_one_string = get_one_string(scene_sentences)
        line = lines_in_ep[line_id][1]
        while line_is_in_scene(line, scene_in_one_string):
            if line_id == 75:
                g = 9
            new_line = np.array([[scene_id, line_id, lines_in_ep[line_id][0],
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
        # print(episode)
        # k=2
        season_num, episode_num = int(episode[0][0]), int(episode[0][1])
        episode_speakers_and_lines = []
        names = episode[1]["Name"].tolist()
        lines = episode[1]["Sentence"].tolist()
        for i in range(len(lines)):
            episode_speakers_and_lines.append((names[i], lines[i]))
        speaker_and_line_dic[(season_num, episode_num)] = episode_speakers_and_lines
    return speaker_and_line_dic


def create_final_csv():
    # all_scenes = get_scenes()  # TODO extract scenes from csv
    table = np.ndarray(shape=(0, LINE_FEATURES_NUM))
    data = pd.read_csv(LINES_CSV, delimiter=";", header=0)
    df = pd.DataFrame(data)
    episodes = df.groupby(['Season', 'Episode'])
    speaker_and_line_dic = get_episode_lines(episodes)
    scenes_lines_dic = get_scenes_lines_dic()

    for season in offsets.keys():
        if not season == 4: continue
        for episode in offsets[season].keys():
            if not episode == 3:
                continue
                k = 0
            scenes = scenes_lines_dic[(season, episode)]
            lines = speaker_and_line_dic[(season, episode)]
            episode_table = text_join(scenes=scenes, lines_in_ep=lines, season=season, episode=episode)
            if episode == 4:
                j = 0
            table = np.append(table, episode_table, axis=0)
            k=2
    p=0
    np.savetxt('/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - NEW/data/Game of Thrones/joint_lines_with_scenes.csv', table, delimiter=';')
# TODO print table to file

create_final_csv()
# print(group)

# for season in NUM_OF_SEASONS:
#     for episode
# for line in lines_csv:

# for episode in script:
#     scenes = get_scenes_in_epiode()
#     lines = get_lines_in_episode()
#     text_join(table, scenes, lines)


# create_final_csv()


# while scene_lines_counter < len(lines_in_episode):
#     line = lines_in_episode[line_id]
#     if line_is_in_scene(line, scene_in_one_string):
#         speaker = speakers[line_id]
#         new_line = [scene_id, line_id, speaker, line, scene_characters]
#     #  (scene id, line id, line, speaker, set of (other) characters in the scene)
#         np.append(new_table, new_line, axis=0)
#     scene_lines_counter += 1
#     line_id += 1