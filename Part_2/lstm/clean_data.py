import csv
import ast
from configure import *
from collections import defaultdict
import pandas as pd


def clean_lines_with_scenes(path):
    """ Sync Speaker name in the dataset with their formal name as presented in 
    the list of present characters. E.g, if speaker = ned, this function changes the
    value to 'Eddard Stark', or 'cersei' to 'Cersei Lannister'.

    Arguments:
        path {[string]} -- path to the csv file
    """
    with open(path, newline='') as f:
        data = csv.reader(f)
        cleaned_data = []
        data_len = 0
        for i, line in enumerate(data):
            if i == 0:
                continue  # header
            speaker = line[SPEAKER]
            # override exceptions
            if speaker in EXCEPTIONS.keys():
                speaker = EXCEPTIONS[speaker]

            characters = ast.literal_eval(line[CHARACTERS])
            for character in characters:
                if speaker.lower() in character.lower():
                    line[SPEAKER] = character
                    cleaned_data.append(line)
                    break
                # print(speaker, ': ', characters)
            data_len = i

    new_path = 'part2_data_cleaned.csv'
    with open(new_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(cleaned_data)

    # record number of lines lost in this process
    print(data_len - len(cleaned_data))


def get_most_common_characters(path, num_of_characters=MAX_CHARACTERS):
    """
    Returns:
        [list] -- a list of the most common characters based on the number of scenes 
        they took part in.
    """
    with open(path, newline='') as f:
        df = pd.read_csv(f)
        scenes = df['Characters']
        characters_counter = defaultdict(int)
        for scene in scenes:
            for character in ast.literal_eval(scene):
                characters_counter[character] += 1

        my_dict = {k: v for k, v in sorted(
            characters_counter.items(), key=lambda item: item[1], reverse=True)}
        most_common = list(my_dict.keys())[:num_of_characters]
        return most_common


def clean_labels(path):
    """
    Remove all data with non common characters. create new csv file with only common characters.
    Arguments:
        path {[type]} -- [description]
    """
    new_data = []
    most_common_characters = get_most_common_characters(path)
    with open(path, newline='') as f:
        data = csv.reader(f)
        for i, line in enumerate(data):
            if i == 0: # header
                continue
            cleaned_characters = []
            for character in ast.literal_eval(line[CHARACTERS]):
                if character in most_common_characters:
                    cleaned_characters.append(character)
            if cleaned_characters:
                new_line = line[:CHARACTERS] + [cleaned_characters]
                new_data.append(new_line)

    new_path = 'part2_data_cleaned_characters.csv'
    with open(new_path, 'w+', newline='') as f:
        w = csv.writer(f)
        w.writerows(new_data)


def normalize_scene_ids(path):
    """ Create new csv where the sceneIDs are organized chronologically w.r.t the entire show
    """
    new_data = []
    with open(path, newline='') as f:
        data = csv.reader(f)
        previous_sceneID = 0
        sceneID = 0
        new_scene_id = 0
        for i, line in enumerate(data):
            sceneID = ast.literal_eval(line[SCENE])
            if sceneID > previous_sceneID:
                sceneID = ast.literal_eval(line[SCENE])
                new_scene_id += 1

            new_line = line[:SCENE] + [new_scene_id] + line[SCENE + 1:]
            new_data.append(new_line)
            previous_sceneID = sceneID

    new_path = 'part_3_data_cleaned_characters_new_sceneIDs.csv'
    with open(new_path, 'w+', newline='') as f:
        w = csv.writer(f)
        w.writerows(new_data)


if __name__ == "__main__":
    # clean_labels('Part_2/part2_data_cleaned.csv')
    normalize_scene_ids('part2_data_cleaned_characters.csv')

    # clean_lines_with_scenes(part2_data_path)
