from pathlib import Path
import json,math,re,hashlib
import pandas as pd

r=Path(__file__).parent
meta=pd.read_json(r/'sample_metadata.jsonl',lines=True)
old=pd.read_json(r.parent/'review-pilot/reviewed_90.jsonl',lines=True)
groups={'回答与任务完成':['ANSWER','EXPLAIN','UNDERSTAND'],'收费与权益':['PAY','BILLING','ENTITLEMENT'],'运行体验':['TECH','SPEED'],'界面与广告':['ADS','UI'],'入门求助':['ONBOARD'],'未覆盖候选':['NEW_PERMISSIONS','NEW_SUPPORT']}
subnames={'ANSWER':'回答质量','EXPLAIN':'解释与步骤','UNDERSTAND':'理解与任务完成','PAY':'付费门槛与额度','BILLING':'扣费争议与退款','ENTITLEMENT':'已购权益','TECH':'运行与访问','SPEED':'响应速度','ADS':'广告体验','UI':'界面易用性','ONBOARD':'入门求助','NEW_PERMISSIONS':'权限异议候选','NEW_SUPPORT':'客服缺失候选'}
rows=[]
for batch in ['A','B']:
    lines=(r/f'annotations_{batch}.tsv').read_text(encoding='utf8').strip().splitlines()
    assert len(lines)==90
    for line in lines:
        ident,codes,status,evidence,note,flags=line.split('|')
        z=meta.loc[meta.sample_id.eq(ident)].iloc[0].to_dict()
        assert z['batch']==batch
        assert evidence.lower() in z['text'].lower(),(ident,evidence)
        assert all(c in subnames for c in codes.split(',') if c)
        rows.append({**z,'issue_codes':codes,'content_status':status,'evidence_excerpt':evidence,'review_note':note,'flags':flags,'has_actionable_feedback':bool(codes),'annotation_source':'AI辅助探索核验，未经独立人工复核'})
new=pd.DataFrame(rows)
new['issue_labels']=new.issue_codes.map(lambda s:'；'.join(subnames[c] for c in s.split(',') if c))
old['batch']='P';old['flags']=''
old.loc[old.sample_id.eq('R052'),'flags']='mild'
old.loc[old.sample_id.isin(['R030','R032','R040','R051','R075']),'flags']='pilot_boundary'
old['annotation_source']='AI辅助探索核验，未经独立人工复核'
combined=pd.concat([old,new],ignore_index=True)
assert len(new)==180 and len(combined)==270
assert combined.review_reviewId.nunique()==270
for frame in [new,combined]:
    frame['category_groups']=frame.issue_codes.map(lambda s:'；'.join(g for g,c in groups.items() if set(s.split(','))&set(c)))
new.to_json(r/'reviewed_new180.jsonl',lines=True,orient='records',force_ascii=False,date_format='iso')
combined.to_json(r/'reviewed_all270.jsonl',lines=True,orient='records',force_ascii=False,date_format='iso')
combined.to_csv(r/'累计270条核验明细.csv',index=False,encoding='utf-8-sig')

batch=[]
for b,d in combined.groupby('batch'):
    row={'batch':b,'n':len(d),'actionable':int(d.has_actionable_feedback.sum()),'uncovered':int(d.issue_codes.str.contains('NEW_').sum()),'ambiguous_or_vague':int(d.content_status.isin(['ambiguous','vague_negative']).sum())}
    for g,c in groups.items():row[g]=int(d.issue_codes.map(lambda s:bool(set(s.split(','))&set(c))).sum())
    batch.append(row)
strata=combined.groupby(['batch','stratum']).has_actionable_feedback.agg(['sum','count']).reset_index()
strata.to_csv(r/'分批评分层统计.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(batch).to_csv(r/'分批分类统计.csv',index=False,encoding='utf-8-sig')
sub=[]
for code,name in subnames.items():
    row={'code':code,'name':name}
    for b in ['P','A','B']:row[b]=int(combined.loc[combined.batch.eq(b),'issue_codes'].map(lambda s:code in s.split(',')).sum())
    sub.append(row)
pd.DataFrame(sub).to_csv(r/'子类稳定性.csv',index=False,encoding='utf-8-sig')

# Diagnostic comparison against pre-existing literal keyword mention rules.
# These patterns were not originally problem classifiers. No tuning on these labels.
patterns={
 'answer_quality':r'\b(?:wrong|incorrect|accurate|accuracy|correct|explain|explanation|explanations)\b',
 'payment_limits':r'\b(?:pay|paid|payment|money|subscription|subscribe|premium|coins|tokens|paywall)\b',
 'advertising':r'\b(?:ads|advertisements|advertisement|adverts)\b',
 'technical_access':r'\b(?:crash|crashes|crashing|bug|bugs|login|loading|freeze|freezes|error|errors)\b',
 'image_input':r'\b(?:photo|photos|picture|pictures|camera|scan|scanning|image|images)\b',
 'memory_context':r'\b(?:remember|remembers|forget|forgets|forgot|memory|context)\b'}
pred=new.text.map(lambda t:any(re.search(p,t,re.I) for p in patterns.values()))
y=new.has_actionable_feedback
tp=int((pred&y).sum());fp=int((pred&~y).sum());fn=int((~pred&y).sum());tn=int((~pred&~y).sum())
errors=new.loc[pred!=y,['sample_id','batch','review_score','text','issue_codes','evidence_excerpt','review_note']].copy()
errors['keyword_hit']=pred[pred!=y].to_numpy()
errors.to_csv(r/'旧关键词与核验不一致案例.csv',index=False,encoding='utf-8-sig')

summary={'new_n':180,'cumulative_n':270,'batch_results':batch,'rating_strata':strata.to_dict('records'),'new_status':new.content_status.value_counts().to_dict(),'all_status':combined.content_status.value_counts().to_dict(),'new_uncovered_ids':new.loc[new.issue_codes.str.contains('NEW_'),'sample_id'].tolist(),'flag_counts_new':{flag:int(new['flags'].str.split(',').map(lambda x:flag in x).sum()) for flag in ['uncertain','mild','language','language_capability','novel']},'subcategories':sub,'high_rating_ids_new':new.loc[new.review_score.ge(4)&y,'sample_id'].tolist(),'keyword_proxy_diagnostic':{'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':tp/(tp+fp),'recall':tp/(tp+fn),'false_positive_ids':new.loc[pred&~y,'sample_id'].tolist(),'false_negative_ids':new.loc[~pred&y,'sample_id'].tolist(),'note':'旧主题词提及规则若误用为具体问题筛选会出现的分歧；AI标签探索性参照，不是独立金标准性能。'}}
for b,d in [('new',new),('all',combined)]:
    summary[b+'_rating_totals']=d.groupby('stratum').has_actionable_feedback.agg(['sum','count']).to_dict('index')
    summary[b+'_high_without_mild']=int((d.review_score.ge(4)&d.has_actionable_feedback&~d['flags'].str.contains('mild')).sum())
    summary[b+'_multilabel_n']=int(d.issue_codes.str.contains(',').sum())
    summary[b+'_no_issue_but_low_ids']=d.loc[d.review_score.le(2)&~d.has_actionable_feedback,'sample_id'].tolist()
summary['new_sensitive_exclusion']={}
for name,mask in [('exclude_uncertain',~new['flags'].str.contains('uncertain')),('exclude_language',~new['flags'].str.contains(r'(?:^|,)language(?:,|$)',regex=True)),('exclude_both',~new['flags'].str.contains(r'uncertain|(?:^|,)language(?:,|$)',regex=True))]:
    z=new[mask]
    summary['new_sensitive_exclusion'][name]={'n':len(z),'actionable':int(z.has_actionable_feedback.sum()),'by_rating':z.groupby('stratum').has_actionable_feedback.agg(['sum','count']).to_dict('index')}
(r/'expanded_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('HIGH RATING EVIDENCE')
print(new.loc[new.review_score.ge(4)&y,['sample_id','review_score','app_name','issue_codes','text']].to_string(index=False))
