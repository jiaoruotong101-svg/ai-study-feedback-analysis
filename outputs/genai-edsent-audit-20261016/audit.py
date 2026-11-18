from pathlib import Path
import pandas as pd,json,re
import pyarrow.parquet as pq
r=Path('outputs/genai-edsent-audit-20261016')
cols=pq.read_schema(next(Path('数据/GenAI-EdSent').glob('*.parquet'))).names
keep=['app_name','app_appId','source_file','review_reviewId','review_content','review_score','review_at','review_reviewCreatedVersion','review_replyContent','review_repliedAt','review_thumbsUpCount']
d=pd.concat([pd.read_parquet(f,columns=keep) for f in sorted(Path('数据/GenAI-EdSent').glob('*.parquet'))],ignore_index=True)
s={ 'rows':len(d),'columns':cols,'missing':{c:int((d[c].isna()|d[c].astype(str).str.strip().eq('')).sum()) for c in d},'duplicate_rows_on_audited_fields':int(d.duplicated().sum()),'duplicate_ids':int(d.duplicated(['app_appId','review_reviewId']).sum())}
d['date']=pd.to_datetime(d.review_at,errors='coerce');d['text']=d.review_content.fillna('').str.strip();d['norm']=d.text.str.lower().str.replace(r'\s+',' ',regex=True);d['words']=d.text.str.findall(r'\b[a-zA-Z]+\b').str.len()
s['date_min']=str(d.date.min());s['date_max']=str(d.date.max());s['years']=d.date.dt.year.value_counts().sort_index().to_dict();s['scores']=d.review_score.value_counts().sort_index().to_dict();s['duplicate_text_extra']=int(d.norm.duplicated().sum());s['short_under5words']=int((d.words<5).sum());s['recent_rows']=int((d.date>='2023-01-01').sum());s['top_texts']=d.norm.value_counts().head(20).to_dict()
x=d[(d.date>='2023-01-01')&(d.words>=5)].drop_duplicates(['app_appId','review_reviewId']).drop_duplicates(['app_appId','norm']).copy()
s['candidate_rows']=len(x);s['candidate_scores']=x.review_score.value_counts().sort_index().to_dict()
a=d.groupby('app_name').agg(rows=('text','size'),start=('date','min'),end=('date','max'));a['recent']=d[d.date>='2023-01-01'].groupby('app_name').size();a['candidate']=x.groupby('app_name').size();a['candidate_low_rate']=x.groupby('app_name').review_score.apply(lambda z:(z<=2).mean());a.to_csv(r/'app_summary.csv',encoding='utf-8-sig')
x[['app_name','review_reviewId','text','review_score','date','review_reviewCreatedVersion','review_replyContent','norm']].to_parquet(r/'candidate.parquet',index=False)
sample=pd.concat([g.sample(min(5,len(g)),random_state=42) for _,g in x.groupby('app_name')])[['app_name','text','review_score']]
sample.to_json(r/'sample.jsonl',orient='records',lines=True,force_ascii=False)
(r/'quality.json').write_text(json.dumps(s,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(s,ensure_ascii=False,indent=2,default=str));print(a.to_string())


