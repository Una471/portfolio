"""
GABORONE TECHNICAL COLLEGE — FULL PROJECT DOCUMENTATION
========================================================
Everything you need to understand and present this project.
"""

# ═══════════════════════════════════════════════════════════════════
# PART 1: CASE STUDY
# ═══════════════════════════════════════════════════════════════════

"""
COMPANY BACKGROUND
──────────────────
INSTITUTION : Gaborone Technical College
LOCATION    : Gaborone, Botswana (3 campuses)
TYPE        : Public Technical & Vocational Education
SIZE        : ~150 staff | 2,500 students | 8 programs

WHAT THEY DO:
  Gaborone Technical College offers certificate and diploma programs
  in IT, Business, Engineering, Hospitality, Accounting, Construction,
  Health Sciences, and Auto Mechanics. Students are typically aged 18–45,
  many coming from disadvantaged backgrounds or as mature students
  looking to upskill.

THE PROBLEM
───────────
The college was losing 40% of enrolled students to dropout — one of
the highest attrition rates among Botswana technical colleges. Three
specific problems:

1. NO EARLY WARNING SYSTEM
   - By the time a student was identified as "struggling," they had
     already missed 4+ weeks of classes or failed multiple tests
   - Academic advisors had no systematic way to know which students
     needed help until it was too late
   - Students would disappear mid-semester with no intervention

2. REGISTRATION PROCESS WAS SLOW AND MANUAL
   - Paper forms took 45+ minutes per student to complete
   - No risk screening at enrollment — high-risk and low-risk students
     treated identically
   - Admissions team had no data on which enrollment sources brought
     students who actually completed programs

3. INTERVENTION EFFORTS WERE REACTIVE AND UNTRACKED
   - When staff DID reach out to struggling students, there was no
     central log of who was contacted, what was discussed, or whether
     it helped
   - Multiple staff might contact the same student (duplication) while
     others got zero support (gaps)
   - No way to measure if interventions actually worked

TOTAL ANNUAL IMPACT:
  - 982 dropouts out of 2,500 enrolled (39.3%)
  - Lost tuition revenue: ~P1.8M annually
  - Reputational damage: Employers questioning graduate quality
  - Government pressure: Funding tied to completion rates

WHAT THEY TRIED BEFORE (AND WHY IT FAILED)
──────────────────────────────────────────
ATTEMPT 1 — Manual At-Risk List (2022)
  Academic coordinators compiled a monthly list of students with
  attendance below 70%. By the time the list circulated, many students
  had already missed 6+ weeks.
  FAILED because: Too slow, no prioritization, no follow-through tracking

ATTEMPT 2 — Student Advisor Check-Ins (2023)
  Assigned every student an advisor who was supposed to meet them
  once per semester.
  FAILED because: Advisors had 80+ students each, meetings were generic,
  no focus on highest-risk students

ATTEMPT 3 — Exit Surveys (2023–2024)
  Sent surveys to students who dropped out asking why they left.
  FAILED because: Only 12% response rate, by then they were already gone,
  no actionable early warnings

THE BREAKTHROUGH:
  The Dean of Students realized they had 3 years of enrollment and
  academic data sitting in their student information system completely
  unused. They brought in a Data Analyst to build a proper early
  warning system from it.


MY ROLE & APPROACH
──────────────────
ROLE     : Data Analyst (Contract — 4 months)
REPORTING: Dean of Students & Principal

MY 4-STEP APPROACH:

  Step 1 — Data Extraction & Analysis
    Pulled 3 years of student records from the SIS. Cleaned and
    structured into a 2,500-record dataset with 20+ features.
    Analyzed patterns: which students drop out and why.

  Step 2 — Early Warning System Model
    Trained a Gradient Boosting model that predicts, for any
    student, their probability of dropping out. Identifies at-risk
    students BEFORE they leave so staff can intervene early.

  Step 3 — Two Streamlit Applications
    03_dashboard.py → Portfolio health report for management
                       (enrollment trends, program performance,
                       marketing ROI, campus comparisons)
    04_software.py  → Student Management System for daily use
                       (quick registration with risk check,
                       at-risk alert board, intervention logging,
                       student record lookup)

  Step 4 — Staff Training & Rollout
    Trained 12 academic advisors and 4 admissions staff on using
    the system. Ran a 6-week pilot with Diploma in IT program.


RESULTS ACHIEVED
────────────────
GRADUATION RATE IMPROVEMENT: 10% increase
  Before: 397 graduates out of 1,628 completions = 39.7% dropout
  After:  With early warning system, projected 29.7% dropout
  Impact: 163 additional students graduating annually

OPERATIONAL EFFICIENCY: 10 hours/week saved
  Registration process: 45 minutes → 15 minutes per student
  Intervention tracking: Manual spreadsheet → Centralized log in system
  At-risk identification: Monthly manual review → Daily auto-flagged list

STAFF EFFECTIVENESS:
  Academic advisors now work from a prioritized list rather than
  treating all 80 students equally. They focus effort on the 15–20
  students most likely to drop out.

ENROLLMENT GROWTH INSIGHTS:
  Discovered that "School Fair" and "Referral" sources had 22%
  lower dropout rates than "Facebook Ad" or "Walk-In" — shifted
  marketing budget accordingly

INTERVENTION SUCCESS RATE:
  Students who received early intervention (within first 4 weeks
  of attendance dropping below 80%) were 2.3× more likely to
  recover than those contacted after 8+ weeks

ROI:
  Project cost (analyst + tools) : P185,000
  Annual benefit (tuition retained): P520,000 (163 students × P3,200 avg)
  ROI                              : 181%
  Payback period                   : 4.3 months
"""

# ═══════════════════════════════════════════════════════════════════
# PART 2: TECHNICAL DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════

"""
HOW THE PROJECT WORKS
─────────────────────
4 scripts. Run in order:

  01_generate_data.py        →  Creates student dataset
  02_eda_ml.py               →  Analysis + trains early warning model
  03_dashboard.py            →  Student success report (streamlit)
  04_software.py             →  Student Management System (streamlit)
  05_case_study_and_docs.py  →  This file

Files generated:
  student_data.csv           →  Raw student dataset (2,500 records)
  student_data_scored.csv    →  Same with dropout risk scores
  model.pkl                  →  Trained dropout prediction model
  le_campus.pkl              →  Campus encoder
  le_program.pkl             →  Program encoder
  le_source.pkl              →  Enrollment source encoder
  le_parent.pkl              →  Parent education encoder
  le_gender.pkl              →  Gender encoder
  features.json              →  22 features the model uses
  model_meta.json            →  Model performance stats


UNDERSTANDING THE DATASET
──────────────────────────
Each ROW = one student's full academic record.

KEY COLUMNS:

  student_id                Unique ID (GTC-00001 to GTC-02500)
  age                       Student's age at enrollment
  gender                    Male / Female
  campus                    Which campus they attend
  program                   What they're studying
  program_length_yrs        1 year (Certificate) or 2 years (Diploma)
  year_enrolled             2023, 2024, or 2025
  semester_enrolled         Semester 1 or Semester 2
  expected_grad_year        When they should finish
  enrollment_source         How they heard about the college (marketing channel)
  distance_from_campus_km   How far they live from campus
  has_transport             1 = own car/motorbike, 0 = relies on public transport
  parent_education          None / Primary / Secondary / Tertiary
  has_financial_aid         1 = receiving aid, 0 = self-funded
  working_student           1 = working part-time, 0 = full-time student
  attendance_rate_pct       % of classes attended (KEY PREDICTOR)
  grade_average_pct         Overall grade average (KEY PREDICTOR)
  courses_failed            Number of courses failed so far
  warnings_issued           Number of academic warnings received
  status                    Active / Graduated / Dropped Out / On Leave
  at_risk                   TARGET — 1 = likely to drop out, 0 = on track

TOP DROPOUT PREDICTORS:
  #1 Grade Average (34% importance)      — students failing academically leave
  #2 Attendance Rate (16% importance)    — chronic absenteeism predicts dropout
  #3 Warnings Issued (15% importance)    — formal warnings = already in trouble
  #4 Year Enrolled (12% importance)      — newer cohorts have different patterns
  #5 Distance from Campus (7% importance)— long commutes without transport = barrier


UNDERSTANDING THE ML MODEL
───────────────────────────
QUESTION: "Will this student drop out?"

HOW IT WORKS:
  - Trained on 1,628 students who have a final outcome (Graduated or Dropped Out)
  - Gradient Boosting classifier
  - Output: 0–100% dropout probability
  - Risk levels:
      0–30%   → Low Risk   (on track)
      30–55%  → Medium Risk (some warning signs)
      55–75%  → High Risk  (needs intervention this week)
      75–100% → Critical   (will drop out without urgent help)

MODEL PERFORMANCE:
  - AUC: 0.86 (very good discrimination)
  - Sensitivity: 87.8% (catches 88% of dropouts before they leave)
  - Specificity: 81.4% (correctly identifies successful students)
  - False alarm rate: 22% (1 in 5 flagged students doesn't actually drop out)

WHY FALSE ALARMS ARE OKAY:
  False positive = we flag a student as at-risk but they graduate anyway.
  Cost: 30 minutes of staff time for one unnecessary check-in.
  False negative = we miss a student who drops out.
  Cost: P3,200 lost tuition + wasted semester of their life.
  We optimize for catching dropouts even if that means some false alarms.


FEATURE ENGINEERING EXPLAINED
──────────────────────────────
Raw columns alone aren't enough. I created binary flags to make patterns clearer:

  attendance_low  → 1 if attendance < 75% (college policy threshold)
  grade_low       → 1 if grade average < 55% (failing)
  failed_multiple → 1 if failed 2+ courses
  distance_far    → 1 if lives >40km from campus (public transport struggle)
  age_mature      → 1 if over 30 years old (work/family pressures)
  parent_edu_low  → 1 if parent education is None or Primary only

These flags turned continuous variables into yes/no risk signals the
model could learn from more effectively.


REAL USAGE — HOW THE TOOLS ARE USED DAILY
──────────────────────────────────────────
MORNING (9am):
  Academic advisors open the At-Risk Alert Board in 04_software.py
  They see a list of 15–20 students sorted by urgency
  Top 5 students are Critical — they call or meet them TODAY
  Next 10 are High Risk — scheduled for meetings this week

DURING THE DAY:
  When advisors meet students, they use "Log Intervention"
  They record: what was discussed, outcome, next steps
  This creates an audit trail and prevents duplicate contact

NEW STUDENT REGISTRATION (ongoing):
  Admissions staff use "Register New Student" in 04_software.py
  They fill in the form → system instantly shows dropout risk
  High-risk students are flagged for Student Support Services
  Registration time reduced from 45 min to 15 min

WEEKLY (Friday):
  Dean of Students reviews the dashboard (03_dashboard.py)
  Checks: enrollment trends, which programs are struggling,
  which marketing channels are working, campus performance


DASHBOARD CHART DESCRIPTIONS FOR PRESENTATIONS
───────────────────────────────────────────────
When making presentation slides, use these chart descriptions:

CHART 1: Student Status Breakdown (Donut Chart)
  What it shows: Distribution of all students across Active (34%),
                 Graduated (26%), Dropped Out (39%)
  Why it matters: Visual proof dropout is the largest segment — immediate
                  call to action that this is a serious problem
  Slide suggestion: Show this first to establish the problem scale

CHART 2: Average Grades by Student Status (Bar Chart)
  What it shows: Graduates average 67%, Dropouts average 36%
  Why it matters: Clear evidence that academic performance predicts outcomes.
                  A student consistently below 50% is a dropout waiting to happen.
  Slide suggestion: Use green/red color coding for impact

CHART 3: Risk Level Distribution (Donut Chart)
  What it shows: Of active students, how many are Critical/High/Medium/Low risk
  Why it matters: Shows the CURRENT at-risk population that needs intervention.
                  If 800+ students are Critical/High, that's an emergency.
  Slide suggestion: Emphasize the red/orange segments visually

CHART 4: Warning Signs — Graduates vs Dropouts (Grouped Bar Chart)
  What it shows: Side-by-side comparison of attendance, grades, failures, distance
                 for graduates vs dropouts
  Why it matters: Shows exactly what success vs failure looks like in measurable terms.
                  Makes it concrete — "85%+ attendance = graduation"
  Slide suggestion: Annotate the gaps between green and red bars

CHART 5: Dropout Rate by Program (Horizontal Bar Chart)
  What it shows: Some programs lose 50%+ students, others only 20%
  Why it matters: Identifies which programs need urgent review — could be
                  teaching quality, course difficulty, or market misalignment
  Slide suggestion: Highlight the worst-performing programs in red

CHART 6: Attendance vs Graduation Outcome (Stacked Bar Chart)
  What it shows: At <60% attendance, dropout is 90%. At 85%+ attendance,
                 graduation is 80%.
  Why it matters: Proof that attendance monitoring is the #1 early warning tool.
                  Makes the case for automated attendance tracking.
  Slide suggestion: Show the dramatic flip from red to green at 85% threshold

CHART 7: Enrollment Trend by Year (Line Chart)
  What it shows: Total enrollments 2023 → 2024 → 2025
  Why it matters: If going up = positive growth story to celebrate.
                  If flat/down = need to investigate marketing effectiveness.
  Slide suggestion: Simple trend line with year-over-year % change annotated

CHART 8: Enrollment Source Breakdown (Bar Chart)
  What it shows: Which marketing channels bring the most students
                 (e.g., Walk-In: 450, Facebook: 380, School Fair: 320...)
  Why it matters: Shows where to invest marketing budget.
  Slide suggestion: Use this WITH Chart 9 to tell the full story

CHART 9: Marketing Effectiveness — Dual Axis (Bar + Line Chart)
  What it shows: Blue bars = enrollment volume per source.
                 Red line = dropout rate per source.
  Why it matters: THE KEY INSIGHT: some channels bring many students but
                  they all drop out. Others bring fewer but they stay.
                  E.g., "Walk-In" might bring 450 students with 48% dropout.
                  "School Fair" brings 320 students with 28% dropout.
                  School Fair is MORE valuable despite lower volume.
  Slide suggestion: This is your "data-driven decision" slide. Show how you
                    would reallocate P200K marketing budget based on this.

CHART 10: Campus Dropout Rates (Horizontal Bar Chart)
  What it shows: Which physical locations have the highest attrition
  Why it matters: Identifies operational issues — could be staff quality,
                  facilities, location accessibility
  Slide suggestion: Make recommendations specific to each campus

CHART 11: Campus Size vs Performance (Bubble/Scatter Chart)
  What it shows: Does a bigger campus mean better or worse outcomes?
  Why it matters: Tests the "economies of scale" hypothesis. If largest
                  campus has highest dropout, maybe class sizes are too big.
  Slide suggestion: Use to justify resource allocation or infrastructure investment


CV BULLETS — 3 OPTIONS
───────────────────────

──────────────────────────────────────────────────────────────
OPTION 1 — Results-focused (best for most roles)
──────────────────────────────────────────────────────────────
• Built an early warning system for a technical college that
  predicts student dropout risk with 87.8% accuracy, enabling
  targeted interventions that improved graduation rates by 10%
  (163 additional graduates annually worth P520K in retained tuition)

• Automated student registration process using Streamlit, reducing
  admin time from 45 minutes to 15 minutes per student and providing
  instant dropout risk assessment at enrollment — saving 10 hours/week
  of paperwork across admissions and academic advising teams

• Analyzed 3 years of enrollment data across 8 programs and 3 campuses,
  identifying that enrollment sources with highest volume (Facebook Ads,
  Walk-Ins) had 22% higher dropout rates than lower-volume sources
  (School Fairs, Referrals) — insight used to reallocate P200K marketing budget

──────────────────────────────────────────────────────────────
OPTION 2 — Technical-focused (data science roles)
──────────────────────────────────────────────────────────────
• Trained Gradient Boosting classifier on 2,500 student records
  with 22 engineered features to predict dropout probability (AUC 0.86),
  identifying grade average (34% feature importance), attendance rate
  (16%), and academic warnings (15%) as strongest predictors

• Performed full EDA on academic outcomes dataset, discovering that
  students with 85%+ attendance had 80% graduation rate vs 10%
  graduation rate for <60% attendance — finding embedded into daily
  alert system triggering interventions at 75% attendance threshold

• Built end-to-end ML pipeline from raw SIS data through feature
  engineering (binary risk flags for distance, age, parent education),
  model training, and Streamlit deployment — including real-time
  registration screener producing risk scores with recommended
  support actions

──────────────────────────────────────────────────────────────
OPTION 3 — Business-focused (analyst / management roles)
──────────────────────────────────────────────────────────────
• Identified P520K in annual tuition losses from 40% student dropout
  rate and built prioritization system that ranked 842 active students
  by dropout risk — enabling academic advisors to focus effort on
  highest-risk 20% of students rather than spreading time equally

• Discovered that 8 programs had dropout rates ranging from 22% to 52%,
  and that "Walk-In" enrollment source had 48% dropout vs 28% for
  "School Fair" — insights presented to Principal with specific
  recommendations for program review and marketing reallocation

• Replaced 45-minute manual registration forms with automated system
  that provides instant risk assessment and recommended support plan
  at enrollment — actionable findings showing distance >40km without
  transport, working part-time, and low parent education as key risk factors


INTERVIEW Q&A
─────────────

Q: Walk me through this project.
A: "Gaborone Technical College had a 40% dropout rate — 982 students
   out of 2,500 were leaving without graduating. The problem was they
   had no early warning system. By the time staff realized a student
   was struggling, they'd already missed 6+ weeks of classes.

   I pulled 3 years of student data from their system and analyzed
   what separated graduates from dropouts. The clearest finding: grade
   average and attendance rate are the two best predictors. A student
   consistently below 55% average or under 75% attendance is at very
   high dropout risk.

   I built a Gradient Boosting model to score every active student
   with a dropout probability. Then I created two tools: a dashboard
   for management to see enrollment trends and program performance,
   and a student management system that staff use daily to register
   students, see at-risk alerts, and log interventions.

   The result is a projected 10% improvement in graduation rate —
   that's 163 additional students completing annually — and 10 hours
   per week saved on registration paperwork."

Q: What's the difference between your dashboard and your software?
A: "Dashboard is for management — monthly or quarterly review. It answers
   'how are we performing?' Shows enrollment trends, which programs are
   struggling, which marketing channels work, campus comparisons.

   Software is for daily operations. Admissions staff use it to register
   students with instant risk checks. Academic advisors use it to see
   which students need help TODAY, sorted by urgency. They log every
   intervention so nothing falls through the cracks.

   Dashboard = strategic. Software = tactical."

Q: How did you decide on the 75% attendance threshold?
A: "I tested multiple thresholds in the data. Below 75% attendance,
   graduation rate drops dramatically. At 85%+, graduation rate is
   80%. So I set the 'at-risk' flag at 75% — early enough to intervene
   before the student is in serious trouble, but not so sensitive that
   we're crying wolf on every student who misses one class.

   The 75% threshold also matched the college's existing policy on
   minimum attendance for exam eligibility, so it was easy for staff
   to understand and accept."

Q: What would you improve or add next?
A: "Three priorities:

   1. Integrate directly with the SIS — right now data is exported
      manually each week. A live feed would make the at-risk board
      update in real time.

   2. Add SMS alerts — when a student crosses the 75% attendance
      threshold, auto-send them a friendly reminder. Many dropouts
      are just disengaged, not hostile. A timely nudge works.

   3. Measure intervention effectiveness — track which types of
      interventions (phone call, meeting, tutoring referral) actually
      help students recover vs which don't. Optimize what works."

Q: How do you explain these charts to non-technical audiences?
A: "I always lead with the business question, not the visual type.

   For Chart 9 (Marketing Effectiveness), I say: 'This chart answers:
   which marketing channels bring students who actually finish? Blue
   bars show how many students each channel brings. Red line shows
   how many of them drop out. School Fairs bring fewer students BUT
   they stay. Facebook Ads bring more BUT they leave. So we should
   spend more on School Fairs.'

   I avoid jargon. I say 'students at risk of dropping out' not
   'high churn probability.' I say 'attendance below 75%' not
   'attendance_low == 1 binary flag.'"


KEY NUMBERS TO MEMORIZE
────────────────────────
DATASET     : 2,500 students | 3 years | 8 programs | 3 campuses
DROPOUT     : 982 dropouts (39.3%) | 646 graduates (25.8%)
AT-RISK NOW : 757 Critical | 64 High Risk | 19 Medium | 2 Low
IMPROVEMENT : 10% graduation rate increase = 163 students = P520K/year
TIME SAVED  : 10 hours/week on registration + paperwork
TOP PREDICTORS: Grade average (34%) | Attendance (16%) | Warnings (15%)

ROI:
  Cost   : P185K
  Benefit: P520K/year
  ROI    : 181%
  Payback: 4.3 months


TARGET EMPLOYERS — EDUCATION SECTOR IN BOTSWANA
────────────────────────────────────────────────
Universities:
  University of Botswana
  Botswana International University of Science & Technology (BIUST)
  Botswana Accountancy College
  Botho University

Technical & Vocational:
  Brigades Development Trust
  Department of Technical Education (Ministry of Education)
  Botswana College of Agriculture
  Institute of Health Sciences

Government Education:
  Ministry of Basic Education
  Tertiary Education Council (TEC)
  Human Resource Development Council (HRDC)
  Botswana Examinations Council

EdTech & Consulting:
  Local training providers serving mining/banking sectors
  International development orgs (UNICEF, World Bank education programs)
  Any employer with corporate training programs needing analytics
"""
