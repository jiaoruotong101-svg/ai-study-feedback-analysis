import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const path=`${dir}/独立人工校准60条.xlsx`;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const sheet=wb.worksheets.getItem('独立填写');
const rows=[
['部分能理解','有','回答与任务完成；收费与权益',"it's not giving the right answer\nYou have to \"buy\" something to get advanced",'用户选A：两项具体反馈，答案不正确；更高级的功能似乎需要购买。购买内容不明；“You were looking for any more”含义不清，不补全。'],
['能理解','有','回答与任务完成','it cannot read correctly the directions in my assignment','用户选A：应用没能正确理解作业要求。不推断为文字识别故障。'],
['能理解','无','无','A really great and useful app for students','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','it will help in my postgraduate studies','用户选A：正面评价或期待，无具体问题或请求；不能仅凭将来时确定作者尚未使用。'],
['能理解','无','无','Is so perfect for my grandson','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','Very very helpful','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','有','收费与权益',"I don't want to pay I just need help with homework",'用户选A：不愿为作业帮助付费。原文没有说明价格或实际扣费；未补充理由。'],
['部分能理解','有','回答与任务完成；待定',"wrong answer\nThis app don't accept your age",'用户选A：错答归回答与任务完成；“不接受填写的年龄”是另一项具体反馈，类别待定，不推断原因。'],
['能理解','无','无','Excellent app helpful with everything I love it','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','有','收费与权益','Limit in Queries\nAsking Paid Membership for AI Use','用户选A：提问次数限制、使用AI功能要求购买会员，均归收费与权益；未补充理由。']
];
assert.deepEqual(sheet.getRange('A6:A15').values.flat(),Array.from({length:10},(_,i)=>`C${String(i+1).padStart(3,'0')}`));
assert.ok(sheet.getRange('C6:G15').values.flat().every(v=>v==null||v===''));
const originals=sheet.getRange('B6:B15').values.flat();
rows.forEach((r,i)=>r[3].split('\n').forEach(excerpt=>assert.ok(originals[i].includes(excerpt),`${i+1}: ${excerpt}`)));
await fs.copyFile(path,`${dir}/before_first10.xlsx`);
sheet.getRange('C6:G15').values=rows;
wb.recalculate();
assert.deepEqual(sheet.getRange('C6:G15').values,rows);
for(const [range,name] of [['C6:G10','filled1'],['C11:G15','filled2']]){
 const preview=await wb.render({sheetName:sheet.name,range,scale:1,format:'png'});
 await fs.writeFile(`${dir}/${name}.png`,new Uint8Array(await preview.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/filled_first10_candidate.xlsx`);
await fs.writeFile(`${dir}/first10_values.json`,JSON.stringify(rows,null,2));
console.log('Wrote ten responses to candidate workbook.');
