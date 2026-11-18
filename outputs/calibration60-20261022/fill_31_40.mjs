import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const path=`${dir}/独立人工校准60条.xlsx`;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem('独立填写');
const rows=[
['能理解','无','无','Thanks for your workdone i really appreciate it','用户选A：正面评价或感谢，无具体问题或请求；未补充理由。'],
['能理解','无','无','Fast and helps with writing homework','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['部分能理解','有','其他候选：获取答案的附加要求','make me do stuff for sum answer like follow u','用户选A：不满为了拿到答案还要关注等额外操作，暂记其他候选；不推断涉及付费。口语缩写按暂译理解，具体措辞仍有歧义。'],
['部分能理解','有','回答与任务完成；收费与权益','incorrect answer\nlimited chance to solve the question\nafter the chance over it asking for money','用户选A：记录评论者所述的答案错误、解题次数限制及用完后要求付费。原文另有含义不清的句子，不补全；未补充理由。'],
['能理解','有','回答与任务完成','please (improve this app) like an app that can create a graph like this 📉📈 not a graph like using this ***** and /////////','用户选A：请求用图表呈现结果，避免字符拼图；归为回答与任务完成中的结果呈现需求。'],
['能理解','无','无','this apps haped me a lot','用户选A：正面评价，无具体问题或请求；haped按上下文理解为helped，未补充理由。'],
['能理解','无','无','This app healping me for all of may assesment','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','Worst kind of app. All gimic','用户选A：泛泛差评，无可定位的具体问题；“全是噱头”未指出具体问题。'],
['能理解','有','回答与任务完成','IT GOT ALL THE QUESTIONS I ASKED WRONG','用户选A：记录评论者称题目答错；“我没通过”另作用户自述，不认定两者存在因果关系。'],
['能理解','无','无','This is very helpful for those who seeks informations for a certain topic.','用户选A：正面评价，无具体问题或请求；未补充理由。']
];
assert.deepEqual(s.getRange('A36:A45').values.flat(),Array.from({length:10},(_,i)=>`C${String(i+31).padStart(3,'0')}`));
assert.ok(s.getRange('C36:G45').values.flat().every(x=>x==null||x===''));
const texts=s.getRange('B36:B45').values.flat();
rows.forEach((r,i)=>r[3].split('\n').forEach(q=>assert.ok(texts[i].includes(q),`C${i+31}: ${q}`)));
await fs.copyFile(path,`${dir}/before_31_40.xlsx`);
s.getRange('C36:G45').values=rows;
wb.recalculate();
assert.deepEqual(s.getRange('C36:G45').values,rows);
const preview=await wb.render({sheetName:s.name,range:'C36:G45',scale:1,format:'png'});
await fs.writeFile(`${dir}/filled_31_40.png`,new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/candidate_31_40.xlsx`);
await fs.writeFile(`${dir}/values_31_40.json`,JSON.stringify(rows,null,2));
console.log('C031-C040 candidate saved.');
