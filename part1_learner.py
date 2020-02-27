import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('sentence_vectors.csv').to_numpy()
X, y = df.iloc[0:-1, :-1]
