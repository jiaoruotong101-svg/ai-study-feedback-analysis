---
license: cc-by-nc-4.0
task_categories:
- text-classification
- text-generation
language:
- en
tags:
- sentiment-analysis
- education
- generative-ai
- app-reviews
dataset_info:
  features:
  - name: app_name
    dtype: string
  - name: source_file
    dtype: string
  - name: review_reviewId
    dtype: string
  - name: review_userName
    dtype: string
  - name: review_userImage
    dtype: string
  - name: review_content
    dtype: string
  - name: review_score
    dtype: int64
  - name: review_thumbsUpCount
    dtype: int64
  - name: review_reviewCreatedVersion
    dtype: string
  - name: review_at
    dtype: string
  - name: review_replyContent
    dtype: string
  - name: review_repliedAt
    dtype: string
  - name: review_appVersion
    dtype: string
  - name: app_info_json
    dtype: string
  - name: app_title
    dtype: string
  - name: app_summary
    dtype: string
  - name: app_description
    dtype: string
  - name: app_descriptionHTML
    dtype: string
  - name: app_genre
    dtype: string
  - name: app_genre_id
    dtype: string
  - name: app_developer
    dtype: string
  - name: app_developer_email
    dtype: string
  - name: app_installs
    dtype: string
  - name: app_minInstalls
    dtype: int64
  - name: app_realInstalls
    dtype: int64
  - name: app_score
    dtype: float64
  - name: app_ratings
    dtype: int64
  - name: app_reviews_count
    dtype: int64
  - name: app_price
    dtype: int64
  - name: app_free
    dtype: bool
  - name: app_offersIAP
    dtype: bool
  - name: app_inAppProductPrice
    dtype: string
  - name: app_appId
    dtype: string
  - name: app_url
    dtype: string
  - name: app_icon
    dtype: string
  - name: app_headerImage
    dtype: string
  - name: app_released
    dtype: string
  - name: app_lastUpdatedOn
    dtype: string
  - name: app_updated_ts
    dtype: int64
  - name: app_version
    dtype: string
  splits:
  - name: train
    num_bytes: 7755072015
    num_examples: 480831
  - name: app_AI_Quiz_Generator
    num_bytes: 1758004
    num_examples: 109
  - name: app_Edu_AI_AI_Homework_Helper
    num_bytes: 403211
    num_examples: 25
  - name: app_Help_AI_Your_Homework_With_AI
    num_bytes: 30127996
    num_examples: 1868
  - name: app_Answer_AI_Your_AI_tutor
    num_bytes: 263748994
    num_examples: 16353
  - name: app_Quiz_AI_AI_Homework_Helper
    num_bytes: 4306303
    num_examples: 267
  - name: app_Teacher_AI_Language_Practice
    num_bytes: 887066
    num_examples: 55
  - name: app_Studocu_AI_Homework_Helper
    num_bytes: 37611609
    num_examples: 2332
  - name: app_Kahoot_Play_Create_Quizzes
    num_bytes: 550739124
    num_examples: 34147
  - name: app_Quizard_AI_Homework_Helper
    num_bytes: 23289521
    num_examples: 1444
  - name: app_Homework_AI_Math_Essay_App
    num_bytes: 68594415
    num_examples: 4253
  - name: app_Course_Hero_AI_Homework_Help
    num_bytes: 68223460
    num_examples: 4230
  - name: app_Academi_AI_Study_Exam_Tutor
    num_bytes: 3935348
    num_examples: 244
  - name: app_Nerd_AI_Tutor_Math_Helper
    num_bytes: 237233777
    num_examples: 14709
  - name: app_Tutor_AI_Learning_Assistants
    num_bytes: 193541
    num_examples: 12
  - name: app_StudyX_AI_Homework_Helper
    num_bytes: 98738539
    num_examples: 6122
  - name: app_School_Hack
    num_bytes: 84755149
    num_examples: 5255
  - name: app_Gauth_AI_Study_Companion
    num_bytes: 1672716669
    num_examples: 103712
  - name: app_Question_AI_Chatbot_Math_AI
    num_bytes: 528610853
    num_examples: 32775
  - name: app_Brainly_AI_Homework_Helper
    num_bytes: 3767612368
    num_examples: 233600
  - name: app_AI_Questions_Generator
    num_bytes: 5548196
    num_examples: 344
  - name: app_Blackboard
    num_bytes: 301376732
    num_examples: 18686
  - name: app_Mathos_AI_Math_Helper_Tutor
    num_bytes: 4661130
    num_examples: 289
  download_size: 196210355
  dataset_size: 15510144020
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: app_AI_Quiz_Generator
    path: data/app_AI_Quiz_Generator-*
  - split: app_Edu_AI_AI_Homework_Helper
    path: data/app_Edu_AI_AI_Homework_Helper-*
  - split: app_Help_AI_Your_Homework_With_AI
    path: data/app_Help_AI_Your_Homework_With_AI-*
  - split: app_Answer_AI_Your_AI_tutor
    path: data/app_Answer_AI_Your_AI_tutor-*
  - split: app_Quiz_AI_AI_Homework_Helper
    path: data/app_Quiz_AI_AI_Homework_Helper-*
  - split: app_Teacher_AI_Language_Practice
    path: data/app_Teacher_AI_Language_Practice-*
  - split: app_Studocu_AI_Homework_Helper
    path: data/app_Studocu_AI_Homework_Helper-*
  - split: app_Kahoot_Play_Create_Quizzes
    path: data/app_Kahoot_Play_Create_Quizzes-*
  - split: app_Quizard_AI_Homework_Helper
    path: data/app_Quizard_AI_Homework_Helper-*
  - split: app_Homework_AI_Math_Essay_App
    path: data/app_Homework_AI_Math_Essay_App-*
  - split: app_Course_Hero_AI_Homework_Help
    path: data/app_Course_Hero_AI_Homework_Help-*
  - split: app_Academi_AI_Study_Exam_Tutor
    path: data/app_Academi_AI_Study_Exam_Tutor-*
  - split: app_Nerd_AI_Tutor_Math_Helper
    path: data/app_Nerd_AI_Tutor_Math_Helper-*
  - split: app_Tutor_AI_Learning_Assistants
    path: data/app_Tutor_AI_Learning_Assistants-*
  - split: app_StudyX_AI_Homework_Helper
    path: data/app_StudyX_AI_Homework_Helper-*
  - split: app_School_Hack
    path: data/app_School_Hack-*
  - split: app_Gauth_AI_Study_Companion
    path: data/app_Gauth_AI_Study_Companion-*
  - split: app_Question_AI_Chatbot_Math_AI
    path: data/app_Question_AI_Chatbot_Math_AI-*
  - split: app_Brainly_AI_Homework_Helper
    path: data/app_Brainly_AI_Homework_Helper-*
  - split: app_AI_Questions_Generator
    path: data/app_AI_Questions_Generator-*
  - split: app_Blackboard
    path: data/app_Blackboard-*
  - split: app_Mathos_AI_Math_Helper_Tutor
    path: data/app_Mathos_AI_Math_Helper_Tutor-*
---

---
<div align="center">

<img src="https://github.com/erfan-nourbakhsh/GenAI-EdSent/raw/main/Figures/logo.png" alt="GenAI-EdSent Logo" width="350"/>

# 🎓 GenAI-EdSent: Sentiment-Driven Evaluation of AI Educational Apps

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/erfan-nourbakhsh/GenAI-EdSent/blob/main/LICENSE)
[![Paper](https://img.shields.io/badge/Paper-arXiv-red.svg)](https://huggingface.co/papers/2512.11934)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Dataset-yellow.svg)](https://huggingface.co/datasets/Erfan-Nourbakhsh/GenAI-EdSent)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/erfan-nourbakhsh/GenAI-EdSent)

*Unveiling User Perceptions in the Generative AI Era Through Large-Scale Sentiment Analysis*

</div>

---


### 📄 Associated Paper

**Title:** *Unveiling User Perceptions in the Generative AI Era: A Sentiment-Driven Evaluation of AI Educational Apps' Role in Digital Transformation of E-Teaching*

**Authors:** Adeleh Mazaheriyan (Islamic Azad University) & Erfan Nourbakhsh (University of Isfahan)

**Abstract:** This study performs a sentiment-driven evaluation of user reviews from 22 top AI ed-apps on the Google Play Store to assess efficacy, challenges, and pedagogical implications. Our pipeline leverages **RoBERTa** for binary sentiment classification, **GPT-4o** for key point extraction, and **GPT-5** for synthesizing top positive/negative themes. Results reveal predominantly positive sentiments, with homework apps leading (e.g., Edu AI: 95.9% positive) while specialized LMS/language apps lag due to stability issues.

---

## 📊 Research at a Glance

<div align="center">

| 📱 Apps Analyzed | 💬 Reviews Processed | 🤖 AI Models Used | 📚 Categories |
|:----------------:|:-------------------:|:----------------:|:-------------:|
| **22** | **481,000+** | **3** (RoBERTa, GPT-4o, GPT-5) | **7** |

</div>


#### 1️⃣ **App Selection & Categorization**
-   Selected **22 prominent AI education apps** based on ratings, downloads, and GenAI integration
-   Categorized into **7 functional types** with overlaps for multifunctional designs:
    -   📝 AI Quiz & Question Generators
    -   🎒 All-in-One Study Companions
    -   ✏️ Homework Helpers
    -   🔢 Math-Focused Solvers & Specialized Tools
    -   📄 Document/Content Tools
    -   🏫 Learning Management Systems (LMS)
    -   🌐 Language Learning Apps

#### 2️⃣ **Data Collection**
-   **Web scraping** from Google Play Store using Python
-   Collected app metadata + verbatim user reviews (up to November 2025)
-   Dataset: **Tens of thousands to millions** of reviews per app

## 📊 Dataset

The full dataset containing **481,000+ app reviews** from 22 AI educational apps is publicly available on Hugging Face:

**🔗 [GenAI-EdSent Dataset on Hugging Face](https://huggingface.co/datasets/Erfan-Nourbakhsh/GenAI-EdSent)**

The dataset includes:
-   **App Information**: Metadata for all 22 applications (ratings, descriptions, install counts)
-   **User Reviews**: Complete review texts with scores, timestamps, and sentiment labels
-   **Sentiment Analysis Results**: Binary classification outputs from RoBERTa
-   **Extracted Insights**: Key positive/negative themes per application

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@article{mazaherian2025unveiling,
  title={Unveiling User Perceptions in the Generative AI Era: A Sentiment-Driven Evaluation of AI Educational Apps' Role in Digital Transformation of e-Teaching},
  author={Mazaherian, Adeleh and Nourbakhsh, Erfan},
  journal={arXiv preprint arXiv:2512.11934},
  year={2025}
}
```

## 📄 License

This dataset is licensed under the CC-BY-NC-4.0 License. The code is licensed under the MIT License.

---

Made with ❤️ for the future of education

</div>