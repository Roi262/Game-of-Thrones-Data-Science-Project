import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
import matplotlib.pyplot as plt

epochs = 20
embedding_dim = 50
maxlen = 100
vocab_size = 5000

NUMBER_OF_CLASSES = 30


def load_data():
    data = np.load("text.npy", allow_pickle=True)
    labels = np.load("labels.npy", allow_pickle=True)
    return data, labels


def clean_data(data):
    return data


def get_number_labels(labels):
    labels_map = {}
    curr_index = 0
    for label in labels:
        if label not in labels_map.keys():
            labels_map[label] = curr_index
            curr_index += 1
    number_labels = np.array([labels_map[label] for label in labels])
    return number_labels


def remove_classes(data, labels):
    labels = get_number_labels(labels)
    bins = np.arange(np.max(labels) + 1)
    histogram, bins = np.histogram(labels, bins=bins)
    max_labels = np.array(list(reversed(np.argsort(histogram))))[:NUMBER_OF_CLASSES]
    indexes = np.array([i for i in range(len(labels)) if labels[i] in max_labels])
    new_data, new_labels = data[indexes], labels[indexes]
    return new_data, new_labels


def tokenize_words(data):
    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(data)
    data = tokenizer.texts_to_sequences(data)
    data = pad_sequences(data, maxlen=maxlen)
    return data


def build_model():
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=maxlen))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(10, activation='relu'))
    model.add(Dense(NUMBER_OF_CLASSES, activation='softmax'))
    model.summary()
    return model


def train_model(model, x_train, y_train, x_test, y_test):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test, y_test), batch_size=10)
    return history


def plot_history(history):
    # acc = history.history['accuracy']
    # val_acc = history.history['val_accuracy']
    # loss = history.history['loss']
    # val_loss = history.history['val_loss']
    # x = range(1, len(acc) + 1)
    #
    # plt.figure(figsize=(12, 5))
    # plt.subplot(1, 2, 1)
    # plt.plot(x, acc, 'b', label='Training accuracy')
    # plt.plot(x, val_acc, 'r', label='Validation accuracy')
    # plt.title('Training and validation accuracy')
    # plt.legend()
    # plt.subplot(1, 2, 2)
    # plt.plot(x, loss, 'b', label='Training loss')
    # plt.plot(x, val_loss, 'r', label='Validation loss')
    # plt.title('Training and validation loss')
    # plt.legend()
    # plt.show()

    accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']
    loss = history.history['loss']
    validation_loss = history.history['val_loss']

    x_axis = np.arange(epochs) + 1

    plt.figure()
    plt.plot(x_axis, accuracy, label="Training accuracy")
    plt.plot(x_axis, validation_accuracy, label="Validation accuracy")
    plt.title("Training and validation accuracy")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(x_axis, loss, label="Training loss")
    plt.plot(x_axis, validation_loss, label="Validation loss")
    plt.title("Training and validation loss")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    data, labels = load_data()
    data = clean_data(data)
    data = tokenize_words(data)
    data, labels = remove_classes(data, labels)
    labels = get_number_labels(labels)

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.1)

    model = build_model()
    history = train_model(model, x_train, y_train, x_test, y_test)

    loss, accuracy = model.evaluate(x_train, y_train)
    print("Training Accuracy: {:.4f}".format(accuracy))
    loss, accuracy = model.evaluate(x_test, y_test)
    print("Testing Accuracy:  {:.4f}".format(accuracy))
    plot_history(history)
