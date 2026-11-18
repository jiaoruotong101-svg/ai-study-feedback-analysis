from pathlib import Path
import json, hashlib, csv
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

root = Path(__file__).resolve().parent
model_dir = root.parent / 'feedback-baseline-20261026'
out = root.parent / 'human-evaluation-20261030'
out.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((model_dir/'frozen_manifest.json').read_text(encoding='utf-8'))
for name in ['model.joblib', 'config.json']:
    assert sha(model_dir/name) == manifest['files_sha256'][name]
source = root/'human_decisions_20261030.json'
rows = json.loads(source.read_text(encoding='utf-8'))
originals = json.loads((root/'blind_sample.json').read_text(encoding='utf-8'))
assert [(r['sample_id'],r['text']) for r in rows] == [(r['sample_id'],r['text']) for r in originals]
assert len(rows) == 180
bundle = joblib.load(model_dir/'model.joblib')
cfg = bundle['config']
X = bundle['vectorizer'].transform([r['text'] for r in rows])
prob = bundle['feedback_model'].predict_proba(X)[:,1]
pred = (prob >= cfg['binary_threshold']).astype(int)
names = cfg['trained_categories']
cp = {c:bundle['category_models'][c].predict_proba(X)[:,1] for c in names}
def score(y,p):
    return dict(n=len(y),positive_n=int(sum(y)),accuracy=float(accuracy_score(y,p)),precision=float(precision_score(y,p,zero_division=0)),recall=float(recall_score(y,p,zero_division=0)),f1=float(f1_score(y,p,zero_division=0)),macro_f1=float(f1_score(y,p,average='macro',zero_division=0)),confusion=confusion_matrix(y,p,labels=[0,1]).tolist())
records=[]
for i,r in enumerate(rows):
    y={'有':1,'无':0,'不确定':None}[r['feedback']]
    cats=r['categories'].split('；')
    partial='待定' in cats or '其他候选' in cats
    targets={c:None if y is None else 0 if y==0 else 1 if c in cats else None if partial else 0 for c in names}
    predictions={c:int(pred[i] and cp[c][i]>=cfg['category_threshold']) for c in names}
    records.append({**r,'human_binary':y,'human_targets':targets,'model_binary':int(pred[i]),'model_probability':float(prob[i]),'model_categories':predictions,'category_probabilities':{c:float(cp[c][i]) for c in names},'binary_disagreement':None if y is None else y!=int(pred[i]),'category_disagreements':[c for c in names if targets[c] is not None and targets[c]!=predictions[c]]})
eligible=[r for r in records if r['human_binary'] is not None]
y=[r['human_binary'] for r in eligible];p=[r['model_binary'] for r in eligible]
metrics={'method':'Human final decisions with AI translations and label-specific options; frozen model predictions unseen during labeling','binary':score(y,p),'always_negative_baseline':score(y,[0]*len(y)),'categories':{},'excluded_binary':[r['sample_id'] for r in records if r['human_binary'] is None]}
flat_y=[];flat_p=[]
for c in names:
    known=[r for r in records if r['human_targets'][c] is not None]
    cy=[r['human_targets'][c] for r in known];pp=[r['model_categories'][c] for r in known]
    metrics['categories'][c]=score(cy,pp)
    flat_y+=cy;flat_p+=pp
metrics['category_micro']={'observed_cells':len(flat_y),'precision':float(precision_score(flat_y,flat_p,zero_division=0)),'recall':float(recall_score(flat_y,flat_p,zero_division=0)),'f1':float(f1_score(flat_y,flat_p,zero_division=0))}
metrics['verification']={'model_hash_unchanged':sha(model_dir/'model.joblib')==manifest['files_sha256']['model.joblib'],'human_labels_sha256':sha(source),'script_sha256':sha(Path(__file__)),'n_predictions':len(records),'no_fit_or_tuning':True}
(out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8')
with (out/'逐条对照.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['编号','原文','人工选择','人工反馈','人工类别','人工理由与待定','模型反馈','模型类别','二分类是否一致','类别不一致项'])
    for r in records:
        w.writerow([r['sample_id'],r['text'],r['choice'],r['feedback'],r['categories'],r['note'],'有' if r['model_binary'] else '无','；'.join(c for c in names if r['model_categories'][c]) or '无','待定不计分' if r['binary_disagreement'] is None else '否' if r['binary_disagreement'] else '是','；'.join(r['category_disagreements'])])
assert len((out/'predictions.jsonl').read_text(encoding='utf-8').splitlines())==180
print(json.dumps(metrics,ensure_ascii=True))
