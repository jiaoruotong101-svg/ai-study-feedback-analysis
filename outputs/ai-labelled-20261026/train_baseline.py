"""CPU baseline. Development labels are AI-assisted, not an independent test."""
from pathlib import Path
import hashlib, json, sys, warnings
import numpy as np
import sklearn, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.exceptions import ConvergenceWarning

sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('error', category=ConvergenceWarning)
src = Path(__file__).resolve().parent
out = src.parent / 'feedback-baseline-20261026'
out.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read_jsonl = lambda p: [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
rows = read_jsonl(src/'all_annotations.jsonl')
train = [r for r in rows if r['split']=='train' and r['eligible_binary']]
dev = [r for r in rows if r['split']=='development' and r['eligible_binary']]
assert len(train)==1721 and len(dev)==347
assert not {r['sample_id'] for r in train} & {r['sample_id'] for r in dev}
assert not {r['text'].lower().strip() for r in train} & {r['text'].lower().strip() for r in dev}
names = ['回答与任务完成','收费与权益','运行体验','界面与广告']
config = {'vectorizer':{'ngram_range':[1,2],'min_df':2,'max_features':20000,'sublinear_tf':True},'classifier':{'C':1.0,'class_weight':'balanced','solver':'liblinear','max_iter':1000,'random_state':20261026},'binary_threshold':0.5,'category_threshold':0.5,'category_prediction_gate':'feedback_probability >= 0.5','trained_categories':names,'withheld_category':'入门求助','withheld_reason':'Only 5 train and 1 development positives; descriptive cases only.','fitting_scope':'Vectorizer fit on train text only; each category fit only on observed targets; null labels never converted to negative.','selection':'One predeclared configuration; no search or threshold tuning on development or human test.'}
vectorizer = TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=20000,sublinear_tf=True)
X = vectorizer.fit_transform([r['text'] for r in train])
D = vectorizer.transform([r['text'] for r in dev])
y = np.array([r['feedback'] for r in train])
yd = np.array([r['feedback'] for r in dev])
binary = LogisticRegression(**config['classifier']).fit(X,y)
prob = binary.predict_proba(D)[:,1]
pred = (prob>=.5).astype(int)
models, train_masks, category_prob, per_class = {}, {}, {}, {}
def scores(y,p):
    return {'n':len(y),'positive_n':int(sum(y)),'accuracy':float(accuracy_score(y,p)),'positive_precision':float(precision_score(y,p,zero_division=0)),'positive_recall':float(recall_score(y,p,zero_division=0)),'positive_f1':float(f1_score(y,p,zero_division=0)),'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'confusion_matrix_true_rows_pred_cols_0_1':confusion_matrix(y,p,labels=[0,1]).tolist()}
flat_y,flat_p = [],[]
for c in names:
    ti = [i for i,r in enumerate(train) if r['category_targets'][c] is not None]
    di = [i for i,r in enumerate(dev) if r['category_targets'][c] is not None]
    assert all(train[i]['category_targets'][c] in [0,1] for i in ti)
    yc = np.array([train[i]['category_targets'][c] for i in ti])
    dc = np.array([dev[i]['category_targets'][c] for i in di])
    models[c] = LogisticRegression(**config['classifier']).fit(X[ti],yc)
    train_masks[c] = {'sample_ids':[train[i]['sample_id'] for i in ti],'positive_n':int(sum(yc))}
    category_prob[c] = models[c].predict_proba(D)[:,1]
    cp = ((category_prob[c]>=.5)&(pred==1)).astype(int)
    per_class[c] = scores(dc,cp[di])
    flat_y.extend(dc.tolist());flat_p.extend(cp[di].tolist())
majority = int(np.bincount(y).argmax())
metrics = {'evaluation_type':'development_agreement_with_AI_labels_NOT_human_test','binary_majority_baseline':scores(yd,np.full(len(yd),majority)),'binary_tfidf_logistic_regression':scores(yd,pred),'four_categories_masked_end_to_end':per_class,'four_categories_masked_micro':{'precision':float(precision_score(flat_y,flat_p,zero_division=0)),'recall':float(recall_score(flat_y,flat_p,zero_division=0)),'f1':float(f1_score(flat_y,flat_p,zero_division=0)),'observed_cells':len(flat_y)},'warnings':['Same-assistant training/development labels may share systematic errors.','These scores cannot establish human-level accuracy or population prevalence.','入门求助 is not trained or included in category metrics.']}
bundle = {'vectorizer':vectorizer,'feedback_model':binary,'category_models':models,'config':config}
joblib.dump(bundle,out/'model.joblib')
loaded = joblib.load(out/'model.joblib')
assert np.allclose(prob,loaded['feedback_model'].predict_proba(loaded['vectorizer'].transform([r['text'] for r in dev]))[:,1])
for c in names:
    assert np.allclose(category_prob[c],loaded['category_models'][c].predict_proba(D)[:,1])
predictions = []
for i,r in enumerate(dev):
    cp = {c:int(pred[i]==1 and category_prob[c][i]>=.5) for c in names}
    cp['入门求助'] = None
    predictions.append({'sample_id':r['sample_id'],'feedback_probability':float(prob[i]),'feedback_prediction':int(pred[i]),'category_predictions':cp,'category_probabilities':{c:float(category_prob[c][i]) for c in names},'ai_feedback_label':r['feedback'],'ai_category_targets':r['category_targets']})
(out/'development_predictions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in predictions),encoding='utf-8')
assert read_jsonl(out/'development_predictions.jsonl') == predictions
for name,data in [('config.json',config),('development_metrics.json',metrics),('category_training_masks.json',train_masks)]:
    (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
manifest = {'date':'2026-10-26','status':'baseline_configuration_and_model_frozen_before_human_test','python':sys.version,'sklearn':sklearn.__version__,'train_n':len(train),'development_n':len(dev),'vocabulary_n':len(vectorizer.vocabulary_),'training_labels_sha256':sha(src/'all_annotations.jsonl'),'label_manifest_sha256':sha(src/'label_manifest.json'),'script_sha256':sha(Path(__file__)),'files_sha256':{p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='frozen_manifest.json'},'validation':{'serialized_model_predictions_match':True,'train_development_id_overlap':0,'null_target_mask_checked':True,'development_predictions_readback_match':True},'human_test':{'target_n':180,'selected':False,'labels_created':False,'evaluated':False}}
(out/'frozen_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'train_n':len(train),'development_n':len(dev),'vocabulary_n':len(vectorizer.vocabulary_),'metrics':metrics},ensure_ascii=False))
