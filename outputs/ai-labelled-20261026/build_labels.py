"""Expand the assistant's full-text review notes; this script does not infer labels."""
from pathlib import Path
from collections import Counter
import hashlib, json, re

out = Path(__file__).resolve().parent
root = out.parent
src = root / 'ai-label-candidates-20261024'
rules = root / 'calibration60-20261022/校准复盘与AI标注规则v0.3.md'
read_jsonl = lambda p: [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
queue = read_jsonl(out/'review_queue.jsonl')
assert len(queue) == 2158
categories = dict(A='回答与任务完成', P='收费与权益', R='运行体验', U='界面与广告', H='入门求助')
annotations, batches = {}, []
for n in range(1,19):
    p = out / f'batch{n:02}.txt'
    chunk = queue[(n-1)*120:n*120]
    ids = {r['sample_id'] for r in chunk}
    exceptions = {}
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        sid, codes, note = line.split('|',2)
        assert sid in ids and sid not in exceptions, (p,sid)
        assert codes in ['S','X'] or set(codes) <= set('APR UHO?'.replace(' ','')), codes
        exceptions[sid] = (codes,note)
    for r in chunk:
        sid = r['sample_id']
        assert sid not in annotations
        annotations[sid] = (*exceptions.get(sid,('N','全文阅读后未发现明确的具体问题、限制、改进诉求或产品使用求助；正面评价和普通任务指令不作为问题反馈。')),n)
    batches.append({'batch':n,'reviewed_ids':[r['sample_id'] for r in chunk],'notes_sha256':sha(p)})
for c in json.loads((out/'audit_corrections.json').read_text(encoding='utf-8')):
    before,_,n = annotations[c['sample_id']]
    assert before == c['before']
    annotations[c['sample_id']] = (c['after'],c['reason'],n)
duplicate_audit = json.loads((out/'duplicate_audit.json').read_text(encoding='utf-8'))
all_meta = []
for split in ['train','development']:
    all_meta.extend(dict(r,split=split) for r in read_jsonl(src/f'{split}_metadata.jsonl'))
assert len(all_meta) == 2160
assert {r['sample_id'] for r in all_meta} == set(annotations) | set(duplicate_audit['excluded'])
rows = []
for r in all_meta:
    sid, text = r['sample_id'], r['text']
    base = {k:r[k] for k in ['sample_id','split','review_reviewId','app_name','review_score','stratum','text']}
    base.update(label_source='AI_assisted_not_human_gold', annotator='gpt-6-astra', review_date='2026-10-26', rules_version='v0.3', rules_sha256=sha(rules), text_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest())
    if sid in duplicate_audit['excluded']:
        base.update(review_status='excluded_near_duplicate', duplicate_of=duplicate_audit['excluded'][sid], language_status='not_reviewed', feedback=None, categories=[], category_targets={k:None for k in categories.values()}, category_complete=False, eligible_binary=False, evidence=[], note='按已记录的近重复筛选阈值排除，未强行赋语义标签。')
    else:
        codes,note,batch = annotations[sid]
        feedback = None if codes in ['S','X'] else int(codes!='N')
        cats = [v for k,v in categories.items() if k in codes]
        complete = codes not in ['S','X'] and not any(k in codes for k in '?O')
        targets = {v:(1 if k in codes else 0 if complete else None) for k,v in categories.items()}
        base.update(review_status='full_text_reviewed', review_batch=batch, annotation_codes=codes, language_status='outside_reliable_english_scope' if codes=='X' else 'english_semantics_pending' if codes=='S' else 'english_understood_for_feedback', feedback=feedback, categories=cats, category_targets=targets, category_complete=complete, other_candidate='O' in codes, category_pending='?' in codes, eligible_binary=feedback is not None, evidence=[{'category':c,'quote':text,'scope':'full_review','start':0,'end':len(text)} for c in cats], note=note)
    rows.append(base)

def write_jsonl(name, data):
    p = out/name
    p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')
    assert read_jsonl(p) == data
    return sha(p)

hashes = {'all_annotations.jsonl':write_jsonl('all_annotations.jsonl',rows)}
for split in ['train','development']:
    binary = [{'sample_id':r['sample_id'],'text':r['text'],'feedback':r['feedback']} for r in rows if r['split']==split and r['eligible_binary']]
    masked = [{'sample_id':r['sample_id'],'text':r['text'],'targets':r['category_targets']} for r in rows if r['split']==split and r['eligible_binary'] and any(v is not None for v in r['category_targets'].values())]
    for suffix,data in [('binary',binary),('categories_masked',masked)]:
        name = f'{split}_{suffix}.jsonl'
        hashes[name] = write_jsonl(name,data)
hashes['pending_and_excluded.jsonl'] = write_jsonl('pending_and_excluded.jsonl',[r for r in rows if not r['eligible_binary'] or not r['category_complete']])

# Check data provenance, split separation, abstention and positive-label evidence.
original = {r['sample_id']:r for r in all_meta}
assert len({r['sample_id'] for r in rows}) == 2160
for r in rows:
    assert r['text'] == original[r['sample_id']]['text']
    assert r['review_reviewId'] == original[r['sample_id']]['review_reviewId']
    assert r['split'] == original[r['sample_id']]['split']
    if r['feedback'] is None:
        assert not r['eligible_binary'] and all(v is None for v in r['category_targets'].values())
    if r['feedback'] == 0:
        assert not r['categories'] and all(v==0 for v in r['category_targets'].values())
    if r.get('category_pending') or r.get('other_candidate'):
        assert all(v is None for k,v in r['category_targets'].items() if k not in r['categories'])
    for e in r['evidence']:
        assert r['text'][e['start']:e['end']] == e['quote'] and e['category'] in r['categories']
norm = lambda s:' '.join(re.findall(r'\w+',s.lower()))
assert not {norm(r['text']) for r in rows if r['split']=='train'} & {norm(r['text']) for r in rows if r['split']=='development'}
counts = {}
for split in ['train','development']:
    part = [r for r in rows if r['split']==split]
    counts[split] = {'candidates':len(part),'near_duplicate_excluded':sum(r['review_status']=='excluded_near_duplicate' for r in part),'language_excluded':sum(r['language_status']=='outside_reliable_english_scope' for r in part),'semantics_pending':sum(r['language_status']=='english_semantics_pending' for r in part),'binary_eligible':sum(r['eligible_binary'] for r in part),'feedback_yes':sum(r['feedback']==1 for r in part),'feedback_no':sum(r['feedback']==0 for r in part),'feedback_yes_category_incomplete':sum(r['feedback']==1 and not r['category_complete'] for r in part),'category_positives':{c:sum(r['category_targets'][c]==1 for r in part) for c in categories.values()},'category_observed_negatives':{c:sum(r['category_targets'][c]==0 for r in part) for c in categories.values()},'application_counts':dict(Counter(r['app_name'] for r in part if r['eligible_binary']))}
manifest = {'date':'2026-10-26','status':'AI_labels_prepared_not_independently_validated','counts':counts,'rules_sha256':sha(rules),'source_files_sha256':{p.name:sha(p) for p in src.glob('*metadata.jsonl')},'outputs_sha256':hashes,'batch_review':batches,'second_pass':{'method':'Assistant re-read 253 no-feedback rows containing selected ambiguity/negative cue words; these words only selected QA cases, never generated labels. Same-assistant QA is not independent validation.','correction_n':4},'evidence_scope':'Full original passage is retained for each positive category; no claim of sentence-level localization. Per-record Chinese notes describe the interpretation.','final_human_test':{'target_n':180,'sample_selected':False,'labels_created':False},'limitations':['AI labels and language screening have not been independently human-validated.','Near-duplicate screen is character based and cannot exclude all paraphrases.','Unobserved category targets are null, not zero; masked training is required.','Candidate stratification is not the original population distribution.','No samples were silently replenished after filtering.','Raw data, source candidate files and the human calibration workbook were not modified.']}
(out/'label_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'counts':counts,'readback':'all output JSONL equal in-memory records; original texts and IDs preserved; no split overlap; null masks verified'},ensure_ascii=True))
