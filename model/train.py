import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump
from .feature_engineering import Featurizer
import os

def train(data_path='data/sample_findings.csv', out_dir='model/artifacts'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    label_map = {'low':0,'medium':1,'high':2}
    df['label_num'] = df['label'].map(label_map).fillna(1)
    fe = Featurizer()
    fe.fit(df)
    X = fe.transform(df)
    y = df['label_num'].to_numpy()
    clf = GradientBoostingClassifier(n_estimators=100)
    clf.fit(X, y)
    dump(clf, os.path.join(out_dir,'model.joblib'))
    dump(fe, os.path.join(out_dir,'featurizer.joblib'))
    with open(os.path.join(out_dir,'label_map.json'),'w') as f:
        f.write('{"0":"low","1":"medium","2":"high"}')

if __name__ == '__main__':
    train()
