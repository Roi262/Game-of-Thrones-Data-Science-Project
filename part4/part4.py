import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from Part_2.lstm.clean_data import get_most_common_characters

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
    # if "Brea" in all_characters:
    #     print(all_characters.index("Brea"))
    for line in data:
        text = line[COLUMN_MAP["Line"]]
        speaker = line[COLUMN_MAP["Speaker"]]
        characters_in_scene = ast.literal_eval(line[COLUMN_MAP["Characters"]])
        characters_in_text = find_characters_in_text(text, MOST_COMMON_CHARACTERS)
        relevant_characters = set(characters_in_text) - set(characters_in_scene)
        for character in relevant_characters:
            character_said_on_dict[character].append((speaker, text))
    return character_said_on_dict


def plot_score_data(data):
    characters = [data_line[0] for data_line in data]
    number_of_sentences = [data_line[1] for data_line in data]
    score_data = [data_line[2] for data_line in data]

    ind = np.arange(len(data))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, number_of_sentences, width, label='Number Of Sentences')
    rects2 = ax.bar(ind + width / 2, score_data, width, label='Score')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind)
    ax.set_xticklabels(characters)
    ax.legend()

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    autolabel(rects1, "left")
    autolabel(rects2, "right")

    fig.tight_layout()

    plt.show()


def get_score_data(said_on_dict):
    score_data = []
    for character in said_on_dict.keys():
        number_of_sentences = len(said_on_dict[character])
        score = func()  # TODO: call roy's function
        score_data.append((character, number_of_sentences, score))
    return score_data


def print_dict(d):
    for key in d.keys():
        print(key, ":")
        for t in d[key]:
            print("\t", t)


if __name__ == "__main__":
    data = load_data()
    print_dict(find_said_on_dict(data))
