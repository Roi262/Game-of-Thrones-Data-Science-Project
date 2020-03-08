from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict


kaggle_file = "/cs/usr/tamar.yov/Desktop/final_project/" \
              "Data-Science---Final-Project/data/Game of Thrones/kaggle_cleaned.csv"

def isStopWord(word):
    return word in set(stopwords.words('english'))


def find_word_freq():
    with open(kaggle_file, 'r') as reader:
        ps = PorterStemmer()
        d = defaultdict(int)
        prev = []
        for row in reader:
            if row.strip():
                ep = row[:2]
                if ep != prev:
                    print(ep)
                prev = ep
                text = row.split(";")[3]
                text = text.replace(".", " ").replace(",", " ").replace("?", " ").replace("!", " ")
                text = text.replace("\"", " ").replace("-", " ").replace("\n", " ")
                for word in text.split(" "):
                    word = ps.stem(word)
                    if not isStopWord(word):
                        d[word.lower()] += 1
        return d


di = find_word_freq()
words = [e[0] for e in sorted(di.items(), key=lambda x:x[1], reverse=True)]
with open("new_word_map.txt", 'w') as out:
    for word in words:
        out.write(word + '\n')

