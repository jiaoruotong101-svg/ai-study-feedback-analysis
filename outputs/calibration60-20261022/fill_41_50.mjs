import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const path=`${dir}/独立人工校准60条.xlsx`;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem('独立填写');
const rows=[
['能理解','有','界面与广告','Why does it always take snaps some of us prefer typing','用户选A：希望更方便地选择文字输入；不据此认定文字输入功能完全不存在，未补充理由。'],
['能理解','有','运行体验；收费与权益','slow in searching\nneeds to pay in order to search','用户选A：搜索慢归运行体验，付费才能搜索归收费与权益；两项分别有原文证据。'],
['能理解','无','无',"It's the besttttttttt Ai app",'用户选A：正面评价，无具体问题或请求；未补充理由。'],
['部分能理解','有','收费与权益','it the best until time for paying','用户选A：整体认可应用，但把需要付费视为不足；具体价格和收费方式不明。'],
['部分能理解','无','无',"It's very smart and wide",'用户选A：正面评价，无具体问题或请求；wide的具体含义不明但不影响总体判断。'],
['部分能理解','有','收费与权益',"where's the ads? I don't have money",'用户选B：明确表示没钱并询问广告在哪，暂归收费与权益。是否想通过看广告使用功能，原文未明确，保留疑点。'],
['部分能理解','无','无','Super app, need most for academic performance','用户选A：正面评价，无具体问题或请求；原句省略较多，未补充理由。'],
['能理解','有','收费与权益','you have to pay for it to help u if u use it more than once','用户选A：用户所述的再次使用需要付费；笔记或回答质量未明确有问题。'],
['能理解','无','无','very very usefull app for doubt solving','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','5/5 it gives the right answer right away','用户选A：正面评价，无具体问题或请求；未补充理由。']
];
assert.deepEqual(s.getRange('A46:A55').values.flat(),Array.from({length:10},(_,i)=>`C${String(i+41).padStart(3,'0')}`));
assert.ok(s.getRange('C46:G55').values.flat().every(x=>x==null||x===''));
const texts=s.getRange('B46:B55').values.flat();
rows.forEach((r,i)=>r[3].split('\n').forEach(q=>assert.ok(texts[i].includes(q),`C${i+41}: ${q}`)));
await fs.copyFile(path,`${dir}/before_41_50.xlsx`);
s.getRange('C46:G55').values=rows;
wb.recalculate();
assert.deepEqual(s.getRange('C46:G55').values,rows);
const preview=await wb.render({sheetName:s.name,range:'C46:G55',scale:1,format:'png'});
await fs.writeFile(`${dir}/filled_41_50.png`,new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/candidate_41_50.xlsx`);
await fs.writeFile(`${dir}/values_41_50.json`,JSON.stringify(rows,null,2));
console.log('C041-C050 candidate saved.');
