from itertools import combinations
# from configure import *
from Part_2.configure import *
from Part_2.lstm.clean_data import get_most_common_characters
import nltk
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
NUM_OF_PAIRS = 10

RELEVENT_CHARACTERS = ALL_CHARACTERS_FORMAL

sid = SentimentIntensityAnalyzer()

# def get_vader_score(sent):
#     # Polarity score returns dictionary
#     ss = sid.polarity_scores(sent)
#     for k in sorted(ss):
#         print('{0}: {1}, '.format(k, ss[k]), end='')
#         print()


def get_both_char_lines():
    """returns one list of all lines character A says and
     another list of all lines character B says 
    """


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
    return float(average_compound)/len(sentences)
    # ss = sid.polarity_scores(text)
    # return ss['compound']


def get_dialogues(data_path, char_1, char_2, conversation_thresh=5, noise=.1):
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
    with open(data_path, newline='') as f:
        data = csv.reader(f)
        conversations = []
        for i, row in enumerate(data):
            if i == 0:
                continue
            row_counter = 0
            dialoug = []
            word_count = 0
            other_speaker_counter = 0
            while True:
                if row[SPEAKER] == char_1 or row[SPEAKER] == char_2:
                    word_count += len(row[LINE].split())
                    dialoug.append((row[SCENE], row[SPEAKER], row[LINE]))
                    row_counter += 1
                else:
                    other_speaker_counter += 1
                    if float(other_speaker_counter)/row_counter > noise:
                        break
            if row_counter >= conversation_thresh:
                sentiment = get_sentiment([tup[1] for tup in dialoug])
                conversations.append((dialoug, word_count, len(
                    dialoug), (char_1, char_2), sentiment))
    return conversations


def plot_pair():
    pass


def get_arrays(conversations):
    non_normalized_x = []
    x = []
    y = []
    scenes_dic = defaultdict(int)
    passed_scenes_dict = defaultdict(int)
    
    for conversation in conversations:
        lines_in_scene = conversation[2]
        for sceneID, speaker, line in conversation[0]:
            sentiment = get_sentiment(line)
            non_normalized_x.append((sceneID, sentiment))
            scenes_dic[sceneID] += 1


    for sceneID, sentiment in non_normalized_x:
        x.append(sceneID + float(passed_scenes_dict[sceneID])/scenes_dic[sceneID])
        passed_scenes_dict[sceneID] += 1
        y.append(sentiment)

    return np.array(x), np.array(y)
        


def plot_conversations(conversations):
    plt.figure()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'lime', 'lavender']
    for i, dialogue in enumerate(conversations):
        x, y = get_arrays(dialogue)
        pair = dialogue[3]
        plt.plot(x, y, label=str(pair), color=colors[i])
    plt.show()
        

def main():
    # conversations = np.ndarray(shape=(0, 6))
    conversations = []
    common_characters = get_most_common_characters(
        'Part_2/part2_data_cleaned.csv')
    # get all permutations of common_character pairs
    pairs = list(combinations(common_characters, 2))
    path = 'part_3_data_cleaned_characters_new_sceneIDs.csv'
    for pair in pairs:
        # conversations = np.append(conversations, get_dialogues(path, pair[0], pair[1]), axis=0)
        conversations.append(get_dialogues(path, pair[0], pair[1]))

    # plot_conversations(conversations)

    most_common_conversations = [v for v in sorted(
        conversations, key=lambda item: item[2], reverse=True)][:NUM_OF_PAIRS]

    plot_conversations(most_common_conversations)


if __name__ == "__main__":
    main()

# def score_function(k, nw) -> float:
#     """[summary]

#     Arguments:
#         k {[int]} -- number of rows in conversation
#         nw {[int]} -- total number of words in conversation

#     Returns:
#         float -- function score
#     """
#     word_count = 0
#     for row in rows_in_convo:
#         char1_lines, char2_lines = get_both_char_lines()
