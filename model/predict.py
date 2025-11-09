from joblib import load
import os
import numpy as np
import json
import shap

class Predictor:
    def __init__(self, artifacts_dir=os.path.join('model','artifacts')):
        model_path = os.path.join(artifacts_dir,'model.joblib')
        feat_path = os.path.join(artifacts_dir,'featurizer.joblib')
        label_path = os.path.join(artifacts_dir,'label_map.json')
        if not os.path.exists(model_path) or not os.path.exists(feat_path):
            from .train import train
            train()
        self.model = load(model_path)
        self.feat = load(feat_path)
        with open(label_path,'r') as f:
            self.label_map = json.load(f)

    def _score(self, X):
        probs = self.model.predict_proba(X)
        scores = np.dot(probs, [0,0.5,1.0])
        return scores

    def predict_single(self, row):
        import pandas as pd
        df = pd.DataFrame([row])
        X = self.feat.transform(df)
        score = float(self._score(X)[0])
        pred = int(self.model.predict(X)[0])
        expl = self._explain(X)
        return {'id': row.get('id'), 'score': score, 'priority': self.label_map.get(str(pred),'medium'), 'explanation': expl}

    def predict_batch(self, rows):
        import pandas as pd
        df = pd.DataFrame(rows)
        X = self.feat.transform(df)
        scores = self._score(X).tolist()
        preds = self.model.predict(X).tolist()
        expl = self._explain(X)
        out = []
        for i,row in enumerate(rows):
            out.append({'id': row.get('id'), 'score': float(scores[i]), 'priority': self.label_map.get(str(preds[i]),'medium')})
        return {'count': len(out), 'items': out, 'explanation_sample': expl}

    def _explain(self, X):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        mean_imp = [float(abs(v).mean()) for v in shap_values]
        return {'mean_feature_importance': mean_imp}
