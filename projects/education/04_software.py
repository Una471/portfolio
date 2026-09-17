"""
GABORONE TECHNICAL COLLEGE — STUDENT MANAGEMENT SYSTEM
The software that solves the problem.
Staff use this daily to: register students, track at-risk alerts, log interventions, manage the pipeline.
Run: streamlit run 04_software.py --server.port 8502
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib, json
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Gaborone Technical | Student System", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ===== GLOBAL BASE ===== */
html, body {
    font-family: 'Inter', sans-serif;
    background: #0f172a;
    color: #e2e8f0;
}

/* Remove aggressive streamlit override */
[class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ===== PAGE WRAPPER ===== */
.page-section {
    background: #0f172a;
    padding: 0.5rem 0;
}

/* ===== TOP BAR ===== */
.topbar {
    background: linear-gradient(135deg,#1e3a5f,#0f172a);
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.2rem;
    border: 1px solid #1e3a5f;
}

.topbar h1 {
    color: #ffffff;
    margin: 0;
}

.topbar p {
    color: #cbd5e1;
    opacity: 0.85;
}

/* ===== FIX INLINE DARK TEXT BUG ===== */
.dark-text-fix {
    color: #e2e8f0 !important;
}

/* ===== INPUTS (ISOLATED CLEAN) ===== */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
}

/* Placeholders */
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94a3b8 !important;
    font-style: italic;
}

/* Labels */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label {
    color: #cbd5e1 !important;
}

/* ===== SIDEBAR CLEAN ===== */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ===== MARKDOWN RESET ===== */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #ffffff !important;
}

.stMarkdown p,
.stMarkdown li,
.stMarkdown span {
    color: #cbd5e1 !important;
}

/* ===== REMOVE BLACK INLINE COLORS ===== */
div[style*="color:#161717"] {
    color: #e2e8f0 !important;
}

/* ===== BUTTONS ===== */
.stButton>button,
.stDownloadButton>button {
    background: #3b82f6;
    color: #ffffff !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover,
.stDownloadButton>button:hover {
    background: #2563eb;
}

/* ===== DATAFRAME ===== */
div[data-testid="stDataFrame"] th {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

div[data-testid="stDataFrame"] td {
    background-color: #0f172a !important;
    color: #cbd5e1 !important;
}

/* ===== ADDITIONAL FIXES FOR TEXT VISIBILITY ===== */

/* Fix for all section headings */
.stMarkdown h3 {
    color: #ffffff !important;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

/* Fix for action plan boxes */
div[style*="background:#450a0a"],
div[style*="background:#431407"],
div[style*="background:#422006"] {
    color: #ffffff !important;
}

div[style*="background:#450a0a"] *,
div[style*="background:#431407"] *,
div[style*="background:#422006"] * {
    color: #ffffff !important;
}

/* Fix for bold text in dark boxes */
div[style*="background:#450a0a"] b,
div[style*="background:#431407"] b,
div[style*="background:#422006"] b {
    color: #ffffff !important;
}

/* Fix for caption text */
.stCaption {
    color: #94a3b8 !important;
}

/* Fix for profile section values */
div[style*="display:flex;justify-content:space-between"] span:last-child {
    color: #ffffff !important;
}

/* Fix for any text with dark inline colors */
div[style*="color:#161717"] {
    color: #ffffff !important;
}

/* Fix for KPI cards text */
.kcard .kval {
    color: #ffffff !important;
}

.kcard .klbl {
    color: #94a3b8 !important;
}

.kcard .ksub {
    color: #64748b !important;
}

/* ===== HIDE STREAMLIT BRANDING ===== */
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m = joblib.load("model.pkl")
    lc = joblib.load("le_campus.pkl")
    lp = joblib.load("le_program.pkl")
    ls = joblib.load("le_source.pkl")
    lpar = joblib.load("le_parent.pkl")
    lg = joblib.load("le_gender.pkl")
    with open("features.json") as f: feat = json.load(f)
    return m, lc, lp, ls, lpar, lg, feat

@st.cache_data
def load_data():
    return pd.read_csv("student_data_scored.csv")

model, le_campus, le_program, le_source, le_parent, le_gender, FEATURES = load_model()
df = load_data()

CAMPUSES = sorted(le_campus.classes_.tolist())
PROGRAMS = sorted(le_program.classes_.tolist())
SOURCES  = sorted(le_source.classes_.tolist())

# Session state
if "registrations" not in st.session_state: st.session_state.registrations = []
if "interventions" not in st.session_state: st.session_state.interventions = []

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def dchart(fig, h=300):
    fig.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",font_color="#161717",height=h,margin=dict(t=15,b=10,l=5,r=5))
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Student Management")
    st.markdown("*Gaborone Technical College*")
    st.markdown("---")
    nav = st.radio("Go to", [
        "📝  Register New Student",
        "⚠️  At-Risk Alert Board",
        "📞  Log Intervention",
        "🔍  Check Student Record",
        "📋  Registration Queue",
    ])
    st.markdown("---")
    active = (df["status"]=="Active").sum()
    at_risk = df[(df["status"]=="Active") & (df["at_risk"]==1)].shape[0]
    pending_reg = len(st.session_state.registrations)
    st.markdown(f"👥 **Active students:** {active}")
    st.markdown(f"🔴 **At-risk:** {at_risk}")
    st.markdown(f"📋 **Pending registrations:** {pending_reg}")

# ════════════════════════════════════════════════════════════════
# PAGE 1 — REGISTER NEW STUDENT
# Automates the registration form + instant dropout risk check
# ════════════════════════════════════════════════════════════════
if nav == "📝  Register New Student":
    st.markdown('<div class="topbar"><h1>📝 New Student Registration</h1><p>Quick registration form with instant dropout risk assessment</p></div>', unsafe_allow_html=True)

    st.markdown("### 👤 Student Information")
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("**Personal Details**")
        full_name = st.text_input("Full Name")
        omang     = st.text_input("Omang / ID Number")
        age       = st.number_input("Age", 16, 65, 20)
        gender    = st.selectbox("Gender", ["Male","Female"])
        phone     = st.text_input("Phone Number")

    with col2:
        st.markdown("**Program & Campus**")
        campus    = st.selectbox("Campus", CAMPUSES)
        program   = st.selectbox("Program", PROGRAMS)
        year_enr  = st.selectbox("Enrollment Year", [2024, 2025, 2026])
        semester  = st.selectbox("Semester", ["Semester 1","Semester 2"])
        source    = st.selectbox("How Did You Hear About Us?", SOURCES)

    with col3:
        st.markdown("**Background & Support**")
        distance  = st.number_input("Distance from Campus (km)", 0.5, 150.0, 10.0, 0.5)
        transport = st.checkbox("Has Own Transport?")
        parent_ed = st.selectbox("Parent/Guardian Education", ["None","Primary","Secondary","Tertiary"])
        fin_aid   = st.checkbox("Applying for Financial Aid?")
        working   = st.checkbox("Working Part-Time?")

    st.markdown("---")

    if st.button("🔍  CHECK REGISTRATION & ASSESS RISK"):
        if not full_name or not omang:
            st.error("Please fill in at least Full Name and Omang.")
        else:
            # Feature engineering
            prog_len = 1 if "Certificate" in program else 2
            attendance_low = 0  # can't know yet
            grade_low      = 0  # can't know yet
            failed_mult    = 0  # can't know yet
            distance_far   = 1 if distance > 40 else 0
            age_mature     = 1 if age > 30 else 0
            parent_low     = 1 if parent_ed in ("None","Primary") else 0

            try:
                campus_enc = le_campus.transform([campus])[0]
                program_enc= le_program.transform([program])[0]
                source_enc = le_source.transform([source])[0]
                parent_enc = le_parent.transform([parent_ed])[0]
                gender_enc = le_gender.transform([gender])[0]
            except:
                campus_enc=program_enc=source_enc=parent_enc=gender_enc=0

            # Predict with limited info (we don't have attendance/grades yet)
            # Use average values for unknown features
            avg_att = 80.0
            avg_grade = 55.0
            courses_fail = 0
            warnings = 0

            row = np.array([[
                age, distance, int(transport), int(fin_aid), int(working),
                avg_att, avg_grade, courses_fail, warnings,
                prog_len, year_enr,
                campus_enc, program_enc, source_enc, parent_enc, gender_enc,
                attendance_low, grade_low, failed_mult, distance_far, age_mature, parent_low,
            ]])

            prob = model.predict_proba(row)[0][1] * 100

            # Risk level
            if prob < 30:
                level = "LOW RISK"
                bg = "#052e16"
                border = "#22c55e"
                icon = "🟢"
                colour = "#86efac"
            elif prob < 55:
                level = "MEDIUM RISK"
                bg = "#422006"
                border = "#f97316"
                icon = "🟡"
                colour = "#fde68a"
            else:
                level = "HIGH RISK"
                bg = "#450a0a"
                border = "#ef4444"
                icon = "🔴"
                colour = "#fca5a5"

            # Result banner
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {border};border-radius:14px;padding:2rem;margin:1rem 0;text-align:center;">
              <div style="font-size:3rem;margin-bottom:.5rem">{icon}</div>
              <div style="font-size:2.5rem;font-weight:800;color:{colour}">{level}</div>
              <div style="color:#94a3b8;margin-top:.5rem">{full_name} &nbsp;·&nbsp; Predicted dropout risk: {prob:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

            # Risk factors identified - FIXED: Changed color from #161717 to #ffffff
            st.markdown("### 🚩 Risk Factors Identified")
            flags = []
            if distance > 40:        flags.append(f"Lives {distance:.0f}km from campus — commute is difficult")
            if not transport:        flags.append("No personal transport — relies on public transport")
            if working:              flags.append("Working part-time — may struggle to balance job and studies")
            if parent_ed in ("None","Primary"): flags.append("Low parent/guardian education — less academic support at home")
            if not fin_aid:          flags.append("Not applying for financial aid — may face financial pressure")
            if age > 30:             flags.append(f"Age {age} — mature students often face work/family competing priorities")

            if flags:
                for f in flags:
                    c = "#ef4444" if level == "HIGH RISK" else "#f97316"
                    # FIXED: Changed color from #161717 to #ffffff
                    st.markdown(f'<div style="background:#1e293b;border-left:4px solid {c};border-radius:8px;padding:.85rem;margin:.4rem 0;color:#ffffff">⚠️ {f}</div>', unsafe_allow_html=True)
            else:
                st.success("✅ No major risk factors identified at enrollment")

            # Recommendation
            st.markdown("### 📋 Enrollment Recommendation")
            if level == "LOW RISK":
                st.markdown("""
                <div class="result-pass">
                <h4 style="color:#86efac;margin-top:0">✅ APPROVE REGISTRATION</h4>
                <p>This student has a good profile for success. Proceed with standard enrollment.</p>
                <p><b>Suggested support:</b> Assign to regular academic advisor, no special monitoring needed.</p>
                </div>
                """, unsafe_allow_html=True)
            elif level == "MEDIUM RISK":
                st.markdown("""
                <div class="result-risk">
                <h4 style="color:#fde68a;margin-top:0">⚠️ APPROVE WITH MONITORING</h4>
                <p>This student has some risk factors. Accept them but provide extra support.</p>
                <p><b>Suggested support:</b></p>
                <ul>
                  <li>Assign to an academic advisor experienced with at-risk students</li>
                  <li>Check in after first month to see how they're coping</li>
                  <li>Flag for early intervention if attendance drops below 80%</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-fail">
                <h4 style="color:#fca5a5;margin-top:0">🔴 APPROVE WITH INTENSIVE SUPPORT</h4>
                <p>This student has significant risk factors. They need proactive support to succeed.</p>
                <p><b>Required support plan:</b></p>
                <ul>
                  <li>Assign to Student Support Services immediately upon enrollment</li>
                  <li>Weekly check-ins for first 8 weeks</li>
                  <li>Connect with counselor if they live far or lack transport — arrange carpooling or accommodation</li>
                  <li>Priority consideration for financial aid or work-study programs</li>
                  <li>If attendance drops below 85% in first month, trigger immediate intervention</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

            # Save registration
            st.markdown("---")
            st.markdown("### 💾 Complete Registration")
            reg_officer = st.text_input("Your Name (Admissions Officer)")
            notes       = st.text_area("Notes (optional)")
            if st.button("💾  Save Registration", key="save_reg"):
                st.session_state.registrations.append({
                    "reg_id":      f"REG-{len(st.session_state.registrations)+1:04d}",
                    "date":        str(date.today()),
                    "student_name":full_name,
                    "omang":       omang,
                    "age":         age,
                    "gender":      gender,
                    "phone":       phone,
                    "campus":      campus,
                    "program":     program,
                    "year":        year_enr,
                    "semester":    semester,
                    "source":      source,
                    "risk_level":  level,
                    "risk_score":  f"{prob:.0f}%",
                    "officer":     reg_officer,
                    "notes":       notes,
                    "status":      "Pending Approval",
                })
                st.success(f"✅ Registration saved! Go to **Registration Queue** to review.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 — AT-RISK ALERT BOARD
# Daily priority list sorted by urgency
# ════════════════════════════════════════════════════════════════
elif nav == "⚠️  At-Risk Alert Board":
    st.markdown('<div class="topbar"><h1>⚠️ At-Risk Student Alert Board</h1><p>Students who need immediate intervention to prevent dropout</p></div>', unsafe_allow_html=True)

    active_students = df[df["status"]=="Active"]
    if "risk_level" in active_students.columns and not active_students["risk_level"].isna().all():
        rc = active_students["risk_level"].value_counts()
    else:
        rc = pd.Series(dtype=int)

    at_risk_total = (active_students["at_risk"]==1).sum() if "at_risk" in active_students.columns else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}",    "Critical Risk",    "Urgent intervention needed"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High Risk',0):,}",   "High Risk",        "Meet with them this week"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium Risk',0):,}", "Medium Risk",      "Monitor closely"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low Risk',0):,}",    "On Track",         "No immediate action"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📏 Action Plan by Risk Level")
    e1,e2,e3 = st.columns(3)
    with e1:
        st.markdown("""
        <div style="background:#450a0a;border:1px solid #ef4444;border-radius:10px;padding:1.2rem">
        <h4 style="color:#fca5a5;margin-top:0">🔴 CRITICAL</h4>
        <p><b>Step 1:</b> Call or meet student TODAY</p>
        <p><b>Step 2:</b> Contact parent/guardian if student is under 21</p>
        <p><b>Step 3:</b> Refer to counselor for support plan</p>
        <p><b>Step 4:</b> Log all contact in system</p>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div style="background:#431407;border:1px solid #f97316;border-radius:10px;padding:1.2rem">
        <h4 style="color:#fed7aa;margin-top:0">🟠 HIGH RISK</h4>
        <p><b>Step 1:</b> Schedule meeting within 5 days</p>
        <p><b>Step 2:</b> Review attendance and grades with student</p>
        <p><b>Step 3:</b> Offer tutoring or study group support</p>
        <p><b>Step 4:</b> Follow up in 2 weeks</p>
        </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown("""
        <div style="background:#422006;border:1px solid #f59e0b;border-radius:10px;padding:1.2rem">
        <h4 style="color:#fde68a;margin-top:0">🟡 MEDIUM RISK</h4>
        <p><b>Step 1:</b> Send friendly check-in email or SMS</p>
        <p><b>Step 2:</b> Remind them of tutoring hours available</p>
        <p><b>Step 3:</b> Monitor next 4 weeks</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔴 Priority Contact List — Sorted by Urgency")
    st.caption("Work from top to bottom — these students are most at risk right now")

    urgent = active_students[active_students["at_risk"]==1].copy() if "at_risk" in active_students.columns else pd.DataFrame()
    if len(urgent) > 0:
        urgent = urgent.sort_values("dropout_probability" if "dropout_probability" in urgent.columns else "attendance_rate_pct")
        show = urgent[["student_id","program","campus","attendance_rate_pct","grade_average_pct",
                       "courses_failed","warnings_issued"]].copy()
        if "risk_level" in urgent.columns:
            show.insert(7, "risk_level", urgent["risk_level"])
        show["attendance_rate_pct"] = show["attendance_rate_pct"].apply(lambda x: f"{x:.0f}%")
        show["grade_average_pct"]   = show["grade_average_pct"].apply(lambda x: f"{x:.0f}%")
        show.columns = ["Student ID","Program","Campus","Attendance","Avg Grade","Failed Courses","Warnings"] + (["Risk"] if "risk_level" in urgent.columns else [])
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
        csv = show.to_csv(index=False).encode()
        st.download_button("📥 Download At-Risk List", csv, "at_risk_students.csv", "text/csv")
    else:
        st.success("✅ No students currently flagged as at-risk!")

# ════════════════════════════════════════════════════════════════
# PAGE 3 — LOG INTERVENTION
# Track all support actions taken
# ════════════════════════════════════════════════════════════════
elif nav == "📞  Log Intervention":
    st.markdown('<div class="topbar"><h1>📞 Log Student Intervention</h1><p>Record all meetings, calls, and support actions for at-risk students</p></div>', unsafe_allow_html=True)

    st.markdown("### 📝 Intervention Details")
    ic1,ic2 = st.columns(2)

    with ic1:
        student_id    = st.selectbox("Select Student", sorted(df[df["status"]=="Active"]["student_id"].tolist()))
        intervention  = st.selectbox("Type of Intervention", [
            "Phone Call","In-Person Meeting","Email Sent","SMS Sent",
            "Parent/Guardian Meeting","Counselor Referral","Tutoring Arranged",
            "Financial Aid Discussion","Academic Warning Issued","Study Plan Created"
        ])
        staff_name    = st.text_input("Your Name")
        follow_up_date= st.date_input("Follow-Up Date", value=date.today()+timedelta(days=7))

    with ic2:
        outcome       = st.selectbox("Outcome", [
            "Student responded positively","Student agreed to action plan","No response yet",
            "Student declined support","Parent involved and supportive",
            "Referred to counseling","Issue resolved","Situation unchanged"
        ])
        notes         = st.text_area("Notes", height=120)

    if st.button("💾  Save Intervention Log"):
        if staff_name:
            st.session_state.interventions.append({
                "student_id":  student_id,
                "date":        str(date.today()),
                "intervention":intervention,
                "outcome":     outcome,
                "staff":       staff_name,
                "follow_up":   str(follow_up_date),
                "notes":       notes,
            })
            st.success(f"✅ Intervention logged for {student_id}")
        else:
            st.error("Please enter your name.")

    st.markdown("---")
    if st.session_state.interventions:
        st.markdown("### 📋 All Logged Interventions (This Session)")
        st.dataframe(pd.DataFrame(st.session_state.interventions), use_container_width=True)
        csv = pd.DataFrame(st.session_state.interventions).to_csv(index=False).encode()
        st.download_button("📥 Export Intervention Log", csv, "interventions.csv", "text/csv")
    else:
        st.info("No interventions logged yet.")

# ════════════════════════════════════════════════════════════════
# PAGE 4 — CHECK STUDENT RECORD
# Full profile lookup
# ════════════════════════════════════════════════════════════════
elif nav == "🔍  Check Student Record":
    st.markdown('<div class="topbar"><h1>🔍 Student Record Lookup</h1><p>View full academic record and risk profile for any student</p></div>', unsafe_allow_html=True)

    student_id = st.selectbox("Select Student", sorted(df["student_id"].unique()))
    row = df[df["student_id"] == student_id].iloc[0]

    c1,c2,c3,c4 = st.columns(4)
    status_c = "red" if row["status"]=="Dropped Out" else "green" if row["status"]=="Graduated" else "blue"
    c1.markdown(kcard("blue",   row["program"],                "Program",          row["campus"]), unsafe_allow_html=True)
    c2.markdown(kcard(status_c, row["status"],                 "Status",           f"Enrolled {row['year_enrolled']}"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{row['attendance_rate_pct']:.0f}%","Attendance Rate",""), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"{row['grade_average_pct']:.0f}%",  "Grade Average", ""), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("#### 👤 Student Profile")
        prof = [
            ("Age",           row["age"]),
            ("Gender",        row["gender"]),
            ("Campus",        row["campus"]),
            ("Program",       row["program"]),
            ("Year Enrolled", row["year_enrolled"]),
            ("Semester",      row["semester_enrolled"]),
            ("Enrollment Source", row["enrollment_source"]),
            ("Distance (km)", row["distance_from_campus_km"]),
            ("Has Transport", "Yes" if row["has_transport"] else "No"),
            ("Financial Aid", "Yes" if row["has_financial_aid"] else "No"),
        ]
        for label,val in prof:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid #1e293b;">
              <span style="color:#94a3b8">{label}</span>
              <span style="font-weight:600;color:#ffffff">{val}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### ⚡ Academic Performance")
        acad = [
            ("Attendance Rate", f"{row['attendance_rate_pct']:.0f}%"),
            ("Grade Average",   f"{row['grade_average_pct']:.0f}%"),
            ("Courses Failed",  row["courses_failed"]),
            ("Warnings Issued", row["warnings_issued"]),
            ("At-Risk Flag",    "Yes" if row.get("at_risk",0)==1 else "No"),
        ]
        for label,val in acad:
            # Convert to string for processing
            val_str = str(val)
            
            # Determine color based on the label and value
            if label in ["Attendance Rate", "Grade Average"]:
                # Handle percentage values
                num_val = int(val_str.replace("%", ""))
                if num_val < 60:
                    c = "#ef4444"  # Red for low
                elif num_val > 80:
                    c = "#22c55e"  # Green for high
                else:
                    c = "#f59e0b"  # Orange for medium
            elif label in ["Courses Failed", "Warnings Issued"]:
                # Handle numeric counts
                if val > 2:
                    c = "#ef4444"  # Red for many issues
                elif val > 0:
                    c = "#f97316"  # Orange for some issues
                else:
                    c = "#22c55e"  # Green for no issues
            elif label == "At-Risk Flag":
                # Handle yes/no
                c = "#ef4444" if val == "Yes" else "#22c55e"
            else:
                c = "#94a3b8"  # Default gray
            
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid #1e293b;">
              <span style="color:#94a3b8">{label}</span>
              <span style="font-weight:600;color:{c}">{val}</span>
            </div>""", unsafe_allow_html=True)

    # Intervention history for this student
    st.markdown("---")
    st.markdown("### 📞 Intervention History")
    student_int = [i for i in st.session_state.interventions if i["student_id"]==student_id]
    if student_int:
        st.dataframe(pd.DataFrame(student_int), use_container_width=True)
    else:
        st.info(f"No interventions logged for {student_id} yet.")

# ════════════════════════════════════════════════════════════════
# PAGE 5 — REGISTRATION QUEUE
# ════════════════════════════════════════════════════════════════
elif nav == "📋  Registration Queue":
    st.markdown('<div class="topbar"><h1>📋 Registration Queue</h1><p>All new student registrations pending approval</p></div>', unsafe_allow_html=True)

    regs = st.session_state.registrations
    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",   f"{len(regs)}",     "Total Registrations", "Processed today"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{len([r for r in regs if 'Pending' in r['status']])}","Pending Approval",""), unsafe_allow_html=True)
    c3.markdown(kcard("green",  f"{len([r for r in regs if 'Approved' in r['status']])}","Approved",""), unsafe_allow_html=True)

    st.markdown("---")
    if not regs:
        st.info("No registrations logged yet. Use **Register New Student** to add applications.")
    else:
        for i,reg in enumerate(regs):
            risk_c = "#ef4444" if "HIGH" in reg["risk_level"] else "#f97316" if "MEDIUM" in reg["risk_level"] else "#22c55e"
            c_left,c_right = st.columns([5,1])
            with c_left:
                st.markdown(f"""
                <div style="background:#1e293b;border-radius:10px;padding:1rem;margin:.4rem 0;border-left:4px solid {risk_c}">
                  <div style="display:flex;justify-content:space-between">
                    <div><b>{reg['reg_id']}</b> &nbsp;·&nbsp; {reg['student_name']} &nbsp;·&nbsp; {reg['program']}</div>
                    <div style="color:{risk_c};font-weight:700">{reg['risk_level']}</div>
                  </div>
                  <div style="color:#94a3b8;font-size:.82rem;margin-top:.3rem">
                    Campus: {reg['campus']} &nbsp;·&nbsp; Risk: {reg['risk_score']} &nbsp;·&nbsp; Officer: {reg['officer']} &nbsp;·&nbsp; {reg['date']}
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with c_right:
                new_status = st.selectbox("Status",["Pending Approval","Approved","Declined"],
                    index=0 if "Pending" in reg["status"] else 1 if "Approved" in reg["status"] else 2, key=f"reg_s_{i}")
                if st.button("Update",key=f"upd_{i}"):
                    st.session_state.registrations[i]["status"] = new_status; st.rerun()

        csv = pd.DataFrame(regs).to_csv(index=False).encode()
        st.download_button("📥 Export Registration Queue", csv, "registrations.csv", "text/csv")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem'>Gaborone Technical College · Student Management System · Unaswi Leonard · 2026</div>", unsafe_allow_html=True)