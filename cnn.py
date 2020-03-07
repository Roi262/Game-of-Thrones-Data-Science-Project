import matplotlib.pyplot as plt
from word_embeddings import get_one_hot
from keras.preprocessing.text import Tokenizer
from keras import Sequential, layers

KAGGLE_FILE_PATH = "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/kaggle_cleaned.csv"

EMBEDDING_DIMENSION = 50

def get_data():
    x = []
    y = []
    for line in open(KAGGLE_FILE_PATH, 'r'):
        if line:
            line = line.split(';')
            x.append(line[3])  # Quotes are input data
            y.append(line[2])  # Character's names are desired output
    return x, y


def plot_history(history):
    """[summary]
    
    Arguments:
        history {[type]} -- [description]
    """
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training acc')
    plt.plot(x, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()


def build_model(vocab_size, embedding_dim, input_len):
    """[summary]
    
    Arguments:
        vocab_size {[type]} -- [description]
        embedding_dim {[type]} -- [description]
        input_len {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    model = Sequential()
    model.add(layers.Embedding(vocab_size, embedding_dim, input_len))
    model.add(layers.Conv1D(128, 5, activation='relu'))
    model.add(layers.GlobalMaxPooling1D())
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(1, activation='softmax'))
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    return model


def train_model(model, x, y):
    """[summary]
    
    Arguments:
        model {[type]} -- [description]
        x {[type]} -- [description]
        y {[type]} -- [description]
    """
    history = model.fit(x, y, epochs=20, validation_split=0.2,
                        batch_size=10, verbose=1)
    loss, accuracy = model.evaluate(x, y, verbose=False)
    print("Training Accuracy: {: .4f}".format(accuracy))
    loss, accuracy = model.evaluate(x, y, verbose=False)
    print("Testing Accuracy:{: .4f}".format(accuracy))
    plot_history(history)

def main():
    data = get_data()
    number_of_sentences = len(data[0])
    train_ind = int(0.8 * number_of_sentences)
    val_index = int(0.9 * number_of_sentences)
    training_data, training_labels = data[0][:train_ind], data[1][:train_ind]
    validation_data, validation_labels = data[0][train_ind: val_index], data[1][train_ind: val_index]
    test_data, test_labels = data[0][val_index:], data[1][val_index:]
    
    one_hot_vecs, feature_vec_length = get_one_hot()
    model = build_model(number_of_sentences, EMBEDDING_DIMENSION, feature_vec_length)
    train_model(model, training_data, training_labels)

if __name__ == "__main__":
    main()
