from pathlib import Path
import pandas as pd
r=Path(__file__).parent
d=pd.read_parquet(r.parent/'study_subset_82004.parquet')
d['stratum']=d.review_score.map(lambda z:'low_1_2' if z<=2 else 'mid_3' if z==3 else 'high_4_5')
groups=[]
for (app,s),g in d.groupby(['app_name','stratum']):
    z=g.sample(5,random_state=20261016).copy()
    z['population_n']=len(g)
    z['sampling_weight']=len(g)/5
    groups.append(z)
x=pd.concat(groups).sample(frac=1,random_state=731).reset_index(drop=True)
x.insert(0,'sample_id',[f'R{i:03}' for i in range(1,len(x)+1)])
x.to_json(r/'sample_with_metadata.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
x[['sample_id','app_name','text']].to_json(r/'blind_review.jsonl',orient='records',lines=True,force_ascii=False)
assert len(x)==90 and x.groupby(['app_name','stratum']).size().eq(5).all()
print('90 reviews; 6 apps x 3 rating strata x 5 reviews')
