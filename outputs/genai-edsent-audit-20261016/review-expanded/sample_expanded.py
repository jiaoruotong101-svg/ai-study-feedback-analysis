from pathlib import Path
import pandas as pd,json,hashlib
r=Path(__file__).parent;r.mkdir(exist_ok=True)
base=r.parent
normalize=lambda t:' '.join(str(t).lower().split())
d=pd.read_parquet(base/'study_subset_82004.parquet')
old=pd.read_json(base/'review-pilot/reviewed_90.jsonl',lines=True)
seen=set(old.text.map(normalize))
for name in ['sample.jsonl','baseline_errors.jsonl']:
    seen.update(pd.read_json(base/name,lines=True).text.map(normalize))
seen.update(normalize(x['text']) for x in json.loads((base/'issue_examples.json').read_text(encoding='utf8')))
d['norm']=d.text.map(normalize)
d=d[~d.norm.isin(seen)].copy()
d['stratum']=d.review_score.map(lambda s:'low_1_2' if s<=2 else 'mid_3' if s==3 else 'high_4_5')
groups=[]
for _,g in d.groupby(['app_name','stratum']):
    s=g.sample(10,random_state=2026101602).copy()
    s['batch']=['A']*5+['B']*5
    s['population_n_after_exclusion']=len(g)
    groups.append(s)
x=pd.concat(groups).sample(frac=1,random_state=1702)
x=pd.concat([x[x.batch.eq(b)] for b in ['A','B']]).reset_index(drop=True)
x.insert(0,'sample_id',[f'E{i:03}' for i in range(1,181)])
assert x.groupby(['app_name','stratum','batch']).size().eq(5).all()
assert x.review_reviewId.nunique()==180 and x.norm.nunique()==180
assert not set(x.norm)&seen
x.to_json(r/'sample_metadata.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
for batch in ['A','B']:
    x[x.batch.eq(batch)][['sample_id','app_name','text']].to_json(r/f'blind_{batch}.jsonl',orient='records',lines=True,force_ascii=False)
rule=(base/'review-pilot/问题分类规则.md').read_bytes()
(r/'frozen_codebook_v01.md').write_bytes(rule)
(r/'sampling_manifest.json').write_text(json.dumps({'new_n':180,'pilot_n':90,'total_n':270,'excluded_known_normalized_texts':len(seen),'remaining_population':len(d),'seed':2026101602,'shuffle_seed':1702,'frozen_rule_sha256':hashlib.sha256(rule).hexdigest(),'definition':'6 apps x 3 rating strata x 10; two sequential batches of 90; no overlap with previously displayed normalized text'},ensure_ascii=False,indent=2),encoding='utf8')
print('180 new unique reviews sampled; A/B 90 each; codebook frozen')
