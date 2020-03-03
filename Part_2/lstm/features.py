from configure import *
import ast
import csv
import re
import numpy as np


RELEVANT_CHARACTERS = CHARACTERS_DIC

def spoken_to_in_sent_features(line):
    spoken_to_in_sent = [0] * len(RELEVANT_CHARACTERS)

    # for row in data:
    #     line = row[LINE]
        # characters = ast.literal_eval(row[CHARACTERS])

        # 1. check whether a characters name is said in the line itself
    for character in RELEVANT_CHARACTERS.keys():
        character_subnames = character.split()
        for name in character_subnames:
            if name in line.split():
                spoken_to_in_sent[RELEVANT_CHARACTERS[character]] = 1
                break
                # TODO add 1 in 'character spoken to' index. note that for every rele
                # we have this one hot per character code somewhere
    return np.asarray(spoken_to_in_sent)



# def get_subject_words():
#     # TODO use top 30 subject words (i.e., words that start with capital letters that are not the first word in a sentence)
#     df = pd.read_csv(CLEAN_DATA_PATH, error_bad_lines=False, delimiter=',', header=0)
#     all_lines = df['Line']
#     subject_words = set()
#     for line in all_lines:
#         for i, word in enumerate(line.split()):
            




    # text_path = 'got_lines.txt'
    # with open(text_path, 'w+') as f:
    #     # f.writelines(saved_column)
    #     for sent in all_lines:
    #         f.write(sent + ' ')


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
    # TODO add Average Syllable per Word? Functional Words Count?

    # symbols:
    f = [text.count("?"), text.count("!"), text.count(","), text.count("-"), text.count(".")]

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
    # TODO use tokenize/onehot
    # for line in data():
    features = np.append(additional_features(line[6]), spoken_to_in_sent_features(line[6]))
    # add character id
    features = np.append(features, CHARACTERS_DIC[line[SPEAKER]])
    return features

    # newline = add_features_to_vec()
        # TODO add line to data



