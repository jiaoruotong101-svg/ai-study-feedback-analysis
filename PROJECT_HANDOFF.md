# 项目交接：AI 学习助手用户反馈分析课程设计

> **2026-10-30最新状态：** 180条已由用户逐条最终判定并写入Excel（AI提供翻译及具体候选选项，未展示冻结模型预测）。178条可计分，2条不确定；固定模型二分类准确率87.64%、F1 88.66%，四类微平均F1 71.35%。未重新训练或调参。结果位于 outputs/human-evaluation-20261030/，含人工评测结果.md、逐条对照.csv、课程报告实验章节初稿.md。人工评测不是完全无提示的独立标注。当前进入报告整合阶段；学校DOC模板正文与提交要求仍待核对，暂无全量问题率或正式优先级排名。下方旧状态仅作历史记录。

> **2026-10-26状态更新：** 已完成新一轮AI辅助标注及CPU问题识别基线。二分类实际训练1,721条、开发347条；类别待定保留，入门求助样本不足暂不训练。模型已在最终测试抽样前冻结。独立人工测试180条Excel已准备，等待用户填写，尚无独立人工测试成绩。最新结果与分工见 [本阶段结果与下一步](outputs/ai-labelled-20261026/本阶段结果与下一步.md)，填写表位于 `outputs/human-test180-20261026/独立人工测试180条.xlsx`。下文为2026-10-16历史快照。

交接日期：2026-10-16。项目根目录：`D:\projects\Study`。本文依据本次会话及交接时实际文件核对整理；本次交接只新增本文，没有修改业务代码。文中的既有实验指标来自保存的结果与验证记录，本次没有重新训练模型或重新转换全量 Excel。

## 1. 下一会话先读：项目定位与状态

当前推荐题目：**《基于公开评论的 AI 学习助手体验问题识别与改进优先级分析》**。早期 Word 中标题可能含“用户评论”“产品改进”等措辞差异，不代表另一个课题。

核心问题：公开评论中有哪些可处理的体验问题、需求和求助？评分能否代替具体反馈识别？如何将评论整理成有证据的产品改进候选事项？先验证数据和标签，再决定是否需要改进算法。

**当前结论：课题值得继续。回答与任务完成、收费与权益、运行体验三个主类获得重复样本支持；完整分类体系尚未证明稳定。下一步重点是人工复核标签和建立轻量基线，尚无证据要求发明新算法。**

| 状态 | 工作 | 说明 |
|---|---|---|
| 已完成 | 选题建议 Word | 初始方案，非最终课程报告 |
| 已完成 | 原始数据下载、质量审计、整理到“数据”目录 | 16 个 Parquet，总计 480,831 条、40 列、22 个应用 |
| 已完成 | 原始数据按应用转换 Excel | 22 张表；全量值校验、原文件哈希校验及 WPS 打开验证有记录 |
| 已完成 | 清洗候选集、六应用研究子集 | 158,371 条候选；六应用 82,004 条 |
| 已完成 | 评分预测探索基线 | TF-IDF + 逻辑回归；不是问题分类模型 |
| 已完成 | 90 条首批与新增 180 条核验 | 累计 270 条，均为助手阅读产生的探索标签，不是人工金标准 |
| 已完成 | 扩大核验报告、明细和 Excel | 270×16 明细读回一致，WPS 重算汇总正确 |
| 进行中 | 课程设计整体研究 | 已到探索性数据与分类可行性验证阶段 |
| 未开始 | 独立人工复核、正式标注一致性评价 | 用户尚未确认全部标签；没有 Kappa 等可靠性结果 |
| 未开始 | 正式具体反馈识别、多标签分类模型与改进对照 | 未训练，未证明改进效果 |
| 未开始 | 经核验的全量问题分布、正式优先级排名、最终报告 | 不能把已有关键词统计当作这些成果 |

先读 `outputs/genai-edsent-audit-20261016/review-expanded/扩大抽样核验结论.md` 和同目录 `扩大核验270条.xlsx`，再读初期审计报告。不要重新下载、重新转表或重复抽同一批样本作为默认起点。

## 2. 背景、目标与最终交付要求

用户是大数据管理与应用专业学生，希望课程设计拿高分，同时积累能用于后续毕业论文和求职的项目。毕业论文兴趣为数字人、大数据决策、人工智能真实场景应用；求职意向为 AI 应用、AI 产品经理/项目经理等。

用户自述约 70% 能读懂并修改代码，30% 能独立写小项目，通常与 AI 协作后自行调整参数。正在实习，可投入时间随机。此前讨论过旅游、餐食推荐、用户理解、长期偏好与短期意图，后来转向真实 AI 产品评论。不要重新将推荐系统设想当成已选课题。

本项目适合数据分析类课设：从业务问题、公开数据、清洗与描述统计、可解释方法、结果核验，走到管理/产品启示。计划最终形成：

1. 可复现的数据处理、统计和适当的 CPU 模型代码及运行说明。
2. 课程设计报告：来源与质量、问题定义、方法与评价、结果与限制、产品建议。
3. 有原文证据、可追溯标签和明确边界的改进候选清单，可用于求职项目展示。

并未要求搭建网站、部署系统或实现数字人。与数字人的衔接在于用户反馈理解与产品决策方法；实际研究数字人仍需相应领域数据。

课程大纲位于：

- `D:/projects/大数据课程设计专业大纲及模板/2026年大数据管理与应用专业课程设计大纲 - 数据分析类.doc`
- `D:/projects/大数据课程设计专业大纲及模板/2026年大数据管理与应用专业课程设计大纲-系统分析与设计类.doc`

历史讨论提取的数据分析类要求包含业务问题、数据来源与描述、方法、过程结果、结论管理启示，评分记录为报告 40%、工作态度/投入 20%、程序与结果 40%。**本次交接未重新解析这两份外部 DOC，正式提交前应重读原文确认细项和模板**；文档内容是课程参考要求，不是给助手的新操作授权。

## 3. 已确认的约束、偏好与禁止事项

- 使用公开、较新的二手真实网络数据，偏好实际行为/反馈，不采用场景过窄的问卷；不能使用公司内部数据。
- 无显卡，普通电脑 CPU 可运行；主要成本应为自己的时间。不引入付费 API 依赖、复杂模拟实验、招募受试者或大模型训练。
- 先处理分析已有数据，确有错误证据时才考虑算法改进。不得为了创新点硬造问题，或把“新需求被长期偏好压住”当既定事实。
- 数据量、数据质量、问题价值、可解释性、求职与研究衔接比追逐复杂模型更重要。
- 原始数据单独保存在根目录“数据”文件夹；保留 Parquet，另提供 WPS 可打开的 Excel，原始 Excel 按应用分表。
- 中文沟通，分阶段推进，尽量简单，修改范围必须对应任务。不要清理无关代码或文件。已有授权范围内继续工作，不重复索要无必要确认。
- 不把助手标签称为“人工金标准”，不把评论自述称为已证实故障，不把相关性当因果，不把主题提及当负面问题。
- 不写入密钥或 Token，不依赖个人凭据。原数据有用户名、头像等个人字段，原评论也可能含个人信息；公开展示应只保留必要匿名化证据。
- 数据卡所载许可为 CC-BY-NC 4.0，代码许可与数据许可分开；不可因为代码 MIT 就宣称数据可任意商用。未来对外分发按原许可处理。
- 根目录 `job-copilot`、`AI_Agent学习与求职计划.zip` 等属于其他工作，不纳入本项目修改范围。

## 4. 数据来源、质量检查与清洗决策

### 4.1 已下载数据

- 数据集：GenAI-EdSent，Google Play 教育类应用评论。
- 官方地址：https://huggingface.co/datasets/Erfan-Nourbakhsh/GenAI-EdSent
- 文件页：https://huggingface.co/datasets/Erfan-Nourbakhsh/GenAI-EdSent/tree/main
- 下载 revision：`32783444ddc6b56cc95996d77d0923d6eb075164`。
- 16 个总表分片，共 **97,776,504 字节**；480,831 行、40 列、22 应用。
- 只下载总表；仓库另有按应用组织的同批数据，不能再合并进去。展示的 961,662 不能当作独立评论规模。
- 实际时间范围 **2013-12-16—2025-08-13**，不代表 2026 年最新产品表现。数据卡时间/规模等宣传与实际文件存在差异，以本地字段和统计为准。
- 实际字段没有现成情感或问题分类金标签。评分是用户评分，不是语义标签。

### 4.2 质量审计结果

证据：`quality.json`、`app_summary.csv`、`数据质量与课题可行性报告.md`。

| 项目 | 结果 |
|---|---:|
| 空/缺失评论正文 | 7 |
| 应用 ID + 评论 ID 重复 | 0 |
| 评分、评论时间缺失 | 0 |
| 2023 年以来评论 | 321,485 |
| 少于 5 个 ASCII 英文字母词 token | 231,672 |
| 规范化相同文本的额外记录 | 162,558 |
| 五星评论 | 335,281 |
| 评论版本缺失 | 98,554 |
| 开发者回复缺失 | 311,641 |

短文本和重复文本大量重叠，不能相加成无效数据率，也不能据此认定刷评。ASCII 词计数不是语言识别。应用规模差异很大，部分应用仅 12、25、55 条。

清洗规则：日期不早于 2023-01-01，至少 5 个 ASCII 字母词，去重应用 ID+评论 ID，再在**同一应用内**对小写、空白规范化文本去重。最终候选 **158,371** 条。早期全局去重得到的 156,454 已被修正，勿再使用。

候选集仍含混合语言、音译、预使用期待和空泛评价，不是最终英语有效反馈集。目前没有自动语言检测流程。

### 4.3 六应用研究范围

| 应用 | 候选条数 |
|---|---:|
| Gauth: AI Study Companion | 49,570 |
| Question.AI - Chatbot&Math AI | 16,100 |
| Answer.AI - Your AI tutor | 6,814 |
| Nerd AI - Tutor & Math Helper | 5,694 |
| StudyX: AI Homework Helper | 2,437 |
| Homework AI - Math & Essay App | 1,389 |
| 合计 | 82,004 |

选择相似的学习/作业助手缩小功能差异；Blackboard、Kahoot 等不直接混入比较，Brainly 暂不作为本轮范围，并非判定其质量差。至少 10 词的敏感性子集仍有 46,123 条。

82,004 条中一二星 10,466、三星 3,017、四五星 68,521。Gauth 占总体约 60.4%，在评分模型测试集约占 74%；合计指标有明显应用构成影响。开发者回复覆盖率应用间也差异很大，不能直接推断回复导致满意度改善。2025 年 8 月不是完整月份，评论量也不是活跃用户量。

## 5. 已完成实验及实际验证结果

### 5.1 原始数据整理与 Excel

原始分片从分析目录移至 `数据/GenAI-EdSent/`，移动前后 16 个 SHA-256 一致。现有 `audit.py` 和 `download.py` 已使用新路径，旧 `outputs/.../raw/` 不再是源数据目录。

`数据/GenAI-EdSent_原始数据_按应用分表.xlsx`：120,258,663 字节，22 工作表，480,831 数据行，每表 40 列；保留所有原始字段和记录。表名按 Excel 长度/非法字符要求处理，完整应用名仍在数据字段中；有表头筛选和首行冻结。

验证记录：`.codex_tmp/parquet_excel/verification.json` 记录每应用全量单元格值一致和原始 Parquet 哈希一致；`wps_readback.json` 记录 WPS 实际打开后的各表数据行数、40 列及正文表头。不是仅检查文件存在。Parquet 为二进制，WPS 文本打开乱码不代表数据损坏。

### 5.2 初始 Word

`outputs/AI学习助手用户反馈分析课设选题建议.docx` 已生成（44,500 字节），最终两页，包含选题理由、数据链接、边界及初步设计。既有 WPS 导出和页面图位于 `.codex_tmp/course_topic_render/final.pdf`、`final-1.png`、`final-2.png`。

这是初始提案，未同步吸收后来的 270 条结论，不应作为最新实证报告；旧 `review.pdf`、`page-*.png` 是中间版本。

### 5.3 已运行的评分预测基线

脚本 `preliminary.py`，结果 `baseline.json`、`test_predictions.parquet`。任务为 **1—2 星 vs 3—5 星**，不等于正负情绪或是否有具体问题。

六应用数据按日期排序后全局规范化文本去重，减少跨期完全相同文本泄漏。2025 年前训练，最多抽 50,000 条，种子 42；2025 年测试 17,808 条。TF-IDF 一二元词组、min_df=3、max_features=40,000、sublinear_tf；逻辑回归 class_weight=balanced、max_iter=500、random_state=42。

| 指标 | 全预测非低分 | TF-IDF + 逻辑回归 |
|---|---:|---:|
| 准确率 | 0.8719 | 0.9161 |
| Macro-F1 | 0.4658 | 0.8360 |
| 低分精确率 | 0 | 0.6276 |
| 低分召回率 | 0 | 0.8483 |
| 低分 F1 | 0 | 0.7215 |
| ROC-AUC | 0.5000 | 0.9385 |

应用先验 AUC=0.5501。未做超参数搜索、独立验证集、跨应用留出或完整近重复检查。没有保存训练好的模型/向量器文件，可用脚本重建。不能将该结果用于宣称问题识别准确率达到 91.6%。

### 5.4 首批 90 条

`review-pilot/`：六应用 × 三评分层 × 每层五条，抽样种子 20261016，洗牌种子 731，编号 R001—R090。正文先核验、后合并评分；正文自带评分描述时无法完全盲审。

43 条有可处理问题/请求/求助，34 正面，7 空泛负面，3 预使用，2 无关，1 模糊。评分层具体反馈为低分 24/30、三星 17/30、高分 2/30。43 包含求助和轻度异议，不是 43 个严重故障。

形成五主类与 11 子类：回答与任务完成（ANSWER、EXPLAIN、UNDERSTAND）；收费与权益（PAY、BILLING、ENTITLEMENT）；运行体验（TECH、SPEED）；界面与广告（ADS、UI）；入门求助（ONBOARD）。允许多标签。R051 已修正为仅 UI，不要恢复原先 PAY+UI 的误判。

`annotate_pilot.py` 保存的是逐条助手判断，不是训练出的分类算法。

### 5.5 新增 180 条与累计 270 条

`review-expanded/`：先冻结 v0.1 分类说明，排除原 90 条及此前展示过的抽查/关键词/错误示例的规范化相同文本（已知唯一文本 249，剩余可抽总体 81,817）。六应用 × 三评分层 × 10 条，分 A/B 各 90 条，每批每层每应用五条；种子 2026101602，洗牌 1702。

E001—E090 为 A，E091—E180 为 B。新增 ID 和规范化正文无重复，与已知文本不重叠。新增覆盖 2023 年 37 条、2024 年 97 条、2025 年 46 条，未按年份等量抽样。

冻结规则 SHA-256：`06c209a0a4b672951d1c02e6244d88cdd45c10b4e7f01e3530392005935730e6`。种子、排除规则和哈希见 `sampling_manifest.json`。

| 项目 | 首批 P | 新增 A | 新增 B |
|---|---:|---:|---:|
| 样本量 | 90 | 90 | 90 |
| 具体问题、请求或求助 | 43 | 40 | 44 |
| 回答与任务完成 | 13 | 14 | 19 |
| 收费与权益 | 21 | 17 | 16 |
| 运行体验 | 6 | 10 | 10 |
| 界面与广告 | 4 | 1 | 5 |
| 入门求助 | 2 | 0 | 1 |
| 现有规则未覆盖的候选类 | 0 | 2 | 0 |

累计 270：具体反馈 127、正面 106、空泛负面 18、预使用 8、无关 6、模糊 5。新增多标签 16，累计 19；类别计数不可相加当评论数。

新增 84 条具体反馈中 82 条完全落入原类别。E016 权限异议、E026 登录失败且无客服，其中 E026 部分被 TECH 覆盖。**82/84=97.6% 是助手标签下规则覆盖率，不是模型准确率。** 客服/权限各一例，尚未升级为正式类别；语言支持等保留细节标记。稀有类不足以证明饱和或训练独立模型。

累计低分具体反馈 67/90，三星 53/90，高分 7/90；新增对应 43/60、36/60、5/60。高分去掉轻度收费异议后新增 4/60、累计 5/90。新增有 22 条语义/归类不确定、10 条需语言复核，两组重叠；都排除后剩 149 条，具体反馈 67，低分 32/45、三星 32/50、高分 3/54。

三星含具体问题的线索反复出现；高评分也存在问题，但不能作为“高分普遍掩盖严重问题”的核心叙事。抽样是按应用和评分层等量，不代表全量比例；高分总体基数很大，不能因为样本命中比例低就忽略。

评分与问题标签应分开。收费可细分额度、续费、旧权益；能力可细分答案、步骤、题型理解、展示。相关评论只能支持候选核查事项，不能证明实际缺陷、收入效果或后台模型原因。重复回答不能据此诊断上下文窗口/记忆/长期偏好权重。

旧六类关键词本用于主题提及，假设用来筛选具体反馈时：新增 84 条命中 51、漏 33；非具体反馈误命中 10、未命中 86。无广告/不花钱等正面语境会误命中，energy/bars 额度术语、没有步骤、kicks me off 等会漏。**这仅是用途错配诊断，不是独立金标准上的算法性能评估。没有修改模型并证实效果提升。**

### 5.6 扩大核验 Excel 验证

`review-expanded/扩大核验270条.xlsx` 有“分批汇总”“核验明细”“分类规则”三表，270 行明细、16 列。保留原文、证据片段、中文核验说明、边界标记、原评论 ID、核验来源。

`workbook_verification.json` 记录全部 270×16 值与 `workbook_data.json` 一致、WPS 实际打开重算保存通过。汇总缓存核验包括：B6:B8=90，C6:C8=43/40/44，D7=2；E12:E14=67/53/7；E18:E23=46/54/26/10/3/2。

最终正确预览是 `preview_summary_final.png`；明细与规则分别为 `preview_detail.png`、`preview_rules.png`。旧 `preview_summary.png` 发生公式渲染错误，`wps_summary_preview.pdf/png` 有打印裁切，均不可作为最终交付预览。

## 6. 关键技术决策与原因

1. 先限定六个相近应用，避免把不同功能产品混在一起给出无意义排名。
2. 保存原始全量 40 列；统计读取必要的 11 个原字段，避免大段应用描述等造成内存浪费。
3. 清洗按应用去文本重；评分实验额外跨应用全局去重，是为减少训练测试完全相同文本泄漏，两种口径不要混淆。
4. 冻结规则后增加不同评论，记录证据和不确定性，检验主要类别是否反复出现；不把扩大样本等同于人工可靠性验证。
5. 可处理反馈包含请求和求助，采用先判断有无具体反馈、再多标签归类的后续任务设计。稀有子类先描述，不急于拆成 11 个模型。
6. 先现成 CPU 方法、再误差分析；没有证据不做新算法。旧星级预测模型不直接承担具体问题识别。
7. 大型 Excel 用 artifact-tool 生成结构、Python 标准库流式写 OOXML 与共享字符串，避免在内存构造约 1,923 万个单元格对象。openpyxl 用于读取检查，不用于全量建表。
8. Excel 公式以 WPS 实际重算缓存和读回为准，预览引擎结果不能代替实际工作簿验证。

## 7. 目录与重要文件

以下路径均相对 `D:\projects\Study`，除非写明绝对路径。

```text
数据/
  README.md                              原始数据位置与移动说明
  dataset_card.md                        来源说明副本
  GenAI-EdSent_原始数据_按应用分表.xlsx      WPS 阅读原始数据
  GenAI-EdSent/
    train-00000-of-00016.parquet ... train-00015-of-00016.parquet
    download_manifest.json              来源、下载及 SHA-256 清单
    dataset_card.md / source_metadata.json
outputs/
  AI学习助手用户反馈分析课设选题建议.docx    初始方案，非最新结果
  genai-edsent-audit-20261016/
    download.py / audit.py / preliminary.py
    requirements-lock.txt
    quality.json / app_summary.csv / selected_apps.csv
    candidate.parquet                   158,371 条清洗候选
    study_subset_82004.parquet           六应用研究数据
    baseline.json / test_predictions.parquet
    monthly.csv / keyword_signals.csv   描述统计/未经核验主题提及
    sample.jsonl                        早期 109 条样本
    issue_examples.json                 30 条定向关键词示例
    baseline_errors.jsonl               20 条探索性模型错误样本
    数据质量与课题可行性报告.md
    dataset_card.md / source_metadata.json / download_manifest.json
    audit_log.txt
    review-pilot/
      sample_pilot.py / annotate_pilot.py
      sample_with_metadata.jsonl / blind_review.jsonl
      reviewed_90.jsonl / 评论核验90条.csv
      问题分类规则.md / 一级分类统计.csv / pilot_summary.json
      首批评论核验结论.md / annotation_log.txt
    review-expanded/
      sample_expanded.py / frozen_codebook_v01.md / sampling_manifest.json
      sample_metadata.jsonl / blind_A.jsonl / blind_B.jsonl
      annotations_A.tsv / annotations_B.tsv
      analyze_expanded.py / analysis_log.txt
      reviewed_new180.jsonl / reviewed_all270.jsonl
      累计270条核验明细.csv / 分批评分层统计.csv / 分批分类统计.csv
      子类稳定性.csv / 旧关键词与核验不一致案例.csv
      expanded_summary.json / 扩大抽样核验结论.md
      prepare_workbook.py / workbook_data.json / 扩大核验270条.xlsx
      workbook_verification.json / summary_cached_values.json
      preview_summary_final.png / preview_detail.png / preview_rules.png
  dataset-screening-20261014/             早期其他数据集探索，不是当前主线
.codex_tmp/
  dataset-env/                            分析 Python 虚拟环境
  build_course_topic.py / course_topic_render/
  parquet_excel/
    build.mjs / fill_verify.py / preview.mjs
    catalog.json / template.xlsx
    verification.json / wps_readback.json
    build_expanded.mjs / render_final_summary.mjs
    node_modules                         指向运行时依赖的 junction
    bulk_sheet*.xml / sharedStrings.xml   大型 Excel 流式处理中间文件
```

注意：`annotations_A.tsv`、`annotations_B.tsv` **实际用竖线 `|` 分隔**，不是制表符；以现有分析脚本的解析方式为准。不要凭扩展名直接读 TSV。

临时目录中包含复现脚本和验证证据，尚未整理成正式工程；不要随意删除。`.inspect.ndjson` 为工作簿内部检查输出。其他学习求职项目不属于本课题。

## 8. 尚未解决的问题、风险和复现缺口

- 270 条全部为 AI 辅助标签，没有独立人工复核。尤其需要复核语言、语义、轻度异议、客服/权限边界。不能报告人工一致性或最终分类准确率。
- 180 条在抽取时未看过，但现在已用于澄清规则，不再适合作为完全独立最终测试集。
- 英语范围与混合语言处理仍待确定；ASCII 词数过滤不够。正式报告必须交代语言限制。
- 等量分层样本不能直接推全量频率、给产品排名；应用、评分、年份差异都要说明分母与权重。
- 原始评论时间截至 2025 年 8 月，不能声称研究当前版本；无对话轨迹、实际学习效果、收入或实验数据。
- 星级标签噪声、近重复文本和应用构成会影响评分基线；尚无跨应用泛化评价。
- 类别多、少数类样本少；不要用微小测试样本宣称复杂多标签模型有效。
- `study_subset_82004.parquet` 是先前单独导出的产物，`audit.py` + `preliminary.py` **不会自动重新生成该文件**。如清洗变化，应显式重新按 `baseline.json` 的六应用名单导出并校验，不要保留误导性的旧行数文件名。
- 大型 Excel 的 `catalog.json` 也是保留的一次性构建输入，当前并非单命令端到端流水线。
- 抽样/分析脚本会覆盖同名输出；人工修订应保存独立列/版本，避免重跑丢失。`sample_expanded.py` 会重写冻结规则副本，改规则后不要不加区分地重跑。
- `download.py` 可能先解析当前 main 再下载，且已存在文件会跳过；不可用它无检查地混合新旧 revision。现有数据足够，无需刷新下载。
- `build_expanded.mjs` 重建后仍需 WPS 重算并保存，最终汇总 E 列宽曾在 WPS 调整为 25；重建应复核列宽。预览工具可再次把通配符 COUNTIFS 算错。
- 初始 Word、审计报告与后期核验的时间和用途不同。最新分类判断以扩大核验报告为准，不要把初期高分问题猜想升格为核心结论。

## 9. 下一步待办（按优先级）

### P0：先建立可信标签

1. 与用户确认对现有结果的理解，开展用户或其他独立人工复核。重点看新增 22 条不确定、10 条语言标记及轻度/新类；保留原助手判断，另存人工确认与理由。
2. 明确研究语言范围和可处理反馈定义；在证据支持下冻结新版本规则，客服/权限暂保持候选，不盲目扩类别。
3. 如果需要程序支持，只补必要的复核字段和验证，不重做已完成下载/转表。

### P1：建立正式轻量基线与评价

4. 另抽独立评估样本，按应用、评分和时间说明设计；与规则开发样本隔离，并处理跨集合重复文本。
5. 建立有无具体反馈的基线，再做主类多标签识别；优先现成 CPU 方法。评级仅作辅助字段，不当语义金标签。
6. 报告每类及每应用精确率、召回率、F1、样本数和误差案例；稀有类先做描述。比较只看低分与语义筛查的覆盖差异，不能直接把当前等量样本比例当总体效果。

### P2：根据错误决定是否改进

7. 仅当独立核验持续出现术语、否定转折、多问题遗漏时，测试相应规则/特征改进，保留验证集和最终留出，做有针对性的对照。
8. 标签识别达到可接受质量后再扩到六应用全量，做按应用、月份的分布和人工抽检，提出证据明确的产品候选事项，不预测未观测收入或因果效果。

### P3：形成正式交付

9. 整理可复现脚本入口，补六应用导出步骤，固定来源、清洗和标签版本。
10. 重读课程大纲和模板，撰写最终报告与匿名化求职展示材料。是否需要额外图表/演示由实际交付需求决定，当前没有系统开发任务。

## 10. 尝试失败或已修正的方案

| 尝试 | 原因/结果 | 已采用办法与后续注意 |
|---|---|---|
| WPS 直接打开 Parquet | 二进制格式显示乱码 | 保留原文件，另转 XLSX；不是数据损坏 |
| pandas 全字段加载分析 | 大量应用描述字段导致内存超过约 7.5GB、耗时明显 | 审计只读 11 个必要原字段；不要恢复全字段分析 |
| 候选集跨应用全局文本去重 | 会不必要地删除不同产品同文评论，口径偏移 | 清洗改为应用内去重，最终 158,371；评分实验另行全局去重防泄漏 |
| 直接用主题关键词代表问题 | 正面否定语境误命中、产品术语漏掉 | 保留为探索提及；正式识别需标签与评价，尚未实现改进模型 |
| 强调高评分隐藏问题作为核心题目 | 扩样中有案例但数量与边界不足以支持强叙事 | 保持广义体验问题主题，三星和高分问题作为子问题 |
| Word 标准渲染脚本依赖 LibreOffice | 本机没有可用 LibreOffice | WPS COM 导 PDF，再用 Poppler 查看最终两页 |
| 初稿 Word 第三页孤立来源与标题边框 | 排版溢出/样式问题 | 去掉标题边框、调整行距/网格，最终两页；旧渲染不再使用 |
| artifact-tool 渲染含通配符 COUNTIFS | 分类汇总错误显示 0 | WPS CalculateFull + Save，读取缓存逐项验证 |
| 最终工作簿再次直接用同引擎预览 | 可能重新错误计算公式 | 只在预览副本用 WPS 缓存替换公式，生成 preview_summary_final.png，不覆写交付 XLSX |
| WPS 汇总打印 PDF/A3 调整 | 打印缩放裁切；PaperSize=8 曾报 0x800A03EC | 放弃该打印预览，以最终 PNG 与 XLSX 为准 |
| 部分 node 工具打印完成但退出码 1 | 退出码与产物情况不一致 | 检查产物、回读结果，不能只看成功消息或只看退出码 |
| Python 默认控制台编码输出多语言 | Windows GBK 编码错误 | 设置 PYTHONIOENCODING=utf-8 |

## 11. 环境、重要命令与运行注意

Windows PowerShell，项目根目录 `D:\projects\Study`。系统 Python 位于 `D:\python\python.exe`（3.13）；分析使用 `.codex_tmp\dataset-env\Scripts\python.exe`，不要误用缺依赖的系统解释器。

依赖锁在 `outputs/genai-edsent-audit-20261016/requirements-lock.txt`：pandas 3.0.6、pyarrow 26.0.0、scikit-learn 1.9.1、numpy 2.5.4、scipy 1.18.1 等。已有环境可用，无须主动升级。

```powershell
Set-Location 'D:\projects\Study'
$env:PYTHONIOENCODING = 'utf-8'
$py = '.\.codex_tmp\dataset-env\Scripts\python.exe'
$analysis = '.\outputs\genai-edsent-audit-20261016'

# 按需执行，会覆盖同名结果；交接后不必全部重跑。
& $py "$analysis\audit.py"
& $py "$analysis\preliminary.py"

# 首批：抽样与保存既有逐条判断，并不是训练分类器。
& $py "$analysis\review-pilot\sample_pilot.py"
& $py "$analysis\review-pilot\annotate_pilot.py"

# 扩样：重抽会覆盖抽样文件；先保护人工修订及冻结版本。
& $py "$analysis\review-expanded\sample_expanded.py"
& $py "$analysis\review-expanded\analyze_expanded.py"
& $py "$analysis\review-expanded\prepare_workbook.py"
```

`audit.py` 依赖根目录为当前工作目录。必要时重建环境（已有环境正常时不要执行）：

```powershell
& 'D:\python\python.exe' -m venv '.codex_tmp\dataset-env'
& '.\.codex_tmp\dataset-env\Scripts\python.exe' -m pip install -r '.\outputs\genai-edsent-audit-20261016\requirements-lock.txt'
```

文档/表格运行时既有路径（后续会话先确认存在）：

- Node：`C:/Users/panyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`
- artifact-tool：上述运行时 `dependencies/node/node_modules/@oai/artifact-tool`。
- 捆绑 Python：`C:/Users/panyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`，含 python-docx、openpyxl 等；不等同于分析虚拟环境。
- Poppler：`C:/Users/panyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe`。
- `.codex_tmp/parquet_excel/node_modules` 为依赖目录 junction；不要当普通业务源码目录搬动。

WPS COM：文字使用 `kwps.Application`，表格使用 `ket.Application`。需要重建核验工作簿时，先运行现有 builder，再用自己新建的 COM 实例重算并保存；不要终止用户已有 WPS 窗口。示意：

```powershell
$bookPath = 'D:\projects\Study\outputs\genai-edsent-audit-20261016\review-expanded\扩大核验270条.xlsx'
$wps = New-Object -ComObject ket.Application
$book = $null
try {
    $wps.Visible = $false
    $wps.DisplayAlerts = $false
    $book = $wps.Workbooks.Open($bookPath)
    $wps.CalculateFull()
    $book.Save()
} finally {
    if ($null -ne $book) { $book.Close($false) }
    $wps.Quit()
}
```

上述示例仅说明重算，不能代替 270×16 明细检查、汇总缓存核验和列宽检查。当前交付 XLSX 已通过验证，无需为了交接再执行。

后续修改 DOCX/XLSX 应先读取当前会话提供的 documents/spreadsheets 技能要求并查可用运行时，不盲用旧插件版本路径。个人技能安装不是本项目任务；若另行涉及，用户要求以 `D:\codex\codex-skill` 为源，先进入 `_inbox` 再使用 managed installer，禁止直接写系统或插件缓存技能。

## 12. 本次交接检查范围

已重新查看根目录、原始分片、数据 Excel 与 Word 的文件状态；读取 `quality.json`、`baseline.json`、最新扩大核验报告、抽样清单、工作簿验证记录、原始 Excel WPS 读回记录及全量值验证结果；核对清洗/评分脚本实际口径、依赖锁与预览文件。

这是对已存在成果和验证证据的交接核实，未重新运行全量哈希/单元格扫描、训练或 Word 渲染。此前有记录的成功验证与本次重新执行的检查已分别说明。下一会话最重要的边界是：**数据与探索材料已准备好；可信人工标签、正式问题分类模型与最终课程成果仍待完成。**

