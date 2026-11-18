"""Select the human test only after the model is frozen; never generate its labels."""
from pathlib import Path
from collections import defaultdict, Counter
from difflib import SequenceMatcher
import hashlib, json, re, sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
root = Path(__file__).resolve().parent.parent
base = root/'genai-edsent-audit-20261016'
out = root/'human-test180-20261026'
out.mkdir(exist_ok=True)
frozen_path = root/'feedback-baseline-20261026/frozen_manifest.json'
frozen = json.loads(frozen_path.read_text(encoding='utf-8'))
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,digest in frozen['files_sha256'].items():
    assert sha(frozen_path.parent/name)==digest
norm = lambda s:' '.join(re.findall(r'\w+',str(s).lower()))
read = lambda p:[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
known=[]
for p in [base/'review-expanded/reviewed_all270.jsonl',base/'sample.jsonl',base/'baseline_errors.jsonl',root/'calibration60-20261022/sample_metadata.jsonl',root/'ai-label-candidates-20261024/train_metadata.jsonl',root/'ai-label-candidates-20261024/development_metadata.jsonl']:
    known.extend(read(p))
known.extend(json.loads((base/'issue_examples.json').read_text(encoding='utf-8')))
known_ids={str(r['review_reviewId']) for r in known if r.get('review_reviewId')}
known_plain={norm(r['text']) for r in known}
exclusion_path=out/'language_screen_exclusions.json'
exclusions=json.loads(exclusion_path.read_text(encoding='utf-8')) if exclusion_path.exists() else {}
d=pd.read_parquet(base/'study_subset_82004.parquet')
d['plain']=d.text.map(norm)
d=d[~d.review_reviewId.astype(str).isin(known_ids)&~d.plain.isin(known_plain)].drop_duplicates('plain').drop_duplicates('review_reviewId').copy()
def prefilter(s):
    chars=[c for c in s if c.isalpha()]
    return bool(chars) and sum(c.isascii() for c in chars)/len(chars)>=.95
d=d[d.text.map(prefilter)].copy()
d['stratum']=d.review_score.map(lambda s:'low' if s<=2 else 'mid' if s==3 else 'high')
texts=list(known_plain)
grams=[{t[k:k+3] for k in range(len(t)-2)} for t in texts]
index=defaultdict(list)
for i,gs in enumerate(grams):
    for g in gs:index[g].append(i)
near_rejected=[]
def near_duplicate(t):
    gs={t[k:k+3] for k in range(len(t)-2)}
    hits=Counter(j for g in gs for j in index[g])
    for j,overlap in hits.items():
        if min(len(t),len(texts[j]))>=20 and overlap/(len(gs)+len(grams[j])-overlap)>=.70 and SequenceMatcher(None,t,texts[j],autojunk=False).ratio()>=.92:
            return True
    idx=len(texts);texts.append(t);grams.append(gs)
    for g in gs:index[g].append(idx)
    return False
selected=[];groups=[]
for gi,((app,stratum),group) in enumerate(d.groupby(['app_name','stratum'],sort=True)):
    ordered=group.sort_values('review_reviewId').sample(frac=1,random_state=2026102600+gi)
    part=[]
    for r in ordered.to_dict('records'):
        if str(r['review_reviewId']) in exclusions:continue
        if near_duplicate(r['plain']):
            near_rejected.append(str(r['review_reviewId']));continue
        part.append(r)
        if len(part)==10:break
    assert len(part)==10,(app,stratum,len(part))
    selected.extend(part);groups.append({'app':app,'stratum':stratum,'n':len(part)})
frame=pd.DataFrame(selected).sample(frac=1,random_state=2026102699).reset_index(drop=True)
frame.insert(0,'sample_id',[f'H{i:03}' for i in range(1,181)])
assert len(frame)==180 and frame.review_reviewId.nunique()==180
assert not set(frame.plain)&known_plain
frame.to_json(out/'sample_metadata.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
blind=frame[['sample_id','text']].to_dict('records')
(out/'blind_sample.json').write_text(json.dumps(blind,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'date':'2026-10-26','n':180,'groups':groups,'seed_base':2026102600,'shuffle_seed':2026102699,'known_unique_text_n':len(known_plain),'excluded_known_ids_n':len(known_ids),'language_exclusion_n':len(exclusions),'near_duplicate_rejected_ids':near_rejected,'language_status':'ASCII prefilter plus assistant language-only screen; human may still mark partial or unable','model_frozen_manifest_sha256':sha(frozen_path),'model_sha256':sha(frozen_path.parent/'model.joblib'),'rules_sha256':sha(root/'calibration60-20261022/校准复盘与AI标注规则v0.3.md'),'blind_sample_sha256':sha(out/'blind_sample.json'),'metadata_sha256':sha(out/'sample_metadata.jsonl'),'human_labels_created':False,'model_predictions_created':False,'evaluation_plan':'After all human entries are saved, evaluate the frozen model without fitting, threshold changes or class changes. Report valid sample coverage, binary metrics, masked category metrics, uncertainty counts, and sample limitations. Any later tuning is post-test development, not a fresh independent result.'}
(out/'sampling_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'n':180,'language_excluded':len(exclusions),'near_rejected':len(near_rejected)},ensure_ascii=False))
