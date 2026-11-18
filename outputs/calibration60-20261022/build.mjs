import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const data=JSON.parse(await fs.readFile(`${dir}/blind_sample.json`,'utf8'));
const wb=Workbook.create();
const s=wb.worksheets.add('独立填写');
const g=wb.worksheets.add('填写说明');
function style(sheet,range){sheet.showGridLines=false;sheet.getRange(range).format={font:{name:'Arial',size:11,color:'#243247'},wrapText:true,verticalAlignment:'top'};}
style(s,'A1:G65');
s.getRange('A2').values=[['独立人工校准 · 60条']];
s.getRange('A2').format.font={name:'Arial',size:16,bold:true};
s.getRange('A3').values=[['先看“填写说明”，只填黄色 C—G 列。没有标准答案提示；不确定可以保留。']];
s.getRange('A2:G3').format.wrapText=false;
s.getRange('A5:G5').values=[['编号','评论原文（完整）','能否理解原文','是否有具体反馈','类别（可多选，手填）','原文证据','理由／待定原因']];
s.getRange('A6:G65').values=data.map(r=>[r.sample_id,r.text,null,null,null,null,null]);
s.tables.add('A5:G65',true,'Calibration60');
s.getRange('A5:G5').format={fill:'#334760',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeight:38};
for(const [i,width] of [10,72,18,18,32,42,50].entries())s.getRangeByIndexes(0,i,65,1).format.columnWidth=width;
s.getRange('C6:G65').format.fill='#FFF4CC';
s.getRange('C6:C65').dataValidation={rule:{type:'list',values:['能理解','部分能理解','无法判断']}};
s.getRange('D6:D65').dataValidation={rule:{type:'list',values:['有','无','不确定']}};
data.forEach((r,i)=>s.getRange(`A${i+6}:G${i+6}`).format.rowHeight=Math.max(90,Math.ceil(r.text.length/67)*17+18));
s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);
const instructions=[
['本次任务','独立阅读60条新评论，判断是否有具体体验反馈及其类别。本批用于校准规则，不是最终测试集。先独立完成，再与AI结果对照。'],
['怎么开始','在“独立填写”按编号阅读原文，只填写黄色C—G列。可每次做10条并保存，不用一次完成。不要改编号或评论原文。'],
['C 能否理解原文','能理解／部分能理解／无法判断。以自己能否可靠理解原文为准。缩写、错拼或术语拿不准，写在G列；不要猜出缺失含义。'],
['D 是否有具体反馈','有：能定位的体验问题、限制、改进请求或使用求助。无：只有一般性评价，或明确不涉及使用体验的内容。不确定：不足以可靠判定。'],
['E 类别怎么填','D=有时，可填下方一个或多个主类，用中文分号分隔。类别不明填“待定”；有明确未覆盖内容填“其他候选：具体内容”。D=无填“无”；D=不确定填“待定”。'],
['F 原文证据','复制支持你判断的原文片段。多类别分别给证据。判断无反馈也可摘录对应评价；无法判读时填“无法判读”。只抄原文，不用翻译。'],
['G 理由与待定原因','用一两句话说明理由，或哪些内容无法确认。没有具体反馈时，可说明是正面、一般评价、泛泛差评、普通任务指令等。允许写“理由未补充”。'],
['回答与任务完成','对回答质量、解释步骤、理解需求、完成任务方面有明确反馈。只记录原文支持的层级，质量不满不自动等于答案错误。'],
['收费与权益','明确涉及付费价值、订阅门槛、提问次数限制、扣费退款或已购权益。不要从未知资源词直接猜测付费机制。'],
['运行体验','明确登录／访问失败、报错、运行中断、响应慢等。只有“不回答”且缺少进一步依据时，可有反馈但类别待定。'],
['界面与广告','明确的布局、入口选择、显示、操作或广告干扰问题。同一问题造成无法操作，不自动另加运行故障标签。'],
['入门求助','不知道如何使用、激活等产品使用困难。普通解题指令不自动算入门求助。'],
['多标签与其他候选','多项不同反馈都有证据时可填多类；不要把同一现象的后果重复计类。现有主类覆盖不了的内容保留其他候选，不硬套。'],
['不确定怎么填','看得懂现象但无法确定类别：D填“有”、E填“待定”。连是否有反馈都不清楚：D填“不确定”、E填“待定”。不用为了填满类别而猜测。'],
['语言与翻译','样本经过英语预筛，但不能保证每条你都能理解。若需要未核实翻译才能判断，请标无法判断并注明待语言复核。不要先向AI索要本条的分类答案。'],
['只按评论表达判断','评论所述问题不是已验证的真实故障。不要推断技术原因、收费周期或产品效果。若原文明确说明网站端等平台，在G列注明；没说明不猜。'],
['正面与轻度异议','正面评价也可包含具体反馈；轻度异议和求助可以纳入。只出现转折词不自动表示不满，是否有反馈需看内容。'],
['独立填写要求','本文件没有AI标签、逐条提问、参考答案或预填证据，也不附中文翻译。评分和应用字段不展示；原文自带星级等描述原样保留。'],
['完成之后','保存文件并告诉我完成了哪些编号。我再读取你的答案、与独立生成的AI结果比较并汇总分歧。这60条之后不充当最终测试样本。'],
['抽样范围','六款学习助手各10条；1—2星、3星、4—5星各20条，随机打乱。已排除旧270条及已知展示样本，并做文本重复检查。本样本不能代表总体问题比例。'],
['来源与规则','GenAI-EdSent本地六应用候选集（评论截至2025年8月）。按项目分类规则v0.2整理，准备日期2026-10-22。仅保留原文供独立填写。']
];
style(g,'A1:B25');
g.getRange('A2').values=[['填写说明']];g.getRange('A2').format.font={size:16,bold:true};
g.getRange(`A4:B${instructions.length+3}`).values=instructions;
g.getRange('A1:A25').format.columnWidth=24;g.getRange('B1:B25').format.columnWidth=108;
g.getRange('A4:A24').format.fill='#EDF1F6';g.getRange('A4:A24').format.font.bold=true;
instructions.forEach((r,i)=>g.getRange(`A${i+4}:B${i+4}`).format.rowHeight=Math.max(48,Math.ceil(r[1].length/50)*18+18));
wb.recalculate();
assert.deepEqual(s.getRange('A6:B65').values,data.map(r=>[r.sample_id,r.text]));
assert.ok(s.getRange('C6:G65').values.flat().every(v=>v==null||v===''));
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!',options:{useRegex:true,maxResults:5},maxChars:300})).ndjson);
for(const [sheetName,range,name] of [['独立填写','A5:E10','sample'],['独立填写','C5:G8','inputs'],['填写说明','A2:B14','guide1'],['填写说明','A15:B24','guide2']]){
 const blob=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(`${dir}/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/独立人工校准60条.xlsx`);
console.log('Exported 60 originals and 300 blank human cells; no AI labels.');
