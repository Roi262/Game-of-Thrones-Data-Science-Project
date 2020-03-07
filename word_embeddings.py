from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from keras.preprocessing.text import Tokenizer


KAGGLE_FILE_PATH = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/kaggle_cleaned.csv"


def get_corpus_words():
    """returns a list of all the tokens in the corpus

    Arguments:
        corpus {[type]} -- [description]
    """
    corpus_tokens = []
    for line in open(KAGGLE_FILE_PATH, 'r'):
        if line.strip():
            line = line.split(';')
            corpus_tokens.extend(line[3].split())
    return corpus_tokens, len(corpus_tokens)


def get_one_hot():
    corpus_tokens, num_of_tokens = get_corpus_words()
    encoder = LabelEncoder()
    city_labels = encoder.fit_transform(corpus_tokens)
    encoder = OneHotEncoder(sparse=True)
    city_labels = city_labels.reshape((num_of_tokens, 1))
    # city_labels = city_labels.reshape((6, 1))
    k = encoder.fit_transform(city_labels)
    # print(k.indices)
    one_hot = []
    # g = len(k.indptr[0])
    for i in range(len(k.indptr) - 1):
        one_hot.append((k.indptr[i], k.indices[i]))
    print(one_hot)
    one_hot_vec_dim = len(corpus_tokens)
    return one_hot, one_hot_vec_dim


def create_emb_vectors(training_data, validation_data):
    tok = Tokenizer(num_words=10000)
    tok.fit_on_texts(training_data)
    X_train = tok.texts_to_sequences(training_data)
    X_test = tok.texts_to_sequences(validation_data)
    # Adding 1 because of reserved 0 index
    vocab_size = len(tok.word_index) + 1
    a = 0

# get_one_hot()
