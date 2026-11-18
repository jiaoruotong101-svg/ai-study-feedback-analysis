from pathlib import Path
import json,pandas as pd
r=Path(__file__).parent
d=pd.read_json(r/'reviewed_all270.jsonl',lines=True)
status={'issue':'具体反馈或求助','positive':'正向无具体问题','vague_negative':'泛泛不满','preuse':'未使用或预期','irrelevant':'无关','ambiguous':'语义不明'}
rating={'low_1_2':'1—2星','mid_3':'3星','high_4_5':'4—5星'}
flags={'uncertain':'语义或归类待确认','mild':'轻度异议','language':'混合或非英语待确认','language_capability':'语言能力反馈','novel':'原规则未覆盖','off_domain':'场景可能偏离','format_request':'呈现形式请求','platform_web':'网站端反馈','pilot_boundary':'首批边界案例'}
headers=['编号','批次','应用','评分','评论时间','评分层','可处理反馈','一级类别','子类','内容判断','原始评论','证据片段','核验说明','待复核标记','原评论ID','核验来源']
rows=[]
for _,z in d.iterrows():
    rows.append([z.sample_id,z.batch,z.app_name,int(z.review_score),str(z.date),rating[z.stratum],'是' if z.has_actionable_feedback else '否',z.category_groups,z.issue_labels,status[z.content_status],z.text,z.evidence_excerpt,z.review_note,'；'.join(flags[f] for f in str(z['flags']).split(',') if f),z.review_reviewId,'AI辅助核验，非人工金标准'])
rules=[
 ['回答与任务完成','ANSWER','回答质量','明确错答、不准确或回答质量差','只说考试低分不推断错答；赞扬准确不标问题'],
 ['回答与任务完成','EXPLAIN','解释与步骤','缺步骤、解释难懂、解释不匹配','方程呈现请求保留边界标记'],
 ['回答与任务完成','UNDERSTAND','理解与任务完成','任务无法完成、错读题目、重复回答','不能推断内部记忆机制；语言支持保留细节'],
 ['收费与权益','PAY','门槛与额度','收费异议、次数或能量限制','付费一词本身不等于问题；能量术语不明标待复核'],
 ['收费与权益','BILLING','扣费争议与退款','误购、自动扣费、退款诉求','仅记录用户陈述，不验证欺诈'],
 ['收费与权益','ENTITLEMENT','已购权益','旧会员失效、已购不能跨设备等','付款后报错不自动推断权益失效'],
 ['运行体验','TECH','运行与访问','打不开、报错、不返回答案等','不返回答案可能原因多样，保留不确定'],
 ['运行体验','SPEED','响应速度','明确响应慢、等待过久','解释播放太快及此前找答案耗时不算延迟'],
 ['界面与广告','ADS','广告体验','广告多、造成使用阻碍','没有广告为赞扬'],
 ['界面与广告','UI','界面易用性','界面操作、设置或展示困难','资源不足不自动当成额度'],
 ['入门求助','ONBOARD','入门与激活','不会使用、激活码求助','求助不等于负面故障'],
 ['未覆盖候选','NEW_PERMISSIONS','权限异议','对访问权限表达异议','仅一例且含义较弱，未升格正式主类'],
 ['未覆盖候选','NEW_SUPPORT','客服缺失','找不到客服或帮助入口','仅一例，保留候选，不并入新用户不会使用'],
]
payload={'headers':headers,'rows':rows,'rules':rules,'summary':json.loads((r/'expanded_summary.json').read_text(encoding='utf8'))}
(r/'workbook_data.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf8')
print('Prepared 270 review rows and 13 rule rows')
