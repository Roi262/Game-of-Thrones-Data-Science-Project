import viz
from collections import defaultdict
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


STOPWORDS = set(stopwords.words('english')).union("I")
MAJOR_CHAR_COUNT = 20
WORD_COUNT = 13


def common_characters():
    with open("data/HPMovies/HP1.csv") as f:
        speaker_counter = defaultdict(int)
        major_speakers_counter = defaultdict(int)
        for line in f:
            speaker = line.split(",")[0]
            speaker_counter[speaker] += 1
        viz.dict_to_bar_graph(dict, MAJOR_CHAR_COUNT)


def common_words():
    with open("data/HPMovies/HP1.csv") as f:
        words_counter = defaultdict(int)
        for line in f:
            line = line.replace("{", " ").replace(", ", " ").replace(". ", " ")
            for word in line.split(" "):
                if word.lower() in {"",  " ", "the", "i", "i'm", "he", "you", "and"}:
                    continue
                if word.lower() in {"think",  "know", "it's", "but", "go", "going", "see", "it", "got", "like",
                                    "would", "they", "come", "get", "a", "that's"}:
                    continue
                if word not in STOPWORDS:
                    words_counter[word] += 1
        viz.dict_to_bar_graph(words_counter, WORD_COUNT)


common_words()
