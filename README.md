# 📄 Smart Hire Analyzer

An **offline AI-powered Resume Screening (ATS) System** built using Python and Streamlit.  
It analyzes resumes, extracts skills, calculates ATS match score, and provides recruiter-style insights.

---

## 🚀 Features

- 📄 Upload Resume (PDF / DOCX)
- 🧠 Extracts skills automatically
- 👤 Extracts candidate name, email, phone
- 💼 Detects experience
- 📊 ATS Match Score using AI (TF-IDF)
- 📈 Visual analytics (Pie chart)
- 💾 Stores candidate data in SQLite database
- 🎨 Modern dark UI with custom styling
- ⚡ Fully offline working system

---

## 🏗️ Project Structure
smart_hire_analyzer/
│
├── app.py
├── requirements.txt
│
├── backend/
│ ├── parser.py
│ ├── matcher.py
│ ├── skills.py
│ └── database.py
│
├── frontend/
│ └── styles.css
│
├── database/
│ └── smart_hire.db
│
└── uploads/


## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎯
- spaCy 🤖
- Scikit-learn 📊
- SQLite 🗄️
- Plotly 📈
- PDFMiner / python-docx 📄

## ⚙️ Installation

### 1️⃣ Clone or Download Project
```bash
cd smart_hire_analyzer
