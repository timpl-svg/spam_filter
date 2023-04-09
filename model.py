import pandas as pd
from sklearn.model_selection import train_test_split
from spam_bayes import NaiveBayesSpamFilter
import pickle


spam_filter = NaiveBayesSpamFilter()
df = pd.read_csv("./dataset/spamraw.csv")

train_df, test_df = train_test_split(df, test_size=0.1, random_state=42, stratify=df["type"])
train_spam = train_df[train_df["type"] == "spam"]["text"].to_numpy()
train_ham = train_df[train_df["type"] == "ham"]["text"].to_numpy()
test = test_df["text"].to_numpy()
targets = test_df["type"].to_numpy()

spam_filter.fit(train_spam, train_ham)

pickle.dump(spam_filter, open("model.pkl", "wb"))


