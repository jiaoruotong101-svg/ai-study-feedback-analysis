import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {Workbook, SpreadsheetFile, FileBlob} from '@oai/artifact-tool';

const dir='D:/projects/Study/outputs/human-test180-20261026';
const data=JSON.parse(await fs.readFile(`${dir}/blind_sample.json`,'utf8'));
assert.equal(data.length,180);
assert.ok(data.every(r=>Object.keys(r).sort().join(',')==='sample_id,text'));
assert.ok(data.every(r=>!r.text.startsWith('=')));
const wb=Workbook.create();
const s=wb.worksheets.add('独立填写');
const g=wb.worksheets.add('填写说明');
const style=(sheet,range)=>{
  sheet.showGridLines=false;
  sheet.getRange(range).format={font:{name:'Arial',size:11,color:'#243247'},wrapText:true,verticalAlignment:'top'};
};
style(s,'A1:G185');
s.getRange('A2').values=[['独立人工测试 180条']];
s.getRange('A2').format.font={name:'Arial',size:16,bold:true};
s.getRange('A3').values=[['先读填写说明。只填黄色 C—G 列，可以每次完成10条。无法判断时保留不确定。']];
s.getRange('A2:G3').format.wrapText=false;
s.getRange('A2:G2').format.rowHeight=28;
s.getRange('A3:G3').format.rowHeight=24;
s.getRange('A5:G5').values=[['编号','评论原文（完整）','能否理解原文','是否有具体反馈','类别（可多选，手填）','原文证据','理由／待定原因']];
s.getRange('A6:G185').values=data.map(r=>[r.sample_id,r.text,null,null,null,null,null]);
s.tables.add('A5:G185',true,'HumanTest180');
s.getRange('A5:G5').format={fill:'#334760',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',horizontalAlignment:'center',rowHeight:40};
for(const [i,width] of [10,70,18,18,30,40,46].entries())s.getRangeByIndexes(0,i,185,1).format.columnWidth=width;
s.getRange('C6:G185').format.fill='#FFF4CC';
s.getRange('C6:C185').dataValidation={rule:{type:'list',values:['能理解','部分能理解','无法判断']}};
s.getRange('D6:D185').dataValidation={rule:{type:'list',values:['有','无','不确定']}};
data.forEach((r,i)=>{
  const lines=r.text.split('\n').reduce((n,line)=>n+Math.max(1,Math.ceil(line.length/58)),0);
  s.getRange(`A${i+6}:G${i+6}`).format.rowHeight=Math.max(84,lines*17+20);
});
s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);
const instructions=[
 ['本次任务','独立判断180条新评论，用于评价已经固定的模型。先填写自己的判断，再统一对照模型结果。可以每次完成10条，不需要一次做完。'],
 ['填写位置','在“独立填写”填黄色C—G列。保留编号和原文。表内没有AI标签、逐条翻译或推荐答案。C、D的下拉菜单仅是统一的填写值。'],
 ['C 能否理解原文','能理解／部分能理解／无法判断。以你能否独立理解与判断有关的原文为准。关键缩写、错拼、术语不确定时，在G列说明，不猜测。'],
 ['D 是否有具体反馈','有：能定位的体验问题、限制、改进请求或产品使用求助。无：只有赞扬、一般评价、泛泛差评或普通任务指令。不确定：无法可靠区分。'],
 ['E 类别怎么填','有反馈时填写下列主类，可用中文分号分隔多个类别。不能确定类别填“待定”；未被五类覆盖的明确反馈填“其他候选：具体内容”。无反馈填“无”；反馈不确定填“待定”。'],
 ['F 原文证据','复制支持判断的原文短句。多类别分别摘录对应证据。无反馈也可摘录一般评价或任务指令。无法理解时填“无法判读”。'],
 ['G 理由／待定原因','用一两句话说明为什么这样判断。局部不明但其他反馈清楚时，分别写清楚。原文明说网站、电脑或其他场景时在此注明；没有说明不推断。'],
 ['回答与任务完成','明确涉及错答、回答质量、解释步骤、理解要求或完成指定任务的不足与改进诉求。仅“不回答”且没有其他依据时，反馈可为有，类别待定。'],
 ['收费与权益','明确涉及付费价值、订阅门槛、价格、退款扣费、已购权益或可识别的提问次数限制。不能仅凭不明资源词推断收费机制。'],
 ['运行体验','明确登录或访问失败、报错、卡顿、运行中断、响应慢等。不要从错答、功能缺失推断技术故障。'],
 ['界面与广告','明确布局、输入入口、显示、选择操作或广告干扰方面的问题。广告被提到不自动等于广告有问题。'],
 ['入门求助','明确不知道如何使用或激活产品。普通解题请求不属于产品入门求助。仍可按证据记录此类，不用为任何类别凑样本。'],
 ['多类与局部待定','多个问题都有独立证据时可填多类。某一类明确但另一问题不明，可填“明确类别；待定”，并在G列写清哪部分待定。同一现象不重复推断多个原因。'],
 ['没有答案提示','本次请独立填写，不先向AI索要本条的翻译、标签或选项。需要翻译才能判断时，标“部分能理解”或“无法判断”，在G列注明待语言复核。'],
 ['正面与负面','整体正面仍可能包含具体问题、限制或请求。低分、负面语气也可能只有泛泛差评。不要仅凭转折词或原文中的星级判断。'],
 ['评论中的主张','只记录作者说了什么，不验证真实故障、扣款或成绩变化，不猜技术原因和收费周期。历史问题已经解决时也注明前后时间状态。'],
 ['完成后','保存同一文件并告诉我已完成的编号。先记录全部人工结果，再统一与冻结模型对照。遇到不确定可以保留，不因此无限补抽。'],
 ['样本范围','六应用各30条。每应用的1—2星、3星、4—5星各10条。已排除旧校准及训练开发记录并检查近重复。分层样本不代表总体问题比例。'],
 ['来源与版本','来源：GenAI-EdSent本地六应用子集，原评论截至2025年8月。分类规则v0.3。模型在抽样前固定。表格准备于2026-10-26。']
];
style(g,'A1:B23');
g.getRange('A2').values=[['填写说明']];g.getRange('A2').format.font={name:'Arial',size:16,bold:true};
g.getRange('A2:B2').format.rowHeight=28;
g.getRange(`A4:B${instructions.length+3}`).values=instructions;
g.getRange('A1:A23').format.columnWidth=23;
g.getRange('B1:B23').format.columnWidth=105;
g.getRange('A4:A22').format.fill='#EDF1F6';g.getRange('A4:A22').format.font.bold=true;
instructions.forEach((r,i)=>g.getRange(`A${i+4}:B${i+4}`).format.rowHeight=Math.max(50,Math.ceil(r[1].length/48)*18+18));
wb.recalculate();
assert.deepEqual(s.getRange('A6:B185').values,data.map(r=>[r.sample_id,r.text]));
assert.ok(s.getRange('C6:G185').values.flat().every(x=>x==null||x===''));
console.log((await wb.inspect({kind:'table',range:'独立填写!A5:D7',include:'values,formulas',tableMaxRows:3,tableMaxCols:4,maxChars:500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?',options:{useRegex:true,maxResults:5},maxChars:300})).ndjson);
for(const [sheetName,range,name] of [['独立填写','A2:E9','sample'],['独立填写','C5:G8','inputs'],['填写说明','A2:B13','guide1'],['填写说明','A14:B22','guide2']]){
  const blob=await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(`${dir}/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
}
const file=`${dir}/独立人工测试180条.xlsx`;
await(await SpreadsheetFile.exportXlsx(wb)).save(file);
const imported=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
assert.deepEqual(imported.worksheets.getItem('独立填写').getRange('A6:B185').values,data.map(r=>[r.sample_id,r.text]));
assert.ok(imported.worksheets.getItem('独立填写').getRange('C6:G185').values.flat().every(x=>x==null||x===''));
await fs.writeFile(`${dir}/workbook_verification.json`,JSON.stringify({source_rows:180,originals_equal_after_export_import:true,human_input_cells:900,all_human_inputs_blank:true,sheets:['独立填写','填写说明'],no_AI_labels_or_per_item_hints:true},null,2));
console.log('Saved and reimported: 180 exact originals, 900 blank input cells.');
