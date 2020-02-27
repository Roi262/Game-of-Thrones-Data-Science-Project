import csv
import nltk


def all_harrys_lines():
    with open("data\\HPMovies\\HP1.csv", 'r') as f:
        harrys_quotes = ""
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == "Harry" or row[0] == "harry":
                harrys_quotes = harrys_quotes + row[1]
        return harrys_quotes


def generate_model(cfdist, word, num=15):
    for i in range(num):
        print(word, end=' ')
        word = cfdist[word].max()


text = all_harrys_lines().split(" ")
bigrams = nltk.bigrams(text)
cfd = nltk.ConditionalFreqDist(bigrams)
generate_model(cfd, 'A')
