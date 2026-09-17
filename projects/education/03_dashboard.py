"""
GABORONE TECHNICAL COLLEGE — STUDENT SUCCESS DASHBOARD
Simple report for school heads, administrators, and management.
Run: streamlit run 03_dashboard.py --server.port 8501
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Gaborone Technical | Dashboard", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f5f6fa;color:#1a1a2e;}
.topbar{background:linear-gradient(135deg,#2c3e50,#34495e);color:white;padding:1.4rem 2rem;border-radius:12px;margin-bottom:1.5rem;}
.topbar h1{margin:0;font-size:1.5rem;font-weight:700;color:white !important;}
.topbar p{margin:.3rem 0 0;opacity:.6;font-size:.85rem;color:white !important;}
.kcard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:5px solid #e0e0e0;margin-bottom:.3rem;}
.kcard.red{border-left-color:#e74c3c;} .kcard.orange{border-left-color:#e67e22;}
.kcard.green{border-left-color:#27ae60;} .kcard.blue{border-left-color:#3182ce;}
.kval{font-size:1.9rem;font-weight:700;line-height:1.1;}
.klbl{font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;color:#888;margin-top:.3rem;}
.ksub{font-size:.78rem;color:#666;margin-top:.3rem;}
.ccard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:1rem;}
.ctitle{font-size:.95rem;font-weight:600;color:#1a1a2e;margin-bottom:.2rem;}
.csub{font-size:.78rem;color:#888;margin-bottom:.7rem;}
.ar{background:#fff5f5;border:1px solid #fed7d7;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ao{background:#fffaf0;border:1px solid #fbd38d;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ag{background:#f0fff4;border:1px solid#9ae6b4;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}

/* Sidebar styling */
section[data-testid="stSidebar"]{background:#2c3e50!important;}
section[data-testid="stSidebar"] *{color:white!important;}

/* Fix for selectboxes - INPUT FIELD */
.stTextInput input, .stNumberInput input, .stSelectbox select, 
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

/* Fix for selectbox DROPDOWN MENU */
.stSelectbox div[data-baseweb="select"] ul {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
}

/* Fix for selectbox DROPDOWN OPTIONS */
.stSelectbox div[data-baseweb="select"] li {
    color: white !important;
    background-color: #1e293b !important;
}

/* Fix for selectbox DROPDOWN OPTIONS on HOVER */
.stSelectbox div[data-baseweb="select"] li:hover {
    background-color: #3b82f6 !important;
    color: white !important;
}

/* Fix for selectbox SELECTED VALUE display */
.stSelectbox div[data-baseweb="select"] span {
    color: white !important;
}

/* Fix for selectbox DROPDOWN ARROW */
.stSelectbox svg {
    fill: white !important;
}

/* Fix for any placeholder text */
.stSelectbox input::placeholder {
    color: #aaa !important;
}

/* Hide Streamlit branding */
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    return pd.read_csv("student_data_scored.csv")

df = load()

with st.sidebar:
    st.markdown("### 🎓 Gaborone Technical College")
    st.markdown("Student Success Dashboard")
    st.markdown("---")
    page = st.radio("Go to", [
        "📊  Enrollment Overview",
        "⚠️  At-Risk Students",
        "🎯  Graduation & Retention",
        "📈  Enrollment Growth",
        "📍  Campus Performance",
    ])
    st.markdown("---")
    programs = ["All Programs"] + sorted(df["program"].unique().tolist())
    sel_p    = st.selectbox("Filter: Program", programs)
    campuses = ["All Campuses"] + sorted(df["campus"].unique().tolist())
    sel_c    = st.selectbox("Filter: Campus", campuses)
    st.markdown("---")
    st.caption("Data: 2023 – 2025")

dff = df.copy()
if sel_p != "All Programs": dff = dff[dff["program"] == sel_p]
if sel_c != "All Campuses": dff = dff[dff["campus"] == sel_c]

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def wchart(fig, h=340):
    fig.update_layout(plot_bgcolor="white",paper_bgcolor="white",font_color="#1a1a2e",
                      height=h,margin=dict(t=15,b=20,l=10,r=10))
    return fig

# ════════════════════════════════════════════════════════════════
# PAGE 1 — ENROLLMENT OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "📊  Enrollment Overview":
    st.markdown('<div class="topbar"><h1>🎓 Enrollment Overview</h1><p>Gaborone Technical College &nbsp;·&nbsp; 2023 – 2025</p></div>', unsafe_allow_html=True)

    active = (dff["status"]=="Active").sum()
    grads  = (dff["status"]=="Graduated").sum()
    drops  = (dff["status"]=="Dropped Out").sum()
    avg_att= dff["attendance_rate_pct"].mean()
    avg_gr = dff["grade_average_pct"].mean()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kcard("blue",   f"{len(dff):,}",      "Total Students",       "2023–2025"), unsafe_allow_html=True)
    c2.markdown(kcard("green",  f"{active:,}",        "Currently Active",     f"{active/len(dff)*100:.0f}% of total"), unsafe_allow_html=True)
    c3.markdown(kcard("green",  f"{grads:,}",         "Graduated",            f"{grads/len(dff)*100:.0f}% of total"), unsafe_allow_html=True)
    c4.markdown(kcard("red",    f"{drops:,}",         "Dropped Out",          f"{drops/len(dff)*100:.0f}% of total"), unsafe_allow_html=True)
    c5.markdown(kcard("orange", f"{avg_att:.0f}%",    "Avg Attendance Rate",  "All students"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 What This Report Shows")
    f1,f2,f3 = st.columns(3)
    with f1: st.markdown('<div class="ar"><b>🔴 Dropout Rate Is Too High</b><br><br>Almost 40% of students who enroll do not complete their program. Many of them show warning signs early — low attendance, failing grades, multiple course failures — but no-one intervened.</div>', unsafe_allow_html=True)
    with f2: st.markdown('<div class="ao"><b>🟠 Attendance Drives Success</b><br><br>Students who attend at least 85% of classes have double the graduation rate. Tracking attendance more closely and reaching out to students who drop below 75% could prevent many dropouts.</div>', unsafe_allow_html=True)
    with f3: st.markdown('<div class="ao"><b>🟠 Some Programs Are Struggling</b><br><br>Dropout rates vary significantly by program. Some programs lose 50%+ of enrolled students. Reviewing these programs for common issues (teaching quality, course difficulty, job market alignment) is needed.</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 1: Student Status Breakdown</div><div class="csub">How many students are active, graduated, or dropped out</div>', unsafe_allow_html=True)
        status_c = dff["status"].value_counts().reset_index()
        status_c.columns = ["Status","Count"]
        fig = px.pie(status_c, values="Count", names="Status", hole=0.45,
                     color="Status",
                     color_discrete_map={"Active":"#3182ce","Graduated":"#27ae60",
                                         "Dropped Out":"#e74c3c","On Leave":"#d69e2e"})
        fig.update_traces(textinfo="percent+label", textposition="outside")
        st.plotly_chart(wchart(fig, 360), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 2: Average Grades by Student Status</div><div class="csub">Students who drop out typically have much lower grades — a clear early warning sign</div>', unsafe_allow_html=True)
        grade_comp = dff.groupby("status")["grade_average_pct"].mean().reset_index()
        grade_comp = grade_comp.sort_values("grade_average_pct", ascending=False)
        grade_comp["label"] = grade_comp["grade_average_pct"].apply(lambda x: f"{x:.0f}%")
        fig2 = px.bar(grade_comp, x="status", y="grade_average_pct", color="status",
                      color_discrete_map={"Graduated":"#27ae60","Active":"#3182ce",
                                          "Dropped Out":"#e74c3c","On Leave":"#d69e2e"},
                      text="label", labels={"grade_average_pct":"Average Grade (%)","status":""})
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — AT-RISK STUDENTS
# ════════════════════════════════════════════════════════════════
elif page == "⚠️  At-Risk Students":
    st.markdown('<div class="topbar"><h1>⚠️ At-Risk Students — Early Warning</h1><p>Students who need immediate support to prevent dropout</p></div>', unsafe_allow_html=True)

    active_only = dff[dff["status"]=="Active"]
    if "risk_level" in active_only.columns and not active_only["risk_level"].isna().all():
        rc = active_only["risk_level"].value_counts()
    else:
        rc = pd.Series(dtype=int)

    at_risk_count = (active_only["at_risk"]==1).sum() if "at_risk" in active_only.columns else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}",    "Critical Risk",    "Need urgent help now"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High Risk',0):,}",   "High Risk",        "Meet with them this week"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium Risk',0):,}", "Medium Risk",      "Monitor closely"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low Risk',0):,}",    "On Track",         "Performing well"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📏 What Do the Risk Levels Mean?")
    e1,e2,e3,e4 = st.columns(4)
    with e1: st.markdown('<div class="ar"><b>🔴 CRITICAL</b><br>Attendance below 60% or grade below 40%. Without intervention this week, they will likely drop out this semester.</div>', unsafe_allow_html=True)
    with e2: st.markdown('<div class="ao"><b>🟠 HIGH RISK</b><br>Attendance 60–74% or grade 40–54%. Schedule a meeting with student and parent/guardian to provide support.</div>', unsafe_allow_html=True)
    with e3: st.markdown('<div class="ao"><b>🟡 MEDIUM</b><br>Some warning signs (low attendance or 1–2 failed courses). Keep a closer eye on their progress this semester.</div>', unsafe_allow_html=True)
    with e4: st.markdown('<div class="ag"><b>🟢 LOW RISK</b><br>Attending regularly, passing courses. Continue normal support.</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 3: Risk Level Distribution</div><div class="csub">How active students are spread across the risk categories</div>', unsafe_allow_html=True)
        if len(rc) > 0:
            fig = px.pie(names=rc.index, values=rc.values, hole=0.45,
                         color=rc.index,
                         color_discrete_map={"Critical":"#e74c3c","High Risk":"#e67e22",
                                             "Medium Risk":"#f59e0b","Low Risk":"#27ae60"})
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(wchart(fig, 340), use_container_width=True)
        else:
            st.info("No risk data available for current filter.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 4: Warning Signs — Graduates vs Dropouts</div><div class="csub">Key differences between students who succeed and those who leave</div>', unsafe_allow_html=True)
        compare = pd.DataFrame({
            "Factor":       ["Attendance Rate (%)","Average Grade (%)","Courses Failed","Distance (km)"],
            "Graduates":    [dff[dff["status"]=="Graduated"]["attendance_rate_pct"].mean(),
                             dff[dff["status"]=="Graduated"]["grade_average_pct"].mean(),
                             dff[dff["status"]=="Graduated"]["courses_failed"].mean(),
                             dff[dff["status"]=="Graduated"]["distance_from_campus_km"].mean()],
            "Dropouts":     [dff[dff["status"]=="Dropped Out"]["attendance_rate_pct"].mean(),
                             dff[dff["status"]=="Dropped Out"]["grade_average_pct"].mean(),
                             dff[dff["status"]=="Dropped Out"]["courses_failed"].mean(),
                             dff[dff["status"]=="Dropped Out"]["distance_from_campus_km"].mean()],
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Graduates",x=compare["Factor"],y=compare["Graduates"],marker_color="#27ae60"))
        fig2.add_trace(go.Bar(name="Dropouts", x=compare["Factor"],y=compare["Dropouts"], marker_color="#e74c3c"))
        fig2.update_layout(barmode="group",legend=dict(orientation="h",y=1.1))
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔴 Critical & High Risk Students — Needs Immediate Action")
    urgent = active_only[active_only["risk_level"].isin(["Critical","High Risk"])] if "risk_level" in active_only.columns else pd.DataFrame()
    if len(urgent) > 0:
        urgent = urgent.sort_values("dropout_probability" if "dropout_probability" in urgent.columns else "at_risk", ascending=False)
        show = urgent[["student_id","program","campus","attendance_rate_pct","grade_average_pct",
                       "courses_failed","warnings_issued","risk_level"]].copy()
        show["attendance_rate_pct"] = show["attendance_rate_pct"].apply(lambda x: f"{x:.0f}%")
        show["grade_average_pct"]   = show["grade_average_pct"].apply(lambda x: f"{x:.0f}%")
        show.columns = ["Student ID","Program","Campus","Attendance","Avg Grade","Failed Courses","Warnings","Risk"]
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
        csv = show.to_csv(index=False).encode()
        st.download_button("📥 Export At-Risk List", csv, "at_risk_students.csv", "text/csv")
    else:
        st.success("✅ No students currently in Critical or High Risk category.")

# ════════════════════════════════════════════════════════════════
# PAGE 3 — GRADUATION & RETENTION
# ════════════════════════════════════════════════════════════════
elif page == "🎯  Graduation & Retention":
    st.markdown('<div class="topbar"><h1>🎯 Graduation Rates & Retention</h1><p>How many students complete their programs successfully</p></div>', unsafe_allow_html=True)

    completed = dff[dff["status"].isin(["Graduated","Dropped Out"])]
    grad_rate = (completed["status"]=="Graduated").mean() * 100
    drop_rate = (completed["status"]=="Dropped Out").mean() * 100

    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("green", f"{grad_rate:.0f}%",    "Graduation Rate",     f"Out of students who finished"), unsafe_allow_html=True)
    c2.markdown(kcard("red",   f"{drop_rate:.0f}%",    "Dropout Rate",        "Did not complete program"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",  f"{completed['attendance_rate_pct'].mean():.0f}%","Avg Attendance","All completed students"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 5: Dropout Rate by Program</div><div class="csub">Which programs have the highest student attrition</div>', unsafe_allow_html=True)
        pg = dff.groupby("program").agg(total=("student_id","count"),
                                         dropped=("status",lambda x:(x=="Dropped Out").sum())).reset_index()
        pg["Dropout Rate %"] = (pg["dropped"]/pg["total"]*100).round(1)
        pg = pg.sort_values("Dropout Rate %", ascending=True)
        pg["label"] = pg["Dropout Rate %"].apply(lambda x: f"{x}%")
        fig = px.bar(pg, x="Dropout Rate %", y="program", orientation="h",
                     color="Dropout Rate %", color_continuous_scale=["#c6f6d5","#e74c3c"],
                     text="label", labels={"program":""})
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 6: Attendance vs Graduation Outcome</div><div class="csub">Clear correlation — higher attendance = much higher graduation rates</div>', unsafe_allow_html=True)
        completed["Attendance Band"] = pd.cut(completed["attendance_rate_pct"],
            bins=[0,60,75,85,100], labels=["<60%","60-74%","75-84%","85%+"])
        att_outcome = completed.groupby(["Attendance Band","status"]).size().reset_index(name="Count")
        fig2 = px.bar(att_outcome, x="Attendance Band", y="Count", color="status",
                      barmode="stack",
                      color_discrete_map={"Graduated":"#27ae60","Dropped Out":"#e74c3c"},
                      labels={"Attendance Band":"Attendance Rate"})
        fig2.update_layout(legend=dict(orientation="h",y=1.1))
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Program Performance Summary")
    prog_summary = dff.groupby("program").agg(
        Total=("student_id","count"),
        Graduated=("status",lambda x:(x=="Graduated").sum()),
        Dropped=("status",lambda x:(x=="Dropped Out").sum()),
        Avg_Attendance=("attendance_rate_pct","mean"),
        Avg_Grade=("grade_average_pct","mean")
    ).reset_index()
    prog_summary["Grad Rate %"] = (prog_summary["Graduated"]/prog_summary["Total"]*100).round(1)
    prog_summary["Drop Rate %"] = (prog_summary["Dropped"]/prog_summary["Total"]*100).round(1)
    prog_summary["Avg_Attendance"] = prog_summary["Avg_Attendance"].apply(lambda x: f"{x:.0f}%")
    prog_summary["Avg_Grade"]      = prog_summary["Avg_Grade"].apply(lambda x: f"{x:.0f}%")
    prog_summary.columns = ["Program","Total","Graduated","Dropped","Avg Attendance","Avg Grade","Grad Rate %","Drop Rate %"]
    st.dataframe(prog_summary.reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — ENROLLMENT GROWTH
# ════════════════════════════════════════════════════════════════
elif page == "📈  Enrollment Growth":
    st.markdown('<div class="topbar"><h1>📈 Enrollment Growth & Marketing</h1><p>Which marketing channels bring in the most students</p></div>', unsafe_allow_html=True)

    yr_enr = dff.groupby("year_enrolled").size().reset_index(name="Enrollments")
    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",  f"{yr_enr[yr_enr['year_enrolled']==2023]['Enrollments'].iloc[0] if 2023 in yr_enr['year_enrolled'].values else 0}","2023 Enrollments",""), unsafe_allow_html=True)
    c2.markdown(kcard("blue",  f"{yr_enr[yr_enr['year_enrolled']==2024]['Enrollments'].iloc[0] if 2024 in yr_enr['year_enrolled'].values else 0}","2024 Enrollments",""), unsafe_allow_html=True)
    c3.markdown(kcard("blue",  f"{yr_enr[yr_enr['year_enrolled']==2025]['Enrollments'].iloc[0] if 2025 in yr_enr['year_enrolled'].values else 0}","2025 Enrollments",""), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 7: Enrollment Trend by Year</div><div class="csub">How total enrollments have changed over 3 years</div>', unsafe_allow_html=True)
        fig = px.line(yr_enr, x="year_enrolled", y="Enrollments", markers=True,
                      labels={"year_enrolled":"Year","Enrollments":"New Students"})
        fig.update_traces(line=dict(color="#3182ce",width=3),marker=dict(size=12))
        st.plotly_chart(wchart(fig,320), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 8: Enrollment Source Breakdown</div><div class="csub">Where students heard about the college</div>', unsafe_allow_html=True)
        src = dff["enrollment_source"].value_counts().reset_index()
        src.columns = ["Source","Count"]
        fig2 = px.bar(src, x="Source", y="Count", color="Count",
                      color_continuous_scale=["#c6f6d5","#3182ce"],
                      text="Count", labels={"Source":"Marketing Channel"})
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig2,320), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Chart 9: Marketing Effectiveness — Enrollment vs Dropout by Source")
    st.caption("Not all enrollment sources are equal — some bring students who are much more likely to drop out")
    src_perf = dff.groupby("enrollment_source").agg(
        Enrollments=("student_id","count"),
        Dropped=("status",lambda x:(x=="Dropped Out").sum()),
        Graduated=("status",lambda x:(x=="Graduated").sum())
    ).reset_index()
    src_perf["Dropout Rate %"] = (src_perf["Dropped"]/src_perf["Enrollments"]*100).round(1)
    src_perf = src_perf.sort_values("Enrollments", ascending=False)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Total Enrollments",x=src_perf["enrollment_source"],y=src_perf["Enrollments"],
                          marker_color="#3182ce",yaxis="y",offsetgroup=1))
    fig3.add_trace(go.Scatter(name="Dropout Rate %",x=src_perf["enrollment_source"],y=src_perf["Dropout Rate %"],
                              mode="lines+markers",marker=dict(color="#e74c3c",size=10),
                              line=dict(color="#e74c3c",width=2),yaxis="y2"))
    fig3.update_layout(
        yaxis=dict(title="Total Enrollments",side="left"),
        yaxis2=dict(title="Dropout Rate (%)",overlaying="y",side="right"),
        legend=dict(orientation="h",y=1.1),
        height=360,plot_bgcolor="white",paper_bgcolor="white",font_color="#1a1a2e",
        margin=dict(t=15,b=40,l=10,r=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — CAMPUS PERFORMANCE
# ════════════════════════════════════════════════════════════════
elif page == "📍  Campus Performance":
    st.markdown('<div class="topbar"><h1>📍 Campus Performance Comparison</h1><p>How each campus location is performing</p></div>', unsafe_allow_html=True)

    camp = dff.groupby("campus").agg(
        Students=("student_id","count"),
        Dropout_Rate=("status",lambda x:(x=="Dropped Out").sum()/len(x)*100),
        Avg_Attendance=("attendance_rate_pct","mean"),
        Avg_Grade=("grade_average_pct","mean")
    ).reset_index()
    camp["Dropout_Rate"] = camp["Dropout_Rate"].round(1)

    best  = camp.sort_values("Dropout_Rate").iloc[0]
    worst = camp.sort_values("Dropout_Rate").iloc[-1]

    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",  f"{len(camp)}",        "Total Campuses",       ""), unsafe_allow_html=True)
    c2.markdown(kcard("green", best["campus"],         "Best Performing",      f"{best['Dropout_Rate']}% dropout"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   worst["campus"],        "Needs Most Support",   f"{worst['Dropout_Rate']}% dropout"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 10: Campus Dropout Rates</div><div class="csub">Which campus locations have the highest student attrition</div>', unsafe_allow_html=True)
        camp_s = camp.sort_values("Dropout_Rate", ascending=True)
        camp_s["label"] = camp_s["Dropout_Rate"].apply(lambda x:f"{x}%")
        fig = px.bar(camp_s, x="Dropout_Rate", y="campus", orientation="h",
                     color="Dropout_Rate", color_continuous_scale=["#c6f6d5","#e74c3c"],
                     text="label", labels={"Dropout_Rate":"Dropout Rate %","campus":""})
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">📊 Chart 11: Campus Size vs Performance</div><div class="csub">Scatter plot showing student count vs dropout rate per campus</div>', unsafe_allow_html=True)
        fig2 = px.scatter(camp, x="Students", y="Dropout_Rate", size="Students",
                          color="Dropout_Rate", color_continuous_scale=["#c6f6d5","#e74c3c"],
                          text="campus", labels={"Students":"Total Students","Dropout_Rate":"Dropout Rate (%)"})
        fig2.update_traces(textposition="top center")
        st.plotly_chart(wchart(fig2), use_container_width=True)
        

    st.markdown("---")
    st.markdown("### 📋 Campus Summary Table")
    camp_show = camp.copy()
    camp_show["Avg_Attendance"] = camp_show["Avg_Attendance"].apply(lambda x:f"{x:.0f}%")
    camp_show["Avg_Grade"]      = camp_show["Avg_Grade"].apply(lambda x:f"{x:.0f}%")
    camp_show.columns = ["Campus","Students","Dropout Rate %","Avg Attendance","Avg Grade"]
    st.dataframe(camp_show.reset_index(drop=True), use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#aaa;font-size:.78rem'>Gaborone Technical College · Student Success Dashboard · Prepared by Unaswi Leonard · 2026</div>", unsafe_allow_html=True)
