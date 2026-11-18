import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const path=`${dir}/独立人工校准60条.xlsx`;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem('独立填写');
const rows=[
['能理解','无','无',"it's something better than brainly",'用户选A：正面评价，无具体问题或请求；比较的具体方面不明。'],
['能理解','无','无','the perfect app for solving math','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','有','收费与权益',"I don't recommend this app for people who can't afford like me",'用户选A：费用对评论者构成使用门槛；具体价格和收费方式不明。'],
['部分能理解','有','回答与任务完成',"doesn't even know normal ela",'用户选A：评论者称应用处理不了普通ELA内容；具体题目及原因不明。'],
['能理解','无','无','grade 11 November question paper life orientation','用户选A：普通查询或题目内容，无具体体验反馈。'],
['部分能理解','有','收费与权益','it keeps making me pay for it','用户选A：反复遇到付费要求；反复下载安装和删除的原因未说明，不另归运行体验。'],
['能理解','有','收费与权益；回答与任务完成',"7 dollars a week and the answers aren't even right?",'用户选A：对每周7美元费用不满，并称答案不对；bird的指代不明，不补充解释。'],
['能理解','无','无','This app is very good I like it','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['部分能理解','有','收费与权益','Buy upgrade to continue to use it','用户选A：继续使用需要购买升级服务；具体价格和权益不明。'],
['能理解','无','无',"it's really good for student",'用户选A：正面评价，无具体问题或请求；未补充理由。']
];
assert.deepEqual(s.getRange('A56:A65').values.flat(),Array.from({length:10},(_,i)=>`C${String(i+51).padStart(3,'0')}`));
assert.ok(s.getRange('C56:G65').values.flat().every(x=>x==null||x===''));
const texts=s.getRange('B56:B65').values.flat();
rows.forEach((r,i)=>r[3].split('\n').forEach(q=>assert.ok(texts[i].includes(q),`C${i+51}: ${q}`)));
await fs.copyFile(path,`${dir}/before_51_60.xlsx`);
s.getRange('C56:G65').values=rows;
wb.recalculate();
assert.deepEqual(s.getRange('C56:G65').values,rows);
const preview=await wb.render({sheetName:s.name,range:'C56:G65',scale:1,format:'png'});
await fs.writeFile(`${dir}/filled_51_60.png`,new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/candidate_51_60.xlsx`);
await fs.writeFile(`${dir}/values_51_60.json`,JSON.stringify(rows,null,2));
console.log('C051-C060 candidate saved.');
