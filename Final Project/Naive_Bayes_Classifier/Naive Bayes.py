import numpy as np
import pandas as pd
from nltk import *
import string
import pickle


#  remove matched patterns from string
def remove_pattern(input_txt, pattern):
    try:
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(re.escape(i), '', input_txt)
    finally:
        pass
    return input_txt


#  get sentiment train data
train_data = pd.read_csv('train.csv', nrows=1000000, encoding="ISO-8859-1")


index2 = 0
train_source = {'Content': [], 'Sentiment': []}
for data in train_data['Content']:
    if (index2 % 1 == 0):
        train_source['Content'].append(train_data['Content'][index2])
        train_source['Sentiment'].append(train_data['Sentiment'][index2])
    index2 = index2 + 1
train = pd.DataFrame(train_source)

#  get test data
test_data = pd.read_csv('test.csv', nrows=10000, encoding="ISO-8859-1")

try:
    #  remove @
    train['FilterContent'] = np.vectorize(remove_pattern)(train['Content'], "@[\w]*")
    test_data['FilterContent'] = np.vectorize(remove_pattern)(test_data['Content'], "@[\w]*")
finally:
    pass

try:
    #  remove http
    train['FilterContent'] = np.vectorize(remove_pattern)(train['FilterContent'],
                                                          "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    test_data['FilterContent'] = np.vectorize(remove_pattern)(test_data['FilterContent'],
                                                          "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
finally:
    pass

try:
    #  remove punctuation
    train['FilterContent'] = train['FilterContent'].str.replace("[^a-zA-Z#]", " ")
    test_data['FilterContent'] = test_data['FilterContent'].str.replace("[^a-zA-Z#]", " ")
finally:
    pass

#  remove words less than three
train['FilterContent'] = train['FilterContent'].apply(lambda x: ' '.join([w.lower() for w in x.split() if len(w) >= 3]))
test_data['FilterContent'] = test_data['FilterContent'].apply(lambda x: ' '.join([w.lower() for w in x.split() if len(w) >= 3]))

index = 0
index1 = 0
test_tweets = []

#  get stop words
sentiment_content = []
f = open(r"stopwords.txt")
lines = f.readlines()
stop = []
for line in lines:
    line = line.strip('\n')
    stop.append(line)
f.close()

#  remove stop words and do stemming
for content in train['FilterContent']:
    tokenscontent = TweetTokenizer(content)
    tokens = tokenscontent.tokenize(content)
    porter = PorterStemmer()
    stems = [porter.stem(t) for t in tokens]
    tokens_filtered = [w for w in stems if w.lower() not in stop and w.lower() not in string.punctuation]
    str = ""
    for tokens_filtered_each in tokens_filtered:
        str = str + " " + tokens_filtered_each
    #  get content and corresponding sentiment classification and store in sentiment_content
    if(index % 10 == 0):
        if (train['Sentiment'][index] == 0):
            sentiment_content.append((str, 'negative'))
        elif (train['Sentiment'][index] == 4):
            sentiment_content.append((str, 'positive'))
        elif (train['Sentiment'][index] == 2):
            sentiment_content.append((str, 'neutral'))
    index = index + 1

for content in test_data['FilterContent']:
    tokenscontent = TweetTokenizer(content)
    tokens = tokenscontent.tokenize(content)
    porter = PorterStemmer()
    stems = [porter.stem(t) for t in tokens]
    tokens_filtered = [w for w in stems if w.lower() not in stop and w.lower() not in string.punctuation]
    str = ""
    for tokens_filtered_each in tokens_filtered:
        str = str + " " + tokens_filtered_each
    #  get content and corresponding sentiment classification and store in test_tweets
    if (test_data['Sentiment'][index1] == 0):
        test_tweets.append((str, 'negative'))
    elif (test_data['Sentiment'][index1] == 2):
        test_tweets.append((str, 'neutral'))
    elif (test_data['Sentiment'][index1] == 4):
        test_tweets.append((str, 'positive'))
    index1 = index1 + 1

#  get words set and store corresponding sentiment classification in tweets
tweets = []
for (words, sentiment) in sentiment_content:
    words_filtered = [e.lower() for e in words.split()]
    tweets.append((words_filtered, sentiment))


#  get all words
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words += words
    return all_words


all_words = get_words_in_tweets(tweets)


#  get high frequence words
def get_word_features(wordlist):
    wordlist = FreqDist(wordlist)
    word_features = [w for (w, c) in wordlist.most_common(30000)]
    return word_features


word_features = get_word_features(get_words_in_tweets(tweets))


#  extract features
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


#  train data set and extract features
training_set = [(extract_features(d), c) for (d, c) in tweets]

#  Naive Bayes classifier
classifier = NaiveBayesClassifier.train(training_set)

#  show features
classifier.show_most_informative_features(100)
'''

#  use trained Naive Bayes classifier
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

'''
#  use Naive Bayes classifier to do test
all_num = 0
right_num = 0
index2 = 0
for (t, classify_sentiment) in test_tweets:
    print ("{0} : {1}".format(t, classifier.classify(extract_features([e.lower() for e in t.split() if len(e) >= 3]))))
    naive_classify = classifier.classify(extract_features([e.lower() for e in t.split() if len(e) >= 3]))
    if ( naive_classify == classify_sentiment):
        right_num = right_num + 1
    all_num = all_num + 1
print("accuracy is %f" % (right_num/all_num))

#  store trained Naive Bayes classifier
f = open('naive_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()
