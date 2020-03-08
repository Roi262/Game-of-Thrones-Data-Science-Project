import pickle
from itertools import combinations
from configure import *
from Part_2.lstm.clean_data import get_most_common_characters
import nltk
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm import tqdm
import pandas as pd
import os

# nltk.download('vader_lexicon')
NUM_OF_PAIRS = 5

RELEVENT_CHARACTERS = ALL_CHARACTERS_FORMAL

sid = SentimentIntensityAnalyzer()


def get_sentiment(sentences):
    """Calculates sentiment of a text.

    Arguments:
        sentences {[list]} -- a list of sentences

    Returns:
        [float] -- the compound sentiment of the text as a value in [-1,1]
    """
    if type(sentences) == str:
        return sid.polarity_scores(sentences)['compound']

    text = ''
    average_compound = 0
    for sent in sentences:
        text += ' ' + sent
        average_compound += sid.polarity_scores(sent)['compound']
    return float(average_compound) / len(sentences)


def get_dialogues(data_path, char_1, char_2, conversation_thresh=10, noise=.1):
    """get all conversations of these 2 characters
    Arguments:
        data_path {[string]} -- path to csv file
        char_1 {[type]} -- Character 1
        char_2 {[type]} -- Character 2
        conversation_thresh {[int]} -- minimum amount of consecutive lines between 2 
        characters for the lines to be considered a conversation
        noise {[int]} -- maximum number of rows spoken by characters other than 1 and 2 which we 
        can disregard in the conversation
    Returns:
        conversations {2D array} -- an array of arrays of rows depicting conversations
    """
    data = pd.read_csv(data_path, delimiter=',', header=None).to_numpy()
    conversations = []
    i = 0
    while i < len(data):
        row_counter = 0
        dialoug = []
        word_count = 0
        other_speaker_counter = 0
        while i < len(data):
            row = data[i]
            if row[SPEAKER] == char_1 or row[SPEAKER] == char_2:
                word_count += len(row[LINE].split())
                dialoug.append((row[SCENE], row[SPEAKER], row[LINE]))
                row_counter += 1
                i += 1
            else:
                i += 1
                other_speaker_counter += 1
                if row_counter == 0 or float(other_speaker_counter) / row_counter > noise:
                    break
        if row_counter >= conversation_thresh:
            sentiment = get_sentiment([tup[1] for tup in dialoug])
            conversations.append((dialoug, word_count, len(
                dialoug), (char_1, char_2), sentiment))
        i += 1
    return conversations


def get_arrays(conversations):
    x = []
    y = []
    lines_for_scene = defaultdict(list)

    for conversation in conversations:
        for sceneID, speaker, line in conversation[0]:
            lines_for_scene[sceneID].append(line)

    for sceneID in lines_for_scene.keys():
        lines = lines_for_scene[sceneID]
        sentiment = get_sentiment(lines)
        x.append(sceneID)
        y.append(sentiment)

    return np.array(x), np.array(y)


def plot_conversations(conversations):
    plt.figure()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'lime', 'lavender']
    for i, dialogue in enumerate(conversations):
        x, y = get_arrays(dialogue)
        pair = dialogue[0][3]
        plt.plot(x, y, label=str(pair), color=colors[i])
    plt.xlabel("Number of Scene")
    plt.ylabel("Sentiment")
    plt.title("Dialogue Sentiments")
    plt.legend()
    plt.show()


def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def main():
    pickle_path = "conversations_pickle_5"
    if os.path.exists(pickle_path):
        conversations = load_pickle(pickle_path)
    else:
        conversations = []
        common_characters = get_most_common_characters(
            '../Part_2/part2_data_cleaned.csv')
        # get all permutations of common_character pairs
        pairs = list(combinations(common_characters, 2))
        path = '../part_3_data_cleaned_characters_new_sceneIDs.csv'
        for pair in tqdm(pairs):
            conversations.append(get_dialogues(path, pair[0], pair[1]))
        save_pickle(conversations, pickle_path)

    most_common_conversations = [v for v in sorted(
        conversations, key=lambda item: len(item), reverse=True)][:NUM_OF_PAIRS]

    plot_conversations(most_common_conversations)


if __name__ == "__main__":
    main()
