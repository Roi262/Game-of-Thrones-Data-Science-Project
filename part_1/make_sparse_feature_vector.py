import csv
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import numpy as np
from scipy.sparse import csr_matrix as sparse

kaggle_file = "/cs/usr/tamar.yov/Desktop/final_project/" \
              "Data-Science---Final-Project/data/Game of Thrones/kaggle_cleaned.csv"
TOP_CHARACTERS_AMOUNT = 30


def find_top_characters(reader):
    speaker_counter = defaultdict(int)
    for line in reader:
        if line:
            speaker = line[2]
            line = line[3].split(" ")
            speaker_counter[speaker] += len(line)

    top = [e[0] for e in sorted(speaker_counter.items(), key=lambda x:x[1], reverse=True)]
    return top[:TOP_CHARACTERS_AMOUNT]


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
        line = f.readline()
        while line:
            if line.strip():
                out.append(line.split(';')[0])
            try:
                line = f.readline()
            except UnicodeDecodeError:
                continue
        return out


def clean_text(text):
    text = text.replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")
    text = text.replace("\"", " ").replace("\'", " ").replace("-", " ")
    return text.split(" ")


def words_one_hot(text, word_map):
    ps = PorterStemmer()
    text = clean_text(text)
    out = []
    for word in text:
        word = ps.stem(word.lower())
        if (not is_stop_word(word)) and word.strip():
            try:
                out.append(word_map.index(word))
            except ValueError:
                continue
    return np.asarray(out)


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
    for word in words:
        letters_counter = letters_counter + len(word)
    avg_word_len = letters_counter/words_count
    a_features = np.asarray(f + [avg_sentence_length, avg_word_len, words_count])
    nonzero_indices = np.nonzero(a_features)
    return np.vstack((np.take(a_features, nonzero_indices),
                      np.ones_like(nonzero_indices),
                      nonzero_indices))


def create_sentence_vectors(file_obj):
    """
    This function creates sparse (scipy.sparse.csr_matrix) vectors from each feature vectors
    The features include every (stemmed) word in the corpus, as one-hot format, and additional
    features (see additional_features())
    It then saves the results to sparse_vecs.txt in this format:
    (linenum, column, data)
    Only lines spoken by one of the most common 30 characters are saved. (see constant at the top of this file)
    """
    reader = csv.reader(file_obj, delimiter=';')
    word_map = get_word_map()
    top_chars = find_top_characters(reader)
    char_id = {}
    for n, i in enumerate(top_chars):
        char_id[i] = n
    file_obj.seek(0)
    line_counter = 0
    with open("sparse_vecs_new.txt", 'w') as o:
        for line in reader:
            if line_counter % 500 == 1:
                print("line", line_counter, "out of 14111 or so")
            if line:
                char_name = line[2]
                if char_name in top_chars:
                    one_hot_words_indices = words_one_hot(line[3], word_map)
                    oh = np.vstack((np.ones_like(one_hot_words_indices),
                                    np.ones_like(one_hot_words_indices) * line_counter,
                                    one_hot_words_indices))
                    af = additional_features(line[3])
                    af[1] = af[1] * line_counter
                    data, row, col = np.hstack((oh, af))
                    row, col = row.astype(int), col.astype(int)
                    sparse_vec = sparse((data, (row, col)))
                    o.write(str(sparse_vec))
                    o.write('\n')
                    o.write("label="+str(char_id[char_name]))
                    o.write('\n\n')
                    line_counter += 1


with open(kaggle_file, 'r') as k:
    create_sentence_vectors(k)
    a = 0



