import pandas as pd

DATA_PATH = "../data/Game of Thrones/kaggle_cleaned.csv"


def read_data():
    data_frame = pd.read_csv(DATA_PATH, delimiter=";", header=0)
    return data_frame.to_numpy()


if __name__ == "__main__":
    print(read_data())
