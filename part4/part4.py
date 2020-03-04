import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from Part_2.lstm.clean_data import get_most_common_characters
from Part_3.bonus_analysis import get_sentiment

DATA_PATH = "../Part_2/part2_data_cleaned.csv"
COLUMN_MAP = {"Line": 6, "Speaker": 5, "Characters": 7}
MOST_COMMON_CHARACTERS = list(
    set(get_most_common_characters(DATA_PATH)) - {"Lord Varys", "Grey Worm", "Grand Maester Pycelle"})


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
    # return character.lower() in text.lower()
    if character.lower() in text.lower():
        return True
    if character in MOST_COMMON_CHARACTERS:
        first_name = character.split()[0]
        if first_name.lower() in text.lower():
            return True
    return False


def find_characters_in_text(text, characters):
    characters_in_text = []
    for character in characters:
        if is_character_in_text(character, text):
            characters_in_text.append(character)
    return characters_in_text


def find_said_on_dict(data):
    character_said_on_dict = {character: [] for character in MOST_COMMON_CHARACTERS}
    for line in data:
        text = line[COLUMN_MAP["Line"]]
        speaker = line[COLUMN_MAP["Speaker"]]
        characters_in_scene = ast.literal_eval(line[COLUMN_MAP["Characters"]])
        characters_in_text = find_characters_in_text(text, MOST_COMMON_CHARACTERS)
        relevant_characters = set(characters_in_text) - set(characters_in_scene)
        for character in relevant_characters:
            character_said_on_dict[character].append((speaker, text))
    return character_said_on_dict


def plot_score_data(data, title=""):
    characters = [data_line[0] for data_line in data]
    number_of_sentences = [data_line[1] for data_line in data]
    score_data = [data_line[2] for data_line in data]

    def color(score):
        mult_factor = 5
        green = np.array([0, 1, 0, 1])
        yellow = np.array([1, 1, 0, 1])
        red = np.array([1, 0, 0, 1])
        if score > 0:
            t = score
            ret_color = t ** mult_factor * green + (1 - t ** mult_factor) * yellow
        else:
            t = - score
            ret_color = t ** mult_factor * red + (1 - t ** mult_factor) * yellow
        return tuple(ret_color)

    height = number_of_sentences
    bars = characters
    y_pos = np.arange(len(bars))

    plt.bar(y_pos, height, color=[color(score) for score in score_data])
    plt.xticks(y_pos, bars, rotation='vertical')
    plt.ylabel("Number Of Sentences")
    plt.title(title)
    plt.show()


def get_score_data(said_on_dict):
    score_data = []
    for character in said_on_dict.keys():
        number_of_sentences = len(said_on_dict[character])
        sentences = [t[1] for t in said_on_dict[character]]
        score = get_sentiment(sentences)
        score_data.append((character, number_of_sentences, score))
    return score_data


def invert_keys(said_on_dict):
    said_dict = {character: [] for character in MOST_COMMON_CHARACTERS}
    for said_on_ch in said_on_dict.keys():
        for t in said_on_dict[said_on_ch]:
            said_ch, sentence = t
            if said_ch in MOST_COMMON_CHARACTERS:
                said_dict[said_ch].append((said_on_ch, sentence))
    return said_dict


def print_dict(d):
    for key in d.keys():
        print(key, ":")
        for t in d[key]:
            print("\t", t)


if __name__ == "__main__":
    data = load_data()
    said_on_dict = find_said_on_dict(data)
    score_said_on_data = get_score_data(said_on_dict)
    plot_score_data(score_said_on_data, title="Sentiment Analysis of gossip Sentences ON character")
    said_dict = invert_keys(said_on_dict)
    score_said_data = get_score_data(said_dict)
    plot_score_data(score_said_data, title="Sentiment Analysis of gossip Sentences FROM character")
