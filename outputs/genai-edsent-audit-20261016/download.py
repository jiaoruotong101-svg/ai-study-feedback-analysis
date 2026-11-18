import urllib.request,json,concurrent.futures,pathlib,hashlib
root=pathlib.Path('outputs/genai-edsent-audit-20261016'); raw=pathlib.Path('数据/GenAI-EdSent');raw.mkdir(exist_ok=True)
base='https://huggingface.co'; repo='Erfan-Nourbakhsh/GenAI-EdSent'
meta=json.load(urllib.request.urlopen(base+'/api/datasets/'+repo,timeout=60));rev=meta['sha']
(root/'source_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
files=[x['rfilename'] for x in meta['siblings'] if x['rfilename'].startswith('data/train-') and x['rfilename'].endswith('.parquet')]
def get(f):
 p=raw/pathlib.Path(f).name;u=base+'/datasets/'+repo+'/resolve/'+rev+'/'+f
 if not p.exists():
  data=urllib.request.urlopen(u,timeout=180).read();p.write_bytes(data)
 b=p.read_bytes();return {'file':f,'url':u,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 result=[]
 for item in ex.map(get,files):result.append(item);print(item['file'],item['bytes'],flush=True)
(root/'download_manifest.json').write_text(json.dumps({'revision':rev,'files':result},indent=2),encoding='utf-8')
(root/'dataset_card.md').write_bytes(urllib.request.urlopen(base+'/datasets/'+repo+'/resolve/'+rev+'/README.md',timeout=60).read())
print('DONE',len(result),sum(x['bytes'] for x in result),flush=True)
