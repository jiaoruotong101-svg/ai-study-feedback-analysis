import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const dir = 'D:/projects/Study/outputs/human-review-20261020';
const source = 'D:/projects/Study/outputs/genai-edsent-audit-20261016/review-expanded/reviewed_all270.jsonl';
const raw = await fs.readFile(source, 'utf8');
const all = raw.trim().split(/\r?\n/).map(JSON.parse);
const rows = all.filter(r => r.flags.split(',').some(f => ['uncertain','language','mild','novel','pilot_boundary'].includes(f)));
const questions = {
R030:'“为什么有人愿意付费”是否已经表达了付费价值不满，还是只有泛泛贬低？原文是否支持更具体的收费问题？',
R032:'“horrible answers”能否定位到回答质量问题？请区分“质量差”与“明确错答”，不要补出未提及的错误。',
R040:'“not understanding”是否明确指应用不理解用户，还是也可能是用户看不懂？信息是否足够归类？',
R051:'“bad ui”和“limited resources”分别支持什么判断？资源少具体指什么能否确定？不确定的部分请保留。',
R052:'“很好，但收费”是在表达改进诉求／轻度异议，还是中性说明收费事实？你依据哪个词判断？',
R075:'“新用户，不知道怎么用”是否是可处理的求助？它与尚未使用、尚无评价的情况如何区分？',
E006:'“尽管收费，仍然很好”是否包含可处理的收费异议，还是只有正面评价？请说明判断标准。',
E010:'这里的 accountability 能否结合整句可靠理解？是否包含明确的体验问题或请求？不能确定就保留待定。',
E015:'你能可靠理解这段混合／转写语言吗？若能，它是在表达收费异议还是仅说明收费事实？若不能，请标无法判断。',
E016:'索要访问权限是否被表达为异议？具体权限能否确定？若有反馈，现有五类能否容纳，还是应保留其他候选？',
E019:'这句话是感谢、请求回答，还是二者兼有？其中混合语言是否影响判断？不懂的部分请指出。',
E021:'除负面评价外，有没有足够明确、能定位的产品问题？不清楚的词是否使整条无法判读？',
E026:'原文是否分别表达登录失败和找不到帮助／客服？是否应记录多个类别？客服内容是否适合现有类别？',
E029:'询问网站是否宕机，是否已经构成具体访问问题／求助？它涉及 PC 网站端，是否建议纳入本研究并单独标端？',
E038:'“只能做基础数学”和“大多数功能收费”是否是两个独立反馈？原文能否区分能力限制与付费限制？',
E044:'要求“用方程形式回答”是否是具体改进请求？应归回答呈现／解释、其他类别，还是现有信息不足？',
E051:'“not answering like other apps”是完全不回答，还是回答质量不如别的应用？能否只确定较宽泛的反馈类别？',
E052:'⚡ 在这条评论中指什么，能否仅凭原文确定？是否有明确的消耗不满？若具体含义不明，怎样保留反馈？',
E053:'你能可靠理解混合语言吗？若能，请分别核对是否说了信息错误、纠正后仍重复；若不能，不要照抄参考标签。',
E063:'你能从这段重复拼接内容中识别出明确的产品体验反馈吗？请区分确认无关与因不懂语言而无法判断。',
E065:'“can help”是在讲已经发生的帮助还是未来期待？原文能否证明尚未使用？是否有具体问题或请求？',
E067:'退款请求是否明确？“hard to reach”具体指联系不上、操作困难还是其他？能否增加第二类别？',
E091:'这句不完整的话能否可靠理解？若不能，标无法判断，不必补全作者想说的话。',
E092:'你是否懂这句口语？若懂，请写出大意，并判断是否包含可定位问题；若不懂，请保留待语言复核。',
E100:'“多数时候不给答案”支持什么现象？原文能否区分运行故障、任务无法完成或其他原因？允许类别待定。',
E102:'“sport”是否能确定为拼写错误？整句是否足以支持乌尔都语相关能力问题，还是只能保留疑似含义？',
E112:'“runs out of bars”是什么意思，原文能否确定？是否明确表达了不满？其余拼写问题是否影响归类？',
E115:'“But it give plenty explanations”是在嫌解释过多，还是仍在赞扬？除了 but，有没有支持不满的证据？',
E119:'“will aid”能否确定作者尚未使用，还是只表达预期收益？是否包含具体反馈？不要把时态直接当使用记录。',
E121:'你能可靠理解这段语言吗？若能，请核对是否明确指出不支持某种语言；若不能，请保留待语言复核。',
E124:'无法选中文字输入入口，应归界面问题、运行问题还是两类？两类是否有独立证据，还是同一现象重复标记？',
E127:'这句话是推荐安装、求助还是无法理解？请只按原文可确认的信息判断。',
E133:'是否明确有“两次提问限制”和截图方向问题？截图描述具体能确认到什么程度？是否支持多个类别？',
E137:'“not answering”能否确定具体反馈存在？能否区分不返回答案、任务不会做或运行故障？类别不明可保留待定。',
E140:'“喜欢，但得付费”是在提出收费异议还是说明事实？与 R052、E006 的判断标准是否一致？',
E145:'扫描所需 energy 的问题具体是什么？能否确定是额度不足／收费，还是只能保留未细分的具体反馈？',
E150:'你能可靠理解转写语言吗？若能，分别核对是否有订阅门槛、服务器问题；若不能，请保留待语言复核。',
E163:'句末 pa 是否影响理解？全文是赞扬总结功能，还是提出总结请求？是否存在具体问题？',
E167:'你能可靠理解这句语言吗？若能，它是直接发一道题的指令，还是对应用能力的反馈？若不能，请保留待定。',
E177:'“confuses in itself”和“low time”分别能确认什么？能否定位问题，还是只有含混不满？不要自动归为响应慢。'
};
assert.equal(rows.length,40);
assert.equal(new Set(rows.map(r=>r.sample_id)).size,40);
assert.deepEqual(new Set(Object.keys(questions)),new Set(rows.map(r=>r.sample_id)));
// Preserve source order: six pilot boundary records, then the expanded records.
const workbook = Workbook.create();
const review = workbook.worksheets.add('逐条复核');
const guide = workbook.worksheets.add('填写说明');
const reference = workbook.worksheets.add('AI原判断_填后再看');
function base(s,range) {
  s.showGridLines=false;
  s.getRange(range).format.font={name:'Arial',size:11,color:'#243247'};
  s.getRange(range).format.wrapText=true;
  s.getRange(range).format.verticalAlignment='top';
}
function header(s,range) {
  s.getRange(range).format={fill:'#334760',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};
  s.getRange(range).format.rowHeight=38;
}
base(review,'A1:H45');
review.getRange('A2').values=[['优先人工复核 · 40条']];
review.getRange('A2').format.font={size:16,bold:true};
review.getRange('A3').values=[['先读“填写说明”。只填写黄色 D—H 列；每条疑点在 C 列。先自行判断，再看 AI 参考。']];
review.getRange('A2:H3').format.wrapText=false;
review.getRange('A5:H5').values=[['编号','评论原文（完整）','这条具体要判断什么','能否理解原文','是否有具体反馈','类别（可多选，手填）','支持判断的原文','理由／疑点答复']];
review.getRange('A6:H45').values=rows.map(r=>[r.sample_id,r.text,questions[r.sample_id],null,null,null,null,null]);
header(review,'A5:H5');
const widths={A:10,B:66,C:58,D:18,E:18,F:28,G:36,H:48};
for(const [c,w] of Object.entries(widths)) review.getRange(`${c}1:${c}45`).format.columnWidth=w;
review.getRange('D6:H45').format.fill='#FFF4CC';
review.getRange('D6:D45').dataValidation={rule:{type:'list',values:['能理解','部分能理解','无法判断']}};
review.getRange('E6:E45').dataValidation={rule:{type:'list',values:['有','无','不确定']}};
rows.forEach((r,i)=>review.getRange(`A${i+6}:H${i+6}`).format.rowHeight=Math.max(112, Math.ceil(r.text.length/61)*17+20));
review.freezePanes.freezeRows(5);
review.freezePanes.freezeColumns(1);
review.tables.add('A5:H45',true,'HumanReview');

const instructions=[
['复核目的','先澄清分类边界。本轮是有针对性的疑难样本复核，不用于计算整体准确率、人工一致性或全量问题比例。'],
['本轮范围','40条：新增样本34条＋首批边界6条。新增语义不确定22条、语言待核10条，重叠1条，合并31条；另补轻度异议／新类别3条。'],
['怎么开始','先在“逐条复核”读原文和问题，只填黄色 D—H 列。可先做前6条，分次保存。评分没有放在填写页，但少数正文自带星级。'],
['D 能否理解原文','选“能理解／部分能理解／无法判断”。不懂的语言不用猜。只理解部分时，只对能确认的内容判断，并在 H 写出不懂的部分。'],
['E 是否有具体反馈','选“有／无／不确定”。有＝能定位的问题、限制、改进请求或使用求助，轻度异议也需按原文判断。只有“很好／很差”通常选无。'],
['F 类别','若 E=有，填下方五个类别之一或多个，用中文分号分隔。现有类别装不下时填“其他候选：具体内容”；分类不清填“待定”。E=无填“无”；E=不确定填“待定”。'],
['G 原文证据','复制支持你判断的最短原文片段。多类别分别给证据。无法读懂时可填“无法判读”；没有具体反馈时保留能体现好评／泛泛差评等的片段。'],
['H 理由与问题答复','用一句或几句话回答 C 列疑点。无具体反馈时可说明：正面评价、泛泛差评、使用前期待、无关或语义不明。没有证据的原因不要补。'],
['不会判断怎么办','可以填写 D=无法判断、E=不确定、F=待定、G=无法判读，H 写“语言不熟悉”等原因。这是有效复核记录，但仍需后续解决。'],
['何时看 AI 参考','完成自己的判断后，再按编号看第三张表。原判断仅是待核对的参考，不能当标准答案。若改判，在 H 保留最初判断及修改原因。'],
['回答与任务完成','回答质量、步骤解释、理解需求、不能完成任务。只记用户表达的现象，不猜模型内部原因。'],
['收费与权益','付费门槛、次数额度、扣费退款、购买后权益。仅出现钱或能量等词，不足以自动归类。'],
['运行体验','打不开、登录失败、报错、明确响应慢等。没有答案不一定是运行故障；原因不明时允许类别待定。'],
['界面与广告','界面操作、布局、广告干扰等明确问题。若与运行故障是同一现象，说明为何需要或不需要双标签。'],
['入门求助','不会用、询问激活／使用方法等。求助不等于已证实产品故障。'],
['其他候选','例如权限或客服问题，只有在你确认原文支持、现有类别不适合时填写。当前不自动新增正式类别。'],
['填写示例（虚构）','原文：Great app, but I cannot log in. → 能理解；有；运行体验；cannot log in；肯定产品但明确表示无法登录。'],
['完成之后','保存文件并告诉我已完成哪些编号。我会汇总分歧和待定项，再与你确定规则。不要删除行或改编号、原文、AI参考。'],
['保留边界','本轮没有更新任何原标签，也没有重新抽样。40条之外的230条尚不因此获得人工确认。之后需另准备独立评估样本。'],
['来源','项目 review-expanded/reviewed_all270.jsonl；原规则 frozen_codebook_v01.md；源结果日期2026-10-16，本表整理日期2026-10-20。']
];
base(guide,'A1:B24');
guide.getRange('A2').values=[['填写说明']];
guide.getRange('A2').format.font={size:16,bold:true};
guide.getRange('A4:B23').values=instructions;
guide.getRange('A1:A23').format.columnWidth=24;
guide.getRange('B1:B23').format.columnWidth=108;
guide.getRange('A4:A23').format.font.bold=true;
instructions.forEach((r,i)=>guide.getRange(`A${i+4}:B${i+4}`).format.rowHeight=Math.max(46,Math.ceil(r[1].length/55)*18+14));
guide.getRange('A4:A23').format.fill='#EDF1F6';

base(reference,'A1:J45');
reference.getRange('A2').values=[['AI 原判断（未经独立人工复核）']];
reference.getRange('A2').format.wrapText=false;
reference.getRange('A2').format.font={size:16,bold:true};
reference.getRange('A3').values=[['来源与填写页相同。下列字段原样保留；用于对照，不作为标准答案。']];
reference.getRange('A3').format.wrapText=false;
reference.getRange('A5:J5').values=[['编号','应用','原内容状态','原子类代码','原一级类别','原证据片段','原判断说明','原标记','原评分','原评论ID']];
const refs=rows.map(r=>[r.sample_id,r.app_name,r.content_status,r.issue_codes,r.category_groups,r.evidence_excerpt,r.review_note,r.flags,r.review_score,r.review_reviewId]);
reference.getRange('A6:J45').values=refs;
header(reference,'A5:J5');
for(const [i,w] of [10,32,22,30,28,48,54,28,10,40].entries())reference.getRangeByIndexes(0,i,45,1).format.columnWidth=w;
reference.getRange('A6:J45').format.rowHeight=100;
reference.freezePanes.freezeRows(5);
reference.freezePanes.freezeColumns(1);
reference.tables.add('A5:J45',true,'OriginalAIReference');

workbook.recalculate();
assert.deepEqual(review.getRange('A6:C45').values,rows.map(r=>[r.sample_id,r.text,questions[r.sample_id]]));
assert.ok(review.getRange('D6:H45').values.flat().every(v=>v==null||v===''));
assert.deepEqual(reference.getRange('A6:J45').values,refs);
console.log((await workbook.inspect({kind:'table',range:'逐条复核!A5:E7',tableMaxRows:3,tableMaxCols:5,maxChars:1800})).ndjson);
console.log((await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:500})).ndjson);
for(const [name,range,file] of [['逐条复核','A5:E9','review'],['填写说明','A2:B13','guide'],['AI原判断_填后再看','A5:G8','reference']]) {
  const blob=await workbook.render({sheetName:name,range,scale:1,format:'png'});
  await fs.writeFile(`${dir}/${file}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(workbook)).save(`${dir}/优先人工复核40条.xlsx`);
assert.equal(await fs.readFile(source,'utf8'),raw);
await fs.writeFile(`${dir}/verification.json`,JSON.stringify({selected:40,new:34,pilot:6,selection_flags:['uncertain','language','mild','novel','pilot_boundary'],source_sha256:crypto.createHash('sha256').update(raw).digest('hex'),source_unchanged:true,source_fields_match:true,human_fields_blank:true,ids:rows.map(r=>r.sample_id)},null,2));
console.log('EXPORTED 40 records; source unchanged; human fields blank.');
