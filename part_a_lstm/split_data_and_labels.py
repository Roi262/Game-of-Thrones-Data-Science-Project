from data_reader import read_data
import numpy as np

SPEAKER_COL = 2
TEXT_COL = 3
TEXT_FILENAME = "text.npy"
LABELS_FILENAME = "labels.npy"


def split():
    data = read_data()
    speaker = data[:, SPEAKER_COL]
    text = data[:, TEXT_COL]
    np.save(TEXT_FILENAME, text)
    np.save(LABELS_FILENAME, speaker)


if __name__ == "__main__":
    split()
