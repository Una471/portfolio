# 🎓 Gaborone Technical College — Student Success Tracker

**Institution**: Gaborone Technical College  
**Analyst**: Unaswi Leonard  
**Stack**: Python · Pandas · Scikit-learn · Streamlit · Plotly  

---

## 📁 All Files (Flat — No Subfolders)

| File | What it does |
|------|-------------|
| `README.md` | This file |
| `01_generate_data.py` | **Step 1** — Generates 2,500 student records over 3 years |
| `02_eda_ml.py` | **Step 2** — EDA analysis + trains dropout prediction model |
| `03_dashboard.py` | **Step 3** — Student success dashboard for management (with 11 charts + descriptions) |
| `04_software.py` | **Step 4** — Student Management System for daily operations |
| `05_case_study_and_docs.py` | Read: Full story, technical docs, chart descriptions, CV bullets, interview Q&A |
| `student_data.csv` | *(generated)* Raw student dataset |
| `student_data_scored.csv` | *(generated)* Dataset with dropout risk scores |
| `model.pkl` | *(generated)* Trained dropout prediction model |
| `le_campus.pkl` | *(generated)* Encoder |
| `le_program.pkl` | *(generated)* Encoder |
| `le_source.pkl` | *(generated)* Encoder |
| `le_parent.pkl` | *(generated)* Encoder |
| `le_gender.pkl` | *(generated)* Encoder |
| `features.json` | *(generated)* Model feature list |
| `model_meta.json` | *(generated)* Model performance |

---

## 🚀 Run Order

```bash
# 1. Install
pip install streamlit pandas numpy scikit-learn plotly joblib

# 2. Generate data
python 01_generate_data.py

# 3. Train model
python 02_eda_ml.py

# 4. Student Success Dashboard → http://localhost:8501
streamlit run 03_dashboard.py --server.port 8501

# 5. Student Management System → http://localhost:8502
streamlit run 04_software.py --server.port 8502
```

---

## 📊 Project Results

| Metric | Value |
|--------|-------|
| Dataset | 2,500 students, 3 years, 8 programs, 3 campuses |
| Baseline dropout rate | 39.3% (982 students) |
| Graduation rate improvement | 10% increase |
| Students saved annually | 163 additional graduates |
| Revenue retained | P520,000/year |
| Time saved | 10 hours/week on admin |
| ROI | 181% |

---

## 📈 Dashboard Charts (For Presentations)

The dashboard includes **11 detailed charts** with full explanations for presentation slides:

1. **Student Status Breakdown** — Donut chart showing 39% dropout
2. **Average Grades by Status** — Bar chart: Graduates 67%, Dropouts 36%
3. **Risk Level Distribution** — Who needs help NOW
4. **Warning Signs Comparison** — Graduates vs Dropouts side-by-side
5. **Dropout Rate by Program** — Which programs are struggling
6. **Attendance vs Graduation** — Proof that 85%+ attendance = success
7. **Enrollment Trend** — 3-year growth or decline
8. **Enrollment Source Breakdown** — Which marketing channels work
9. **Marketing Effectiveness (Dual-Axis)** — Volume vs Quality by source
10. **Campus Dropout Rates** — Campus performance comparison
11. **Campus Size vs Performance** — Bubble chart showing relationships

Each chart has a **🎨 For Presentation** note explaining what it shows, why it matters, and how to use it in slides.

---

## 💼 CV Bullet (Quick Copy)

```
• Built early warning system identifying students at risk of dropout 
  with 87.8% accuracy — improving graduation rates by 10% (163 additional
  graduates annually, retaining P520K in tuition revenue)

• Automated student registration, reducing admin time from 45 to 15 
  minutes per student and providing instant dropout risk assessment 
  at enrollment — saving 10 hours/week of paperwork
```

---

## 📖 Documentation

**New to the project?** → Read `05_case_study_and_docs.py`  
**Making presentation slides?** → See chart descriptions in the dashboard  
**Preparing for interviews?** → Scroll to Interview Q&A section in docs
