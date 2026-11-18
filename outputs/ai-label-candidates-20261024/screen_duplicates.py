from pathlib import Path
import json, re
from difflib import SequenceMatcher
from collections import defaultdict, Counter

root = Path('D:/projects/Study/outputs')
src = root / 'ai-label-candidates-20261024'
out = root / 'ai-labelled-20261026'
out.mkdir(exist_ok=True)
base = root / 'genai-edsent-audit-20261016'
known = []
for p in [base/'review-expanded/reviewed_all270.jsonl', base/'sample.jsonl', base/'baseline_errors.jsonl', root/'calibration60-20261022/sample_metadata.jsonl']:
    known.extend(json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip())
known.extend(json.loads((base/'issue_examples.json').read_text(encoding='utf-8')))
normalize = lambda s: ' '.join(re.findall(r'\w+', s.lower()))
known = list({normalize(x['text']): x for x in known}.values())
rows = [{'sample_id': f'K{i:04}', 'text': x['text'], 'split': 'previous'} for i,x in enumerate(known)]
for split, name in [('train','train'), ('development','development')]:
    rows.extend(dict(json.loads(s), split=split) for s in (src/f'{name}_text_only.jsonl').read_text(encoding='utf-8').splitlines())
texts = [normalize(x['text']) for x in rows]
grams = [{t[k:k+3] for k in range(len(t)-2)} for t in texts]
index = defaultdict(list)
parent = list(range(len(rows)))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
pairs = []
for i, gs in enumerate(grams):
    overlaps = Counter(j for g in gs for j in index[g])
    for j, overlap in overlaps.items():
        if min(len(texts[i]),len(texts[j])) < 20:
            continue
        jaccard = overlap / (len(gs)+len(grams[j])-overlap)
        if jaccard < .70:
            continue
        ratio = SequenceMatcher(None,texts[i],texts[j],autojunk=False).ratio()
        if ratio >= .92:
            parent[find(j)] = find(i)
            pairs.append({'left':rows[j]['sample_id'],'right':rows[i]['sample_id'],'trigram_jaccard':round(jaccard,5),'sequence_ratio':round(ratio,5)})
    for g in gs:
        index[g].append(i)
groups = {}
for i in range(len(rows)):
    groups.setdefault(find(i),[]).append(i)
excluded = {}
for members in groups.values():
    keeper = min(members)
    for i in members:
        if i != keeper and rows[i]['split'] != 'previous':
            excluded[rows[i]['sample_id']] = rows[keeper]['sample_id']
review = [x for x in rows if x['split'] != 'previous' and x['sample_id'] not in excluded]
(out/'review_queue.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in review),encoding='utf-8')
(out/'duplicate_audit.json').write_text(json.dumps({'method':'normalized character trigram Jaccard >= .70 AND SequenceMatcher >= .92; both texts >=20 chars; transitive components; previous > train > development priority; mechanical near-duplicate screen, not semantic proof','excluded':excluded,'pairs':pairs,'known_unique_n':len(known),'remaining':{s:sum(x['split']==s for x in review) for s in ['train','development']}},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'excluded_n':len(excluded),'remaining_n':len(review),'remaining':{s:sum(x['split']==s for x in review) for s in ['train','development']}},ensure_ascii=False))
