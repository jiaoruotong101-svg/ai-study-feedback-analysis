from pathlib import Path
import pandas as pd
import json, re, hashlib, difflib

base=Path('D:/projects/Study/outputs/genai-edsent-audit-20261016')
out=Path('D:/projects/Study/outputs/calibration60-20261022')
out.mkdir(exist_ok=True)
norm=lambda s:' '.join(str(s).lower().split())
punct=lambda s:' '.join(re.findall(r'\w+',norm(s)))
known=[]
for p in [base/'review-expanded/reviewed_all270.jsonl',base/'sample.jsonl',base/'baseline_errors.jsonl']:
    known.extend(json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip())
known.extend(json.loads((base/'issue_examples.json').read_text(encoding='utf-8')))
seen={norm(r['text']) for r in known}
seen_ids={str(r['review_reviewId']) for r in known if r.get('review_reviewId')}
seen_punct={punct(r['text']) for r in known}
d=pd.read_parquet(base/'study_subset_82004.parquet')
total=len(d)
d['norm']=d.text.map(norm)
d=d[~d.norm.isin(seen)&~d.review_reviewId.astype(str).isin(seen_ids)].copy()
d=d.drop_duplicates('norm').drop_duplicates('review_reviewId')
# Mechanical script check only; romanized and mixed language requires reading.
def latin_fraction(s):
    letters=[c for c in str(s) if c.isalpha()]
    return sum(c.isascii() for c in letters)/len(letters) if letters else 0
d=d[d.text.map(latin_fraction).ge(.95)].copy()
d['stratum']=d.review_score.map(lambda s:'low' if s<=2 else 'mid' if s==3 else 'high')
apps=sorted(d.app_name.unique())
strata=['low','mid','high']
reject_path=out/'language_exclusions.json'
reject=json.loads(reject_path.read_text(encoding='utf-8')) if reject_path.exists() else {}
selected=[]; skipped=[]; comparisons=list(seen_punct)
for app_i,app in enumerate(apps):
    for stratum_i,stratum in enumerate(strata):
        target=4 if stratum_i==app_i%3 else 3
        group=d[(d.app_name==app)&(d.stratum==stratum)].sort_values('review_reviewId').sample(frac=1,random_state=20261022+app_i*3+stratum_i)
        n=0
        for row in group.to_dict('records'):
            ident=str(row['review_reviewId']); text=punct(row['text'])
            if ident in reject:
                skipped.append({'id':ident,'reason':reject[ident]}); continue
            near=any(text==old or (len(text)>=40 and min(len(text),len(old))/max(len(text),len(old))>=.92 and difflib.SequenceMatcher(None,text,old,autojunk=False).ratio()>=.92) for old in comparisons)
            if near:
                skipped.append({'id':ident,'reason':'exact or >=0.92 sequence similarity after punctuation normalization'}); continue
            selected.append(row); comparisons.append(text);n+=1
            if n==target: break
        assert n==target
x=pd.DataFrame(selected).sample(frac=1,random_state=2026102201).reset_index(drop=True)
x.insert(0,'sample_id',[f'C{i:03}' for i in range(1,61)])
assert len(x)==60 and x.norm.nunique()==60 and x.review_reviewId.nunique()==60
assert x.groupby('app_name').size().eq(10).all()
assert x.groupby('stratum').size().eq(20).all()
assert not set(x.norm)&seen
x.to_json(out/'sample_metadata.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
blind=x[['sample_id','text']].to_dict('records')
(out/'blind_sample.json').write_text(json.dumps(blind,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'source_rows':total,'sample_n':60,'known_unique_texts':len(seen),'sampling_base_seed':20261022,'shuffle_seed':2026102201,'language_filter':'ASCII alphabetic fraction >=0.95 followed by reading for language only; not a validated language detector','language_exclusions':reject,'skipped_in_order':skipped,'groups':x.groupby(['app_name','stratum']).size().to_dict().__str__(),'no_feedback_labels_generated':True,'rule_sha256':hashlib.sha256(Path('D:/projects/Study/outputs/human-review-20261020/分类规则v0.2与后续核验计划.md').read_bytes()).hexdigest()}
(out/'sampling_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for r in x.to_dict('records'): print(json.dumps({k:r[k] for k in ['sample_id','review_reviewId','text']},ensure_ascii=False))
