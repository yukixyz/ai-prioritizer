import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class Featurizer:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=200)

    def fit(self, df):
        texts = (df['summary'].fillna('')+' '+df['description'].fillna('')+' '+df.get('remediation','').fillna(''))
        self.tfidf.fit(texts)

    def transform(self, df):
        texts = (df['summary'].fillna('')+' '+df['description'].fillna('')+' '+df.get('remediation','').fillna(''))
        X_text = self.tfidf.transform(texts).toarray()
        crit_map = {'low':0,'medium':1,'high':2,'critical':3}
        crit = df['asset_criticality'].map(crit_map).fillna(0).to_numpy().reshape(-1,1)
        cvss = df['cvss'].fillna(0).to_numpy().reshape(-1,1)
        X = np.hstack([cvss, crit, X_text])
        return X
