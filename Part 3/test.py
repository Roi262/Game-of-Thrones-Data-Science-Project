import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


sid = SentimentIntensityAnalyzer()

def get_vader_score(sent):
    # Polarity score returns dictionary
    ss = sid.polarity_scores(sent)
    for k in sorted(ss):
        
        print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
    return ss['compound']

g = get_vader_score("i love chips")
print('\n', g)
