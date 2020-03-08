import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from load_feature_vectors import load_feature_vectors


def train_k_nearest(k, train_data, train_labels):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(train_data, train_labels)
    return knn


def knn(k):
    # Take random 80% of the data and train knn with it
    training_data, training_labels, test_data, test_labels = load_feature_vectors(True)
    model = train_k_nearest(k, training_data, training_labels)

    # Predict clustering of the testing data and compare to labels
    predicted_labels = np.asarray(model.predict(test_data))
    correct_predictions_count = np.count_nonzero(predicted_labels == test_labels)
    return 100 * correct_predictions_count / len(test_labels)


if __name__ == "__main__":
    print("Loaded vectors")
    ticks = [1, 2, 3, 4, 5, 6, 7, 8, 9,
             10, 20, 30, 40, 50, 60, 70, 80, 90,
             100, 200, 300, 400, 500, 600, 700, 800, 900,
             1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    acc_data = []
    for k_arg in ticks:
        acc_data.append(knn(k_arg))
        print(k_arg, acc_data[-1])
    plt.plot(ticks, acc_data)
    plt.xscale("log")
    plt.show()

