import pandas as pd
import numpy as np
import ast
from Part_2.lstm.clean_data import get_most_common_characters

DATA_PATH = "../Part_2/part2_data_cleaned.csv"
COLUMN_MAP = {"Line": 6, "Speaker": 5, "Characters": 7}
MOST_COMMON_CHARACTERS = get_most_common_characters()


def load_data():
    return pd.read_csv(DATA_PATH).to_numpy()


def all_characters_names(data):
    all_characters = set()
    for line in data:
        characters = ast.literal_eval(line[COLUMN_MAP["Characters"]])
        for character in characters:
            all_characters.add(character)
    return list(all_characters)


def is_character_in_text(character, text):
    return character.lower() in text.lower()


def find_characters_in_text(text, all_characters):
    characters_in_text = []
    for character in all_characters:
        if is_character_in_text(character, text):
            characters_in_text.append(character)
    return characters_in_text

def find_said_on_dict(data):
    all_characters = all_characters_names(data)
    character_said_on_dict = {character: [] for character in all_characters}
    for line in data:
        text = line[COLUMN_MAP["Line"]]
        speaker = line[COLUMN_MAP["Speaker"]]
        characters_in_scene = ast.literal_eval(line[COLUMN_MAP["Characters"]])
        characters_in_text = find_characters_in_text(text, all_characters)
        relevant_characters = set(characters_in_text) - set(characters_in_scene)
        for character in relevant_characters:
            character_said_on_dict[character].append((speaker, text))
    return character_said_on_dict


def print_dict(d):
    for key in d.keys():
        print(key, ":", d[key])


if __name__ == "__main__":
    data = load_data()
    print_dict(find_said_on_dict(data))
