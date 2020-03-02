import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Embedding, SpatialDropout1D, LSTM, Dense
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from keras.utils import to_categorical
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from split_data_and_labels import TEXT_FILENAME, LABELS_FILENAME

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

MAX_NB_WORDS = 50000
MAX_SEQUENCE_LENGTH = 250
EMBEDDING_DIM = 100

NUMBER_OF_CLASSES = 30


def remove_classes(text, labels):
    rows_ind = []
    bins = range(np.max(labels))
    histogram, bins = np.histogram(labels, bins=bins)
    arg = np.array(list(reversed(np.argsort(histogram))))
    indexes = arg[:NUMBER_OF_CLASSES]
    for i in range(len(labels)):
        if labels[i] in indexes:
            rows_ind.append(i)
    rows_ind = np.array(rows_ind)
    text = text[rows_ind]
    labels = labels[rows_ind]
    labels = np.array([np.where(indexes == labels[i])[0] for i in range(len(labels))]).reshape((-1,))
    return text, labels


def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ',
                                   text)  # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('',
                              text)  # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # remove stopwors from text
    text = text.replace("\\d+", "")
    return text


def clean_data():
    text = np.load(TEXT_FILENAME, allow_pickle=True)
    text = np.array(list(map(clean_text, text)))
    return text


def get_data_and_labels():
    data = clean_data()
    labels = np.load(LABELS_FILENAME, allow_pickle=True)
    return data, labels


def tokenize_words(data):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(data)
    x = tokenizer.texts_to_sequences(data)
    x = pad_sequences(x, maxlen=MAX_SEQUENCE_LENGTH)
    return x


def labels_to_numbers(labels):
    labels_dict = {}
    curr_idx = 0
    for label in labels:
        if label not in labels_dict.keys():
            labels_dict[label] = curr_idx
            curr_idx += 1
    numbers = np.array([labels_dict[label] for label in labels])
    return numbers


def build_model(input_length, number_of_classes):
    model = Sequential()
    model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=input_length))
    model.add(SpatialDropout1D(0.2))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(number_of_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train_model(model, x_train, y_train):
    epochs = 5
    batch_size = 64

    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1,
                        callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])
    return history


if __name__ == "__main__":
    text_data, labels = get_data_and_labels()
    x = tokenize_words(text_data)
    labels = labels_to_numbers(labels)

    x, labels = remove_classes(x, labels)
    y = to_categorical(labels, NUMBER_OF_CLASSES)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    model = build_model(x.shape[1], NUMBER_OF_CLASSES)
    history = train_model(model, x_train, y_train)
    accuracy = model.evaluate(x_test, y_test)
    print("Accuracy:", accuracy)

    plt.title('Loss')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()

    plt.title('Accuracy')
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='test')
    plt.legend()
    plt.show()
