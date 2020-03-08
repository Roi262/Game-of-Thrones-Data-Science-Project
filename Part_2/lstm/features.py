from configure import *
import ast
import csv
import re
import numpy as np


RELEVANT_CHARACTERS = CHARACTERS_DIC


def spoken_to_in_sent_features(line):
    """

    Arguments:
        line {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    spoken_to_in_sent = [0] * len(RELEVANT_CHARACTERS)
    # check whether a characters name is said in the line itself
    for character in RELEVANT_CHARACTERS.keys():
        character_subnames = character.split()
        for name in character_subnames:
            if name in line.split():
                spoken_to_in_sent[RELEVANT_CHARACTERS[character]] = 1
                break
    return np.asarray(spoken_to_in_sent)


def additional_features(text):
    """adds the following additional features:
    Average Word Length
    Average Sentence Length By Word
    Average Sentence Length By Character
    Special Character Count

    Arguments:
        text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # symbols:
    f = [text.count("?"), text.count("!"), text.count(","),
         text.count("-"), text.count(".")]

    # avg sentence length
    text_splitted_to_sentences = re.findall(r"[\w',\- ]+", text)
    sub_sentences_count = len(text_splitted_to_sentences)
    if sub_sentences_count == 0:
        sub_sentences_count = 1
    words = re.findall(r"[\w']+", text)
    if len(words) == 0:
        words = []
        # smoothing
        words_count = 1
    else:
        words_count = len(words)
    avg_sentence_length = words_count/sub_sentences_count

    # avg word len
    letters_counter = 0
    for _ in words:
        letters_counter = letters_counter + words_count
    avg_word_len = letters_counter/words_count
    return np.asarray(f + [avg_sentence_length, avg_word_len, words_count, letters_counter])


def create_features(line):
    features = np.append(additional_features(
        line[6]), spoken_to_in_sent_features(line[6]))
    # add character id
    features = np.append(features, CHARACTERS_DIC[line[SPEAKER]])
    return features, len(features)
