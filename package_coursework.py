from pathlib import Path
import os,json,hashlib,zipfile

root=Path(__file__).resolve().parent
dest=root/'交付包';dest.mkdir(exist_ok=True)
archive=dest/'AI学习助手课设_必要文件_20261106.zip'
folders=['ai-label-candidates-20261024','ai-labelled-20261026','calibration60-20261022','feedback-baseline-20261026','genai-edsent-audit-20261016','human-evaluation-20261030','human-review-20261020','human-test180-20261026']
excluded_dirs={'node_modules','__pycache__','qa','SVG','figures','figures_eda','word_report'}
excluded_ext={'.png','.jpg','.jpeg','.svg','.webp','.gif','.pdf','.zip','.bak','.pyc','.log'}
excluded_names={'build_report.py','generate_eda_figures.cjs','generate_publication_figures.cjs','combine_fig2_fig3.cjs','全部图表索引.md'}
files=[root/'PROJECT_HANDOFF.md',root/'数据'/'README.md',root/'数据'/'dataset_card.md',Path(__file__)]
files+=list((root/'数据'/'GenAI-EdSent').glob('*'))
files+=list((root/'运行指南').glob('*'))
for folder in folders:
    for base,dirs,names in os.walk(root/'outputs'/folder,followlinks=False):
        dirs[:]=[d for d in dirs if d not in excluded_dirs and not (Path(base)/d).is_symlink() and not os.path.isjunction(Path(base)/d)]
        for name in names:
            path=Path(base)/name
            if path.suffix.lower() in excluded_ext or name in excluded_names or '.inspect.' in name:continue
            if path.suffix=='.xlsx' and (name.startswith(('before_','candidate_','filled_','first6_','next20_')) or name in {'remaining_candidate.xlsx'}):continue
            files.append(path)
report=root/'outputs/human-evaluation-20261030/word_report/AI学习助手体验问题识别课程报告.docx'
files.append(report)
initial=root/'outputs/AI学习助手用户反馈分析课设选题建议.docx'
if initial.exists():files.append(initial)
files=sorted(set(p for p in files if p.is_file()))
required=['outputs/feedback-baseline-20261026/model.joblib','outputs/human-test180-20261026/human_decisions_20261030.json','outputs/human-test180-20261026/evaluate_frozen.py','outputs/ai-labelled-20261026/train_baseline.py','outputs/ai-labelled-20261026/all_annotations.jsonl','outputs/human-evaluation-20261030/metrics.json']
rel={p.relative_to(root).as_posix():p for p in files}
assert all(n in rel for n in required)
readme='''# 课设必要文件包

打包日期：2026-11-06。保持原项目目录结构；解压后在本目录运行脚本。

## 包含内容
原始16个Parquet分片及数据卡、下载版本与校验记录；数据审计和研究子集；探索标注、40条复核、60条校准及180条人工判定；训练开发候选与最终AI标签；训练脚本、冻结模型、配置、开发结果；人工评测脚本、完整预测、指标与逐条对照；报告初稿与最终Word。

最终Word保留其内嵌配图。未打包独立生图/改图输出、SVG/PNG图表、图片压缩包、预览PDF、图表生成修改脚本、旧备份、node_modules、Python运行环境、旧迁移包及求职项目。原始数据Excel是Parquet的重复展示版，未放入；人工标注Excel保留。

## 最短复现路径
原实验Python 3.13.14、scikit-learn 1.9.1。Python分析依赖包括numpy、pandas、pyarrow、scikit-learn、joblib。请使用与冻结模型匹配的scikit-learn版本；其他依赖未在此伪造精确版本。

在解压根目录执行：
```
python outputs/human-test180-20261026/evaluate_frozen.py
```
该脚本读取相邻目录的冻结模型和已保存人工判断，不训练。结果写入outputs/human-evaluation-20261030。先另存已有结果，可对比重跑前后的metrics.json。应复现178条确定记录的87.64%准确率、88.66%正类F1，以及四类71.35%微平均F1。

若需要重新训练，请在副本内运行：
```
python outputs/ai-labelled-20261026/train_baseline.py
```
该命令会覆盖副本中的模型、开发结果和冻结清单。不要用它替代原冻结模型的评测复现。AI语义标签不是由训练脚本自动生成的，保存的批次记录及all_annotations.jsonl是实验输入。

## 其他脚本与环境说明
部分早期抽样或表格脚本含D:/projects/Study等本机路径；换电脑运行前应调整。Excel生成与回填脚本使用@oai/artifact-tool及原Codex环境，不是只安装Python即可运行。最终Excel及其JSON决策记录均已保留，无须重新执行填写脚本。原脚本按原样归档，没有为打包修改研究代码或伪造完整依赖锁。

## 结果口径
实际训练1,721条，开发347条。180条人工判定有92条具体反馈、86条无具体反馈、2条不确定。AI提供翻译和候选选项，用户最终判断且未见冻结模型预测；不能称为完全无提示的独立标注。旧91.61%为评分预测，不是本轮问题分类。数据许可信息见数据卡，数据与代码许可不能混同。

根目录文件清单.json逐项记录路径、字节数与SHA-256。ZIP创建后已做CRC完整性与内容哈希核对。学校课程大纲及格式模板另存于课程要求目录。
'''
manifest=[{'path':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in rel.items()]
templates=Path('D:/projects/大数据课程设计专业大纲及模板')
extra={f'课程要求/{p.name}':p for p in templates.glob('*.doc') if '数据分析类' in p.name or '格式模板' in p.name}
for n,p in extra.items():manifest.append({'path':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,p in {**rel,**extra}.items():z.write(p,n)
    z.writestr('先读我.md',readme)
    z.writestr('文件清单.json',json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in manifest:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
    assert not any(Path(n).suffix.lower() in excluded_ext for n in z.namelist())
print(json.dumps({'zip':str(archive),'files':len(manifest)+2,'size_mb':round(archive.stat().st_size/1024**2,2),'verified':'CRC and all SHA-256'},ensure_ascii=True))
