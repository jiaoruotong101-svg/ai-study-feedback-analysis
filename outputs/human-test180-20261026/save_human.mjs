import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/projects/Study/outputs/human-test180-20261026';
const file=`${dir}/独立人工测试180条.xlsx`;
const data=JSON.parse(await fs.readFile(`${dir}/blind_sample.json`,'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const s=wb.worksheets.getItem('独立填写'),g=wb.worksheets.getItem('填写说明');
assert.deepEqual(s.getRange('A6:B185').values,data.map(x=>[x.sample_id,x.text]));
assert.ok(s.getRange('C6:G185').values.flat().every(x=>x==null||x===''));
if(process.argv.includes('--inspect')){
 const b=await wb.render({sheetName:'独立填写',range:'C5:G8',scale:1,format:'png'});
 await fs.writeFile(`${dir}/before-save.png`,new Uint8Array(await b.arrayBuffer()));
 console.log(JSON.stringify(g.getRange('A4:B22').values));
 process.exit(0);
}
const categories={T:'回答与任务完成',P:'收费与权益',R:'运行体验',U:'界面与广告',Q:'待定',O:'其他候选'};
// Each line transcribes the option accepted in this conversation; no model predictions are read.
const lines=`1 N 表达满意，无具体问题。
2 N 赞扬数学答案，无具体问题。
3 N 肯定易用性，无具体问题。
4 N 肯定速度和实用性，无具体问题。
5 R 黑屏、停留在应用名称画面及无法卸载；不推断原因。
6 P 获取答案需付费，不判断价格太贵。
7 P,Q 会员门槛明确；energy资源含义待定，i m pooped up不规范，待语言复核，不推断故障。
8 N 肯定对学生的帮助。
9 Q,O 其他候选：政治倾向。用户评价网站立场，不认定偏向属实，不直接视为手机端体验。
10 N 正面印象，不能确定是否使用过。
11 N 肯定知识丰富，无具体问题。
12 N 没用过还是现在不用不明确，无具体使用问题。
13 T 用户称答案全错；f疑似粗口缩写，含义不明，不认定已核实。
14 T,Q 答案错误明确；操作令人沮丧但缺乏细节，该部分类别待定。
15 U,P 广告不满及10题限制；不推断限制周期或付费能否解除。
16 N 正面预期，不凭将来时判断是否使用过。
17 N 泛泛差评，未说明具体哪里无用。
18 N 对学生适用性的一般好评。
19 P 付费异议；cheating指向待定，待语言复核，不认定欺诈。
20 N 功能介绍和赞扬；text具体操作不清，保留暂译。
21 P 用户选B，将1/1归为使用额度限制；具体含义和周期不明。
22 N 认可并推荐学生使用。
23 N 一般性赞扬，原句零散。
24 Q 不起作用但无具体表现，不区分运行故障与任务问题。
25 T 用户称回答不准确，不核实错误比例。
26 T 图示需求未满足，不认定完全不支持图示。
27 N 整体赞扬幽默感，不凭6.5分推断问题。
28 T 重复旧问题、回答越积越长、新问题未获回答；不推断技术原因。
29 N 认可和感谢，保留不自然表达的暂译。
30 N 肯定帮助作用和喜爱。
31 N 一般性好评。
32 T 写作请求未完成，提示处理量或长度问题；300 letter不改成300单词，不推断技术原因或付费限制。
33 R 根据暂译记录联网使用不满；online work句意不完整，待语言复核。
34 T 理解为答案或结果不准确，没有错误示例。
35 U 广告干扰，不推断广告形式或付费去除。
36 N 一般性赞扬。
37 P 请求延长升级专业版前的使用时间，不推断期限和规则。
38 N 一般性好评。
39 U 广告多、重复且无法关闭，被迫重开是同一广告问题的后果，不单列运行故障。
40 P 付费门槛及儿童支付能力问题，不判断价格过高。
41 P 付费不满，明确请求免费或降价，具体价格未知。
42 N 对用途满意，未说明具体任务或问题。
43 N 表达感谢和帮助作用。
44 T 部分学科未覆盖，不推断具体学科或原因。
45 N 用户补充原话：正向反馈。肯定题目解释；具体问题或改进需求为无。
46 T 用户选B，理解为会计题解答能力问题；accounts暂译会计，待语言复核，不认定原因已证实。
47 T 答案从好变差，用户称全错，不核实错误比例。
48 N 试用后认可，未说明原先不喜欢的原因。
49 T,R 解题过程错误与处理速度慢，不推断技术原因。
50 R 登录耗时、使用速度慢；不称登录失败，stairs暂译stars。
51 N 肯定作业帮助和节省时间。
52 T 回答语言与请求或预期不一致，不认定完全不支持语言。
53 U,R 用户多选AB：搜索入口无法点击及搜索功能无法正常使用，同一描述保留双类，不推断原因。
54 N 肯定回答速度；句末故事部分含义不完整，待语言复核。
55 N 肯定解题帮助，学习困难不是应用问题。
56 T,R 问题理解或回答错误及用户所称故障，不再细分。
57 P 输入或扫描数量限制，不推断周期或付费解除。
58 P 对教育应用收费不满，不判断价格太贵。
59 P,O 其他候选：注册门槛。付费要求和注册要求；sing up暂译注册，不认定注册失败。
60 N 强烈正向评价。
61 U 广告过多。
62 U 广告频繁；浪费流量作为用户所述影响，不认定异常流量消耗。
63 P 大部分内容需付费的不满；不从能用的回答反推其他错误或故障。
64 P 用户称不知情扣款，不认定已核实或推断自动续费。
65 N 肯定数学解题帮助，继续保持不是具体改进需求。
66 N 肯定作业帮助并推荐。
67 P charged暂译收费，记录付费异议，待语言复核，不判断价格太贵。
68 ? 用户原话：负面评价，类别待定。是否有具体反馈未明确，保留不确定；Need ai不替作者修正。
69 N 一般性赞扬。
70 T 大多数答案错误是用户说法，不核实比例。
71 N 用户称成绩提高，不认定已核实或由应用造成。
72 N 一般性好评，保留不规范原句。
73 P 会员门槛，不认定所有功能均需付费。
74 T 答案错误，不推断原因。
75 R,O 其他候选：客服响应。回答卡顿、两次邮件未获回复；付费仅背景，不认定技术故障原因。
76 N 肯定效果并说明正确输入前提，未明确应用问题。
77 N 肯定帮助作用及减少烦恼。
78 P 退款请求；孩子误购为用户所述，不核实经过。
79 P 每日提问额度、付费门槛和价格不满；金额按原文，不推断订阅周期或卢比国家。
80 Q 扫描相关改进需求明确，复制图片具体含义不清，待语言复核，不补全。
81 N 肯定速度、解释和学习帮助。
82 N 肯定解题帮助，不会做题不是应用问题。
83 R 从能用变为不能正常工作并求助，不推断故障原因。
84 N 肯定作业用途。
85 T 用户选A，理解为回答内容多、阅读负担轻度不满。
86 U,T 广告不满及答案不准确，不推断变化原因。
87 N 泛泛负面评价，未说明原因。
88 N 体验、回答和建议正向评价，原句零散，保留暂译。
89 N 解题内容夹杂末尾喜爱；不因截断或拼接认定应用故障。
90 N 肯定对学生的帮助。
91 N 肯定作业用途。
92 T 暂译解释不足，原句不规范，待语言复核。
93 P 超过3张图片需付费，不推断周期或操作。
94 P 反复升级会员要求和支付困难，不认定所有功能收费或价格过高。
95 N 肯定答案帮助和免打字，不推断输入方式。
96 T 回答错误与不可靠，不核实错误比例。
97 P,T,O 用户选B。其他候选：客服响应；退款、取消订阅、失败更多及用户所称推诿，不推断技术原因。
98 T 理解为部分解答错误；原文未明确答案，保留指代不确定。
99 T 用户选B，理解为回答语言不符合预期；原文未明确回答或界面，保留解释依据。
100 Q 不起作用但表现不明，不区分运行和任务能力。
101 N 正向评价，不凭would判断使用经历。
102 P 付费问题明确，无法细分收费不满或支付操作问题。
103 P 免费聊天额度不足，不推断数量和周期。
104 N 正向评价；工作场景或运行表现不明确，保留暂译。
105 N 正向评价与推荐；Kai含义不明，保留待语言复核。
106 P 安装后发现答案付费；网页未承诺免费，不认定虚假宣传。
107 N 一般性评价，未说明具体改进内容。
108 P 特殊功能付费不满，不推断功能或价格太贵。
109 N 肯定帮助作用，不认定能回答所有问题。
110 T 答案错误及方法复杂，不认定二者因果。
111 N 一般性正向评价。
112 N 一般性正向评价。
113 U 广告过多。
114 T 答案错误，不认定所有答案均已核实。
115 T,Q 未提供书中引文；points含义待定，待语言复核，不直接归为积分收费。
116 N 肯定并推荐；chiaos不明，待语言复核，不保证通过考试。
117 N 一般性评价，未说明具体改进内容。
118 N 未订阅仍体验好；so for暂译so far，不视为收费不满。
119 T 基础数学以外任务能力不满，不认定真实能力范围或原因。
120 P 反对强制付费，希望广告支持；未抱怨现有广告，不单列广告类。
121 N 肯定帮助作用。
122 N 泛泛差评并劝退，未说明问题。
123 N 一般性正向评价。
124 P 两条消息限制，不推断周期或付费解除。
125 N 一般性赞扬。
126 P consists Money暂译需要付费，待语言复核，不判断价格太贵。
127 N 肯定选择功能及不催促订阅；99.56币种和含义不明，不视为收费不满。
128 N 肯定简单可靠。
129 U 历史问题已解决：文字选项更新后恢复；不计为当前仍存在的问题，不推断技术原因。
130 N 肯定写作措辞帮助，eassy按essay理解。
131 N 感谢解题帮助。
132 R 反复自动退出登录及修复请求，不推断原因。
133 P 付费使用门槛，不认定所有功能都收费。
134 T 部分答案错误，体谅开发者不改变记录。
135 T 不太准确；最后一句含义不清，待语言复核，不补成答错问题。
136 P,O,Q 其他候选：评分提示。付费要求、评分提示；拍照后未获帮助类别待定，不推断识别失败。
137 N 一般性正向评价。
138 T 用户称每题答错，不认定全部已核实。
139 N 肯定答案过程解释并推荐。
140 T 问题不清时可能答错为用户所述条件，不扩大或核实因果。
141 N 肯定易用性，up暂译app。
142 T 回答错误，不核实比例。
143 N 肯定理解作业的帮助。
144 N 肯定帮助作用。
145 P 收费异议，不判断价格太贵。
146 N 正向评价，不确定是否已使用。
147 N 褒贬混合，未描述具体问题。
148 N 肯定易用性。
149 N 表达偏好，比较对象和原因不明。
150 N 一般正向评价，肯定复查用途，保留拼写修正说明。
151 U,T 广告多及回答错误。
152 Q 无法使用，原因不明，不推断故障、收费或不会操作。
153 N 肯定速度、答案和解释。
154 N 肯定容易获得答案。
155 T 用户选B，未提供答案归为任务完成；后半句语义不清，待语言复核，不额外判断答案错误。
156 P 提问需积分、获取积分需做任务；未提付钱，不推断收费。
157 N 肯定理解题目的帮助。
158 T 请求不同课程体系，公式差异不等于错误；atach暂译attach，待语言复核。
159 N 泛泛负面指控，无具体表现，不认定欺诈或收费问题。
160 T 请求小学阶段和人文学科支持，不认定现有功能完全不支持。
161 N 肯定回答帮助，不认定能回答一切。
162 N 正向评价，按拼写错误理解。
163 N 一般性正向评价。
164 R 回答等待久，2—3工作日可能夸张，不当作核实耗时。
165 Q 用户选B并问：这个应该再说广告多，界面与广告？保留广告猜测；原文未提广告，类别待定，未将猜测作事实。
166 N 肯定答案与分步解释。
167 Q 对立即更新提示的疑问，版本更新还是其他升级不明，不归为收费。
168 T 图片展示答案需求；贪心指向不明，不推断收费或广告，cery暂译very。
169 N 一般性正向评价。
170 N 肯定学生适用性。
171 N 肯定效果；alex含义不明，待语言复核，不补全。
172 ? 原文主语I，可能是自己未答对；不改成应用回答错误，是否具体反馈及类别待定，待语言复核。
173 R 回答速度慢，不推断原因。
174 N 正向评价并推荐。
175 T,P 文字输入却提示图片模糊、答案错误及重复提交扣积分；不推断积分付费，不额外判断故障。
176 N 肯定帮助作用，不从符号表情推断其他含义。
177 N 正向评价和推荐。
178 P 金币机制不满及付费后不受限需求；末句暂译，不确定是否已付费，不推断金币获取方式。
179 P 收费不满，无法细分具体问题。
180 T 答案错误，不推断原因。`;
const choices={21:'B',46:'B',53:'AB',68:'负面评价，类别待定',97:'B',99:'B',155:'B',165:'B（这个应该再说广告多，界面与广告？）'};
const rows=lines.split('\n').map((line,i)=>{
 const [,num,code,note]=line.match(/^(\d+) (\S+) (.+)$/);assert.equal(+num,i+1);
 const cats=code==='N'?'无':code==='?'?'待定':code.split(',').map(c=>categories[c]).join('；');
 return {...data[i],choice:choices[num]||'A',feedback:code==='N'?'无':code==='?'?'不确定':'有',categories:cats,note,method:'人工判定；AI提供翻译与候选选项；未展示冻结模型预测',independent_english_comprehension:null};
});
assert.equal(rows.length,180);
assert.equal(rows.filter(x=>x.feedback==='不确定').length,2);
const backup=`${dir}/before-human-write-20261030.xlsx.bak`;
await fs.copyFile(file,backup,1);
s.getRange('A2').values=[['人工判定 180条（对模型预测盲态）']];
s.getRange('A3').values=[['AI提供翻译与候选选项，用户逐条作最终判断。未展示模型预测。原文理解能力未单独测量，C列留空。']];
s.getRange('D6:G185').values=rows.map(x=>[x.feedback,x.categories,x.text,`用户选择：${x.choice}。${x.note}`]);
rows.forEach((x,i)=>{
 const height=Math.max(100,Math.ceil(x.text.length/48)*17+20,Math.ceil((x.note.length+20)/21)*17+20);
 s.getRange(`A${i+6}:G${i+6}`).format.rowHeight=height;
});
const replacements={
 '本次任务':'已完成人工判定180条。AI提供中文翻译、逐条候选标签及解释；用户声明最终判断由本人作出。未展示冻结模型预测，对模型预测保持盲态。',
 '填写位置':'已将本次对话的最终选择写入D—G列，保留原文和待定项。C列未填写：没有单独询问用户能否独立理解英文，不由接受翻译推断语言能力。',
 'C 能否理解原文':'本轮未测量独立英文理解能力，保留空白。G列注明暂译、不明词语及待语言复核；空白不等于无法理解。',
 'F 原文证据':'本次回填保留完整原文作证据上下文；由助手复制，不是用户亲自圈选的证据片段。',
 'G 理由／待定原因':'用户选择及其接受的选项解释由助手整理，非用户逐字自述。用户额外备注按原话保留，推测与事实分开。',
 '没有答案提示':'方法说明：人工判定，AI提供翻译与候选选项；未展示待评模型预测。候选选项含具体分类解释，可能产生提示影响，不能称为完全无提示的独立标注。',
 '完成后':'180条已完成。H068、H172的具体反馈状态仍不确定，其余类别待定项照实保留。后续可与冻结模型比较，报告为对模型预测盲态的提示辅助人工评测。',
 '来源与版本':'来源：GenAI-EdSent本地六应用子集，原评论截至2025年8月。模型在抽样前固定。人工判定来自本次对话，2026-10-30回填；不依据模型修改用户选择。'
};
const guides=g.getRange('A4:B22').values.map(([key,val])=>[key==='没有答案提示'?'标注方式与盲态':key,replacements[key]||val]);
g.getRange('A4:B22').values=guides;
guides.forEach((r,i)=>g.getRange(`A${i+4}:B${i+4}`).format.rowHeight=Math.max(50,Math.ceil(r[1].length/46)*18+18));
wb.recalculate();
assert.deepEqual(s.getRange('A6:B185').values,data.map(x=>[x.sample_id,x.text]));
await fs.writeFile(`${dir}/human_decisions_20261030.json`,JSON.stringify(rows,null,2));
for(const [sheetName,range,name] of [['独立填写','D5:G8','saved-decisions'],['填写说明','A4:B7','saved-method']]){
 const b=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(`${dir}/${name}.png`,new Uint8Array(await b.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(file);
const reread=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
assert.deepEqual(reread.worksheets.getItem('独立填写').getRange('A6:G185').values,s.getRange('A6:G185').values);
const counts={};rows.forEach(x=>counts[x.feedback]=(counts[x.feedback]||0)+1);
await fs.writeFile(`${dir}/human_write_verification.json`,JSON.stringify({date:'2026-10-30',rows:180,counts,all_originals_preserved:true,all_written_decisions_reimported_equal:true,english_comprehension_unmeasured:true,model_predictions_not_read:true,choice_exceptions:choices},null,2));
console.log(JSON.stringify({saved:file,counts,verified_rows:180}));
process.exit(0);

