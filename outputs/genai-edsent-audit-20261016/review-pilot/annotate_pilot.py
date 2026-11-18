"""Exploratory assistant-reviewed annotations, not independent human ground truth."""
from pathlib import Path
import json
import pandas as pd
r=Path(__file__).parent
d=pd.read_json(r/'sample_with_metadata.jsonl',lines=True)
# Fields: labels | status | exact supporting text | Chinese interpretation.
# All 90 texts were read before revealing the separately stored rating fields.
# Some texts disclose their own ratings, so complete rating blinding is impossible.
notes={
1:'|preuse|gonna help|预期会有帮助，不能视为已验证的使用体验',
2:'|positive|helped me in the finals exams|自述考试帮助，未提出问题',
3:'|irrelevant||个人信息，与产品体验无关；报告不展示正文',
4:'TECH|issue|not working|应用无法工作，具体原因不明',
5:'ANSWER|issue|some answers are not corrected|部分答案错误；同时肯定帮助',
6:'ADS,PAY|issue|watch add to get energy|看广告获得的次数少，更新后限制；不能验证更新因果',
7:'|irrelevant|get the answers yourself|对使用此类应用的态度，不是具体产品故障',
8:'BILLING|issue|refund my 492 pesos|误购退款诉求，不能证实欺诈',
9:'|vague_negative|very disappointing|泛泛不满，没有可定位问题',
10:'|positive|helping me in my maths|肯定数学学习帮助',
11:'PAY|issue|need to pay more money|已付费后仍被要求付更多钱；是否错误扣费不明',
12:'UNDERSTAND|issue|my other question are all the same answers|不同问题重复回答；不能据此诊断模型记忆机制',
13:'|positive|very good app|笼统赞扬',
14:'ANSWER|issue|not every time the answer is correct|肯定实用但存在错答',
15:'|positive|so amazing|笼统赞扬',
16:'BILLING|issue|I need a refund|退款诉求，具体原因不明',
17:'|positive|NO ADS|赞扬快速且无广告，不能标记广告问题',
18:'|ambiguous|different and unusual|语义模糊，未明确提出问题',
19:'ANSWER|issue|not giving accurate answers|回答或信息不准确',
20:'EXPLAIN|issue|It jus gave me the answers only|只给答案，希望有公式和步骤；同时赞扬速度',
21:'PAY|issue|after three days without paying|试用后付费限制',
22:'TECH|issue|not opening|应用打不开',
23:'UNDERSTAND|issue|cannot let it solve word puzzles|任务无法完成，具体技术原因不明',
24:'|positive|I like it|表述不清但正向，无明确问题',
25:'|vague_negative|Some features aren\'t available|未指明功能和原因，暂不推断为收费或技术故障',
26:'|positive|really really good|笼统赞扬',
27:'ANSWER|issue|some Wrong answers|肯定解题但存在错答',
28:'|positive|all steps|赞扬步骤和准确性',
29:'PAY|issue|without money|付费门槛；不能据此认定诈骗',
30:'PAY|issue|Why would anyone pay|付费价值质疑，不推断错误扣费',
31:'PAY|issue|orders me to buy|使用时被要求购买',
32:'ANSWER|issue|horrible answers|回答质量差，未明确到错误或解释原因',
33:'PAY|issue|not paying for answers I can find online|相对免费替代品的付费价值不足',
34:'|positive|Helps so good|肯定作业帮助',
35:'PAY|issue|give the payment|希望取消付款要求',
36:'|positive|so useful for me|肯定数学学习用途',
37:'ONBOARD|issue|get an activation code|激活码获取困难或求助，不认定系统失效',
38:'|positive|i love it|笼统赞扬',
39:'|positive|interesting app|一般正向评价，使用经历未明确',
40:'UNDERSTAND|issue|not understanding|用户表示未被理解，但未给具体任务',
41:'PAY|issue|atleast give 10 questions free everyday|负担不起并建议每天十次免费额度',
42:'TECH|issue|doesn\'t even work|无法工作，原因不明',
43:'|positive|well defined illustrations|赞扬解释与速度',
44:'|preuse|just downloaded|刚下载，没有实质使用反馈',
45:'SPEED|issue|slow|速度慢并请求改进',
46:'ANSWER|issue|answer is wrong|答案错误',
47:'|positive|good ai answering machine|正向评价',
48:'PAY|issue|tried to make me pay|未获得答案并遇到付费要求，不额外推断错答',
49:'BILLING|issue|stole my money|资金损失指控，待核实，不能认定产品盗款',
50:'|vague_negative|policy\'s are too tight|规则过严但不知具体是哪项规则',
51:'UI|issue|bad ui and super limited resources|明确抱怨界面；资源少的含义不明，不推断收费或次数限制',
52:'PAY|issue|but this is paid|赞扬后以转折指出收费',
53:'PAY|issue|2 times per use|免费次数限制及付费解锁',
54:'|positive|explaining nicely|赞扬解释',
55:'|positive|Helps a lot|笼统赞扬',
56:'|positive|accurate and helpful|赞扬准确性',
57:'|vague_negative|Don\'t like|没有具体原因',
58:'|positive|work of AI is very nice|笼统赞扬',
59:'|positive|Best App|笼统赞扬',
60:'ANSWER,EXPLAIN|issue|explanation was hard to follow and wrong|答案错误且解释难理解',
61:'|positive|more information|肯定信息帮助',
62:'|positive|best app|笼统赞扬',
63:'PAY|issue|limited amount of questions|肯定帮助但抱怨可提问次数少',
64:'|vague_negative|made me fail|负面学习结果归因，未说明出错环节',
65:'|positive|helps my assignment|肯定作业帮助',
66:'|vague_negative|doesn\'t do want I expected|未满足预期但具体需求不明',
67:'PAY|issue|pay for unlimited questions|免费到付费限制变化；未明确断言现有答案变差',
68:'PAY|issue|pay to use the app|实际付费门槛与期待不符',
69:'|positive|helps me well|正向评价',
70:'PAY|issue|if your on a budget|肯定帮助但负担不起',
71:'|positive|useful for students|笼统赞扬',
72:'|positive|very good app|笼统赞扬',
73:'|positive|Well detailed explanation|赞扬详细解释',
74:'ENTITLEMENT|issue|NOT used the paid subscription on other devices|已付费权益不能跨设备使用；不认定是bug',
75:'ONBOARD|issue|don\'t know how to use this|新用户不会使用、寻求指导；尚无效果评价',
76:'|positive|reason I\'m passing|自述学习帮助',
77:'|positive|made it easier|肯定帮助',
78:'|positive|love using|肯定使用体验',
79:'|positive|helps with your homework|肯定作业帮助',
80:'SPEED|issue|too long to respond|响应时间长',
81:'PAY|issue|make it without payment|希望免费使用',
82:'ADS|issue|it has ads|广告导致不满并要求改进',
83:'ANSWER|issue|wrong answer at times|偶尔错答',
84:'|vague_negative|worst app|笼统差评',
85:'|positive|everything you need|笼统赞扬',
86:'|preuse|just downloading|正在下载，不能视为使用体验',
87:'|positive|love the experience|肯定体验，无具体维度',
88:'ADS,ANSWER,SPEED,TECH|issue|too many adds|广告多、错答、等待长及报错，多问题共存',
89:'|positive|good in mathematics|自述数学帮助',
90:'|positive|helpful for studying|笼统赞扬',
}
labels={'ANSWER':'回答质量','EXPLAIN':'解释与步骤','UNDERSTAND':'需求理解与任务完成','PAY':'付费门槛与使用额度','BILLING':'扣费争议与退款','ADS':'广告体验','TECH':'运行与访问故障','SPEED':'响应速度','UI':'界面易用性','ONBOARD':'入门与激活求助','ENTITLEMENT':'已购权益与跨设备使用'}
rows=[]
for _,row in d.iterrows():
 n=int(row.sample_id[1:]);cats,status,evidence,note=notes[n].split('|',3)
 if evidence: assert evidence.lower() in row.text.lower(),(n,evidence)
 rows.append({**row.to_dict(),'issue_codes':cats,'issue_labels':'；'.join(labels[z] for z in cats.split(',') if z),'content_status':status,'feedback_kind':'help_request' if n in [37,75] else 'mild_price_objection' if n==52 else 'complaint_or_improvement_request' if cats else 'no_specific_issue','has_actionable_feedback':bool(cats),'evidence_excerpt':evidence,'review_note':note,'annotation_source':'assistant exploratory review; not independent human gold'})
a=pd.DataFrame(rows)
a.to_json(r/'reviewed_90.jsonl',orient='records',lines=True,force_ascii=False,date_format='iso')
a.to_csv(r/'评论核验90条.csv',index=False,encoding='utf-8-sig')
summary={'n':len(a),'stratum_counts':a.groupby('stratum').size().to_dict(),'status':a.content_status.value_counts().to_dict(),'actionable_by_stratum':a.groupby('stratum').has_actionable_feedback.agg(['sum','count']).to_dict('index'),'labels':{v:int(a.issue_codes.str.split(',').apply(lambda x:k in x).sum()) for k,v in labels.items()},'app_results':a.groupby('app_name').has_actionable_feedback.agg(['sum','count']).to_dict('index'),'high_rating_issue_ids':a.loc[a.review_score.ge(4)&a.has_actionable_feedback,'sample_id'].tolist(),'not_low_issue_ids':a.loc[a.review_score.ge(3)&a.has_actionable_feedback,'sample_id'].tolist()}
(r/'pilot_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print(a.loc[a.has_actionable_feedback,['sample_id','review_score','app_name','issue_labels']].to_string(index=False))
