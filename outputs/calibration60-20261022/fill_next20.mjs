import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/calibration60-20261022';
const path=`${dir}/独立人工校准60条.xlsx`;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem('独立填写');
const answers=[
['能理解','有','收费与权益','I wish you could get the answers for free instead of paying 32 USD a month','用户选A：希望免费获得答案，对每月32美元付费提出改进诉求。“通常给出正确答案”是正面评价，不记为问题；未补充理由。'],
['能理解','有','收费与权益','plz make it 0 cost aap','用户选A：提出免费使用的请求，不推断应用当前的具体收费方式；未补充理由。'],
['能理解','无','无','Very useful, but will change my rating after tweaking with it a while longer','用户选A：正面评价，无具体问题或请求；还会继续体验，不据此认定此前未使用。'],
['能理解','有','回答与任务完成','information is good but with not enough details','用户选A：信息细节不足，归回答与任务完成；不推断信息错误。'],
['部分能理解','无','无',"It's fantastic to use",'用户选A：正面评价，无具体问题或请求。末尾感谢对象含义不明，不影响前半句判断。'],
['部分能理解','有','收费与权益','I don\'t like how u have to use energy just to get the answer','用户选B：对获取答案要消耗energy表示不满，暂归收费与权益。energy具体含义未确认，不推断需要付费；仅给选项，未补充理由。'],
['部分能理解','有','回答与任务完成','only if it could give homework','用户选B：希望能处理与作业有关的任务，暂归回答与任务完成。give homework具体指什么不清楚，不能认定现有功能完全做不到；未补充理由。'],
['能理解','无','无','It helps so much thank you','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['部分能理解','有','回答与任务完成','shows everything except answers','用户选A：得不到答案，暂归回答与任务完成；不推断为什么没有显示答案；未补充理由。'],
['能理解','无','无','I love this app you can do your homework','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','You can answer your homework easily','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','无','无','just hope the app is the best','用户选A：一般性的正面期待，无具体问题或请求；不能据此判断作者是否已使用；未补充理由。'],
['能理解','有','其他候选：表格功能','Inclusion of table for accounting analysis will be a welcome development','用户选A：希望增加用于会计分析的表格功能，暂记其他候选；原文没有说明现有应用完全无法做会计分析。'],
['能理解','无','无','This app is so a scam and so bad','用户选A：泛泛差评，无可定位的具体问题；不推断发生扣费或欺诈。'],
['能理解','无','无','this application really help me in my homework','用户选A：正面评价，无具体问题或请求；未补充理由。'],
['能理解','有','回答与任务完成','IT GAVE ME THE WRONG ANSWER','用户选A：记录用户所述的答案错误，归回答与任务完成；没有独立核实答案。'],
['能理解','有','收费与权益','I thought I was buying a special deal for $5.99 but it took $70.33 of of mx debit card\nPlease give me a refund','用户选A：记录评论者所述的扣款金额争议和退款请求；实际扣款未独立核实；未补充理由。'],
['部分能理解','不确定','待定','I hate to use Star','用户选C：Star含义不明，是否有具体体验反馈及类别均待定，不推断是积分或额度。'],
['部分能理解','有','收费与权益','the limit is the problem','用户选B：对某种limit不满，暂归收费与权益；限制的具体对象、周期与机制不明；未补充理由。'],
['部分能理解','有','回答与任务完成','when I take a Pic on the number it will go to the wrong way','用户倾向“回答与任务完成”：可能是在说答案错误。原文只表述拍照后方向不对，不能确定是答案错误，故此类别暂定并保留语义疑点。']
];
assert.equal(answers.length,20);
assert.deepEqual(s.getRange('A16:A35').values.flat(),Array.from({length:20},(_,i)=>`C${String(i+11).padStart(3,'0')}`));
assert.ok(s.getRange('C16:G35').values.flat().every(v=>v==null||v===''));
const texts=s.getRange('B16:B35').values.flat();
answers.forEach((row,i)=>row[3].split('\n').forEach(quote=>assert.ok(texts[i].includes(quote),`C${i+11}: ${quote}`)));
await fs.copyFile(path,`${dir}/before_next20.xlsx`);
s.getRange('C16:G35').values=answers;
wb.recalculate();
assert.deepEqual(s.getRange('C16:G35').values,answers);
for(const [range,name] of [['C16:G21','next20_1'],['C22:G28','next20_2'],['C29:G35','next20_3']]){
 const blob=await wb.render({sheetName:s.name,range,scale:1,format:'png'});
 await fs.writeFile(`${dir}/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/next20_candidate.xlsx`);
await fs.writeFile(`${dir}/next20_values.json`,JSON.stringify(answers,null,2));
console.log('C011-C030 candidate saved.');
