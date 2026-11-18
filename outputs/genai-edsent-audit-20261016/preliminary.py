from pathlib import Path
import pandas as pd, json, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
root=Path(__file__).parent
d=pd.read_parquet(root/'candidate.parquet')
apps=['Gauth: AI Study Companion','Question.AI - Chatbot&Math AI','Answer.AI - Your AI tutor','Nerd AI - Tutor & Math Helper','StudyX: AI Homework Helper','Homework AI - Math & Essay App']
x=d[d.app_name.isin(apps)].copy()
x['low']=x.review_score.le(2).astype(int)
patterns={
 'answer_quality':r'\b(?:wrong|incorrect|accurate|accuracy|correct|explain|explanation|explanations)\b',
 'payment_limits':r'\b(?:pay|paid|payment|money|subscription|subscribe|premium|coins|tokens|paywall)\b',
 'advertising':r'\b(?:ads|advertisements|advertisement|adverts)\b',
 'technical_access':r'\b(?:crash|crashes|crashing|bug|bugs|login|loading|freeze|freezes|error|errors)\b',
 'image_input':r'\b(?:photo|photos|picture|pictures|camera|scan|scanning|image|images)\b',
 'memory_context':r'\b(?:remember|remembers|forget|forgets|forgot|memory|context)\b',
}
stats=[]
for name,pat in patterns.items():
 x[name]=x.text.str.contains(pat,case=False,regex=True)
 z=x[x[name]]
 stats.append({'signal':name,'n':len(z),'share':len(z)/len(x),'low_rating_rate':z.low.mean(),'low_rating_rate_without':x.loc[~x[name],'low'].mean(),'high_rating_mentions':int(z.review_score.ge(4).sum())})
pd.DataFrame(stats).to_csv(root/'keyword_signals.csv',index=False,encoding='utf-8-sig')
x.groupby(['app_name',x.date.dt.to_period('M').astype(str)]).agg(n=('text','size'),low_rate=('low','mean')).to_csv(root/'monthly.csv',encoding='utf-8-sig')
for app,g in x.groupby('app_name'):
 print(app,len(g),round(g.low.mean(),4),flush=True)
# Deterministic chronological split. Remove identical normalized text across both periods.
m=x.sort_values('date').drop_duplicates('norm').copy()
train=m[m.date<'2025-01-01'];test=m[m.date>='2025-01-01']
train=train.sample(min(50000,len(train)),random_state=42)
v=TfidfVectorizer(ngram_range=(1,2),min_df=3,max_features=40000,sublinear_tf=True)
A=v.fit_transform(train.text);B=v.transform(test.text)
model=LogisticRegression(max_iter=500,class_weight='balanced',random_state=42)
model.fit(A,train.low)
pred=model.predict(B);prob=model.predict_proba(B)[:,1]
def metrics(y,p,score):
 return {'accuracy':accuracy_score(y,p),'macro_f1':f1_score(y,p,average='macro'),'low_precision':precision_score(y,p,zero_division=0),'low_recall':recall_score(y,p,zero_division=0),'low_f1':f1_score(y,p,zero_division=0),'roc_auc':roc_auc_score(y,score)}
prior=test.app_name.map(train.groupby('app_name').low.mean()).fillna(train.low.mean())
results={'task':'predict 1-2 stars vs 3-5 stars, NOT issue classification or sentiment gold labels','selected_apps':apps,'selected_rows':len(x),'selected_low_rate':x.low.mean(),'train_n':len(train),'test_n':len(test),'train_end':str(train.date.max()),'test_start':str(test.date.min()),'test_end':str(test.date.max()),'majority':metrics(test.low,[0]*len(test),[train.low.mean()]*len(test)),'app_prior':metrics(test.low,prior.ge(.5).astype(int),prior),'tfidf_logistic':metrics(test.low,pred,prob),'keywords_are_unvalidated_mentions':True,'sensitivity_min10words':int(x.text.str.findall(r'\b[a-zA-Z]+\b').str.len().ge(10).sum())}
per=[]
for app in apps:
 mask=test.app_name.eq(app).to_numpy()
 if mask.sum():per.append({'app':app,'n':int(mask.sum()),**metrics(test.low[mask],pred[mask],prob[mask])})
results['per_app_test']=per
(root/'baseline.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
samples=[]
for name in patterns:
 z=x[x[name]&x.low.eq(1)]
 for _,row in z.sample(min(5,len(z)),random_state=42).iterrows():
  samples.append({'signal':name,'app':row.app_name,'score':row.review_score,'text':row.text})
(root/'issue_examples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2),encoding='utf-8')
test[['app_name','review_reviewId','review_score','date']].assign(predicted_low=pred,probability_low=prob).to_parquet(root/'test_predictions.parquet',index=False)
print(json.dumps(results,ensure_ascii=False,indent=2),flush=True)
