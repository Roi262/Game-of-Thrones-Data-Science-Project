import csv
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import numpy as np

kaggle_file = "/cs/usr/tamar.yov/Desktop/final_project/" \
              "Data-Science---Final-Project/data/Game of Thrones/kaggle_cleaned.csv"


def find_top_characters(reader):
    # count_threshold = 5000
    speaker_counter = defaultdict(int)
    for line in reader:
        if line:
            speaker = line[2]
            line = line[3].split(" ")
            speaker_counter[speaker] += len(line)

    # dict_to_bar_graph(speaker_counter, count_threshold, "Characters that said most words")
    return [e[0] for e in sorted(speaker_counter.items(), key=lambda x:x[1], reverse=True)[:30]]


def is_stop_word(word):
    return word in set(stopwords.words('english'))


def find_word_freq(reader):
    ps = PorterStemmer()
    d = defaultdict(int)
    prev = []
    for row in reader:
        if row:
            ep = row[:2]
            if ep != prev:
                print(ep)
            prev = ep
            text = row[3]
            text = text.replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")
            text = text.replace("\"", " ").replace("\'", " ").replace("-", " ")
            for word in text.split(" "):
                word = ps.stem(word)
                if not is_stop_word(word):
                    d[word.lower()] += 1
    return d


def get_word_map():
    """
    word_freqs is a csv listing all stemmed words in the corpus and how many times they appear.
    This function returns all stemmed words, sorted by frequency. A word's index in the return
    value is its ID for the one-hot vectors
    """
    with open("word_freqs.csv", 'r') as f:
        out = []
        for line in f:
            if line:
                out.append(line.split(';')[0])
        return out


def clean_text(text):
    text = text.replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")
    text = text.replace("\"", " ").replace("\'", " ").replace("-", " ")
    return text.split(" ")


def words_one_hot(text, word_map):
    ps = PorterStemmer()
    vec = np.zeros((len(word_map)))
    text = clean_text(text)
    for word in text:
        word = ps.stem(word.lower())
        if (not is_stop_word(word)) and word.strip():
            word_id = word_map.index(word)
            vec[word_id] += 1
    return vec


def additional_features(text):
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


def create_sentence_vectors(file_obj):
    reader = csv.reader(file_obj, delimiter=';')
    word_map = get_word_map()
    top_chars = find_top_characters(reader)
    for n, i in enumerate(top_chars):
        print(n, i)
    file_obj.seek(0)
    line_counter = 0
    with open("try.csv", 'w') as o, open("sentence_vectors_labels.csv", 'w') as l:
        writer = csv.writer(o)
        label_writer = csv.writer(l)
        for line in reader:
            if line_counter % 5000 == 0:
                print("line", line_counter, "out of 45020")
            line_counter += 1
            if line:
                char_name = line[2]
                if char_name in top_chars:
                    vec = np.hstack((words_one_hot(line[3], word_map), additional_features(line[3])))
                    writer.writerow(vec)
                    label_writer.writerow([top_chars.index(char_name)])


with open(kaggle_file, 'r') as k:
     create_sentence_vectors(k)
     a=0



