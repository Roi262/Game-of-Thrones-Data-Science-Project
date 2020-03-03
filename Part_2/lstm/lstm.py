import pandas as pd
import numpy as np
import re
import csv
import matplotlib.pyplot as plt

from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Embedding, SpatialDropout1D, LSTM, Dense, Input, Concatenate
from keras.models import Model
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from keras.utils import to_categorical
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from split_data_and_labels import TEXT_FILENAME, LABELS_FILENAME

import features
from configure import *

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

MAX_NB_WORDS = 50000
MAX_SEQUENCE_LENGTH = 250
EMBEDDING_DIM = 100

NUMBER_OF_CLASSES = 30

SPECIAL_FEATURES = 9


def create_vector_labels(labels):
    all_characters = set()
    for label in labels:
        for ch in label:
            all_characters.add(ch)
    number_of_labels = len(labels)
    number_of_characters = len(all_characters)
    all_characters = list(all_characters)
    all_characters_dict = {all_characters[i]: i for i in range(number_of_characters)}
    new_labels = np.zeros((number_of_labels, number_of_characters))
    for i, label in enumerate(labels):
        for ch in label:
            ch_idx = all_characters_dict[ch]
            new_labels[i, ch_idx] = 1
    return new_labels


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


def get_data_and_labels(data):
    data = clean_data()
    labels = np.load(LABELS_FILENAME, allow_pickle=True)
    return data, labels


def tokenize_words(data):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    lines = data[:, 6]
    tokenizer.fit_on_texts(lines)
    x = tokenizer.texts_to_sequences(lines)
    x = pad_sequences(x, maxlen=MAX_SEQUENCE_LENGTH)

    additional_2 = np.array([features.create_features(data[i]) for i in range(len(data))])
    x = np.hstack((x, additional_2))
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

def custom_loss_func(y_actual, y_predicted):
    if y_predicted in np.asarray(y_actual):
        return 0
    else:
        return 1


def build_model(input_length, number_of_classes):
    input_tensor = Input(shape=(input_length, ))
    tensor = Embedding(MAX_NB_WORDS, EMBEDDING_DIM)(input_tensor)
    tensor = SpatialDropout1D(0.2)(tensor)
    tensor = LSTM(100, dropout=0.5, recurrent_dropout=0.2)(tensor)
    second_input = Input(shape=(SPECIAL_FEATURES, ))
    tensor = Concatenate()([tensor, second_input])
    tensor = Dense(100, activation='relu')(tensor)
    tensor = Dense(number_of_classes, activation='softmax')(tensor)
    model = Model(inputs=[input_tensor, second_input], outputs=tensor)
    model.compile(loss='mse', optimizer='adam')
    print(model.summary())
    return model


    # model = Sequential()
    # model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=input_length))
    # model.add(SpatialDropout1D(0.2))
    # model.add(LSTM(100, dropout=0.5, recurrent_dropout=0.2))
    # model.add(Dense(number_of_classes, activation='softmax'))
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # return model


def train_model(model, x_train, y_train):
    epochs = 10
    batch_size = 64

    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
                        # callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])
    return history


def normalize_labels(labels):
    pass



if __name__ == "__main__":
    # path = CLEAN_DATA_PATH
    # with open('Part_2/part2_data_cleaned.csv', newline='') as f:
    data = pd.read_csv('Part_2/part2_data_cleaned.csv', delimiter=',', header=0).to_numpy()
    text_data, labels = data[:, :-1], data[:, -1]

    x = tokenize_words(text_data)
    labels = labels_to_numbers(labels)

    x, labels = remove_classes(x, labels)
    y = normalize_labels(labels)
    # y = to_categorical(labels, NUMBER_OF_CLASSES)

    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    model = build_model(MAX_SEQUENCE_LENGTH, NUMBER_OF_CLASSES)
    history = train_model(model, [x[:, :MAX_SEQUENCE_LENGTH], x[:, MAX_SEQUENCE_LENGTH:]], y)
    # accuracy = model.evaluate(x_test, y_test)
    # print("Accuracy:", accuracy)

    plt.title('Loss')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='validation')
    plt.legend()
    plt.show()

    plt.title('Accuracy')
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='validation')
    plt.legend()
    plt.show()