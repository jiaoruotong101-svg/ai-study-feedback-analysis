from pathlib import Path
import hashlib, json, re
import pandas as pd

root=Path('D:/projects/Study')
base=root/'outputs/genai-edsent-audit-20261016'
cal=root/'outputs/calibration60-20261022'
out=root/'outputs/ai-label-candidates-20261024'
out.mkdir(exist_ok=True)
norm=lambda s:' '.join(str(s).lower().split())
plain=lambda s:' '.join(re.findall(r'\w+',norm(s)))
seen=[]
for p in [base/'review-expanded/reviewed_all270.jsonl',base/'sample.jsonl',base/'baseline_errors.jsonl',cal/'sample_metadata.jsonl']:
    seen.extend(json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip())
seen.extend(json.loads((base/'issue_examples.json').read_text(encoding='utf-8')))
known_text={norm(x['text']) for x in seen}
known_plain={plain(x['text']) for x in seen}
known_ids={str(x['review_reviewId']) for x in seen if x.get('review_reviewId')}
d=pd.read_parquet(base/'study_subset_82004.parquet')
d['norm']=d.text.map(norm)
d['plain']=d.text.map(plain)
d=d[~d.norm.isin(known_text)&~d.plain.isin(known_plain)&~d.review_reviewId.astype(str).isin(known_ids)].copy()
d=d.drop_duplicates('plain').drop_duplicates('review_reviewId')
def ascii_fraction(s):
    letters=[c for c in str(s) if c.isalpha()]
    return sum(c.isascii() for c in letters)/len(letters) if letters else 0
d=d[d.text.map(ascii_fraction).ge(.95)].copy()
d['stratum']=d.review_score.map(lambda s:'low' if s<=2 else 'mid' if s==3 else 'high')
# Six apps x (high 190/30, low 80/20, mid 30/10) for train/development.
# This leaves room in the smallest mid-rating groups for the later human test.
quota={'high':(190,30),'low':(80,20),'mid':(30,10)}
train=[];dev=[];groups=[]
for ai,app in enumerate(sorted(d.app_name.unique())):
    for si,stratum in enumerate(('high','low','mid')):
        t,v=quota[stratum]
        group=d[(d.app_name==app)&(d.stratum==stratum)].sort_values('review_reviewId')
        assert len(group)>=t+v+10,(app,stratum,len(group))
        part=group.sample(n=t+v,random_state=2026102400+ai*3+si)
        train.extend(part.iloc[:t].to_dict('records'))
        dev.extend(part.iloc[t:].to_dict('records'))
        groups.append({'app':app,'rating_stratum':stratum,'eligible_after_exclusion':len(group),'train':t,'development':v,'left_before_final_test':len(group)-t-v})
train=pd.DataFrame(train).sample(frac=1,random_state=2026102411).reset_index(drop=True)
dev=pd.DataFrame(dev).sample(frac=1,random_state=2026102412).reset_index(drop=True)
train.insert(0,'sample_id',[f'T{i:04}' for i in range(1,len(train)+1)])
dev.insert(0,'sample_id',[f'V{i:04}' for i in range(1,len(dev)+1)])
assert (len(train),len(dev))==(1800,360)
assert not set(train.plain)&set(dev.plain)
assert train.review_reviewId.nunique()==1800 and dev.review_reviewId.nunique()==360
assert not (set(train.plain)|set(dev.plain))&known_plain
for name,frame in [('train',train),('development',dev)]:
    frame.to_json(out/f'{name}_metadata.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
    frame[['sample_id','text']].to_json(out/f'{name}_text_only.jsonl',orient='records',lines=True,force_ascii=False)
rules=cal/'校准复盘与AI标注规则v0.3.md'
manifest={'status':'candidate_split_only_no_ai_labels','source_rows':82004,'train_n':1800,'development_n':360,'held_out_final_test_n':180,'known_previous_unique_text_n':len(known_text),'normalization':'lowercase whitespace and punctuation-stripped exact-text check','ascii_fraction_prefilter':0.95,'warning':'ASCII fraction is not reliable language identification; candidates still need semantic language screening before label use. Near-duplicate review beyond exact punctuation normalization remains pending.','group_quotas':groups,'group_seed_base':2026102400,'train_shuffle_seed':2026102411,'dev_shuffle_seed':2026102412,'rules_sha256':hashlib.sha256(rules.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((base/'study_subset_82004.parquet').read_bytes()).hexdigest()}
(out/'split_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'train':len(train),'development':len(dev),'groups':groups},ensure_ascii=False))
