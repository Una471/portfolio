"""
GABORONE TECHNICAL COLLEGE — STUDENT DATA GENERATOR
Run this FIRST before anything else.
Generates 3 years of realistic student enrollment, attendance, grades, and outcome data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

np.random.seed(42)
random.seed(42)

print("=" * 70)
print("GABORONE TECHNICAL COLLEGE — GENERATING STUDENT DATA")
print("=" * 70)

# ── CONFIGURATION ─────────────────────────────────────────────────────
N_STUDENTS   = 2500
PROGRAMS     = ["Diploma in IT", "Certificate in Business Admin",
                "Diploma in Engineering", "Certificate in Hospitality",
                "Diploma in Accounting", "Certificate in Construction",
                "Diploma in Health Sciences", "Certificate in Auto Mechanics"]
YEARS        = [2023, 2024, 2025]
SEMESTERS    = ["Semester 1", "Semester 2"]
CAMPUSES     = ["Main Campus - Gaborone", "Block 8 Campus", "Extension Campus - Mogoditshane"]
SOURCES      = ["Walk-In", "Facebook Ad", "Radio Ad", "School Fair", "Referral",
                "Website Form", "Agent", "Open Day"]
STATUS_OPTS  = ["Active", "Graduated", "Dropped Out", "On Leave"]

print(f"\n  Generating {N_STUDENTS:,} student records over 3 years...")

students = []
for sid in range(1, N_STUDENTS + 1):
    # ── STUDENT PROFILE ───────────────────────────────────────────────
    age            = random.randint(18, 45)
    gender         = random.choice(["Male", "Female"])
    campus         = random.choice(CAMPUSES)
    program        = random.choice(PROGRAMS)
    year_enrolled  = random.choice(YEARS)
    semester_enr   = random.choice(SEMESTERS)
    source         = random.choice(SOURCES)

    # Program duration: Certificate = 1 year, Diploma = 2 years
    program_length = 1 if "Certificate" in program else 2
    expected_grad  = year_enrolled + program_length

    # ── SOCIOECONOMIC FACTORS ─────────────────────────────────────────
    distance_km     = round(random.uniform(0.5, 85.0), 1)
    has_transport   = random.choices([1, 0], weights=[70, 30])[0]
    parent_edu      = random.choice(["None", "Primary", "Secondary", "Tertiary"])
    financial_aid   = random.choices([1, 0], weights=[45, 55])[0]
    working_student = random.choices([1, 0], weights=[35, 65])[0]

    # ── ACADEMIC PERFORMANCE (simulated) ──────────────────────────────
    # Base academic ability
    ability_base = random.gauss(65, 15)

    # Risk factors reduce performance
    risk_score = 0
    if distance_km > 50:     risk_score += 8
    if not has_transport:    risk_score += 12
    if working_student:      risk_score += 10
    if parent_edu in ("None","Primary"): risk_score += 7
    if not financial_aid:    risk_score += 6
    if age > 30:             risk_score += 5

    # Attendance rate (%) — affected by risk factors
    attendance_rate = max(40, min(100, 95 - risk_score + random.gauss(0, 5)))
    attendance_rate = round(attendance_rate, 1)

    # Average grade (%) — correlated with attendance and ability
    grade_avg = ability_base - risk_score + (attendance_rate - 80) * 0.4
    grade_avg = max(30, min(95, grade_avg + random.gauss(0, 8)))
    grade_avg = round(grade_avg, 1)

    # Number of courses failed
    fail_risk = max(0, (70 - grade_avg) / 15)
    courses_failed = int(min(5, max(0, random.gauss(fail_risk, 1.2))))

    # Warnings issued
    warnings = 0
    if attendance_rate < 75:  warnings += 1
    if grade_avg < 50:        warnings += 1
    if courses_failed >= 2:   warnings += 1

    # ── OUTCOME ───────────────────────────────────────────────────────
    current_year = 2025
    years_elapsed = current_year - year_enrolled

    # Dropout probability
    dropout_prob = 0.05
    if attendance_rate < 70:  dropout_prob += 0.25
    if grade_avg < 50:        dropout_prob += 0.30
    if warnings >= 2:         dropout_prob += 0.15
    if courses_failed >= 3:   dropout_prob += 0.20
    if distance_km > 60:      dropout_prob += 0.08
    if not has_transport:     dropout_prob += 0.10
    if working_student:       dropout_prob += 0.05

    # Status determination
    if years_elapsed >= program_length:
        if random.random() < dropout_prob:
            status = "Dropped Out"
        else:
            status = "Graduated"
    else:
        if random.random() < dropout_prob * 0.6:  # lower chance mid-program
            status = "Dropped Out"
        elif random.random() < 0.03:
            status = "On Leave"
        else:
            status = "Active"

    # At-risk flag
    at_risk = 1 if (
        (attendance_rate < 75 and status == "Active") or
        (grade_avg < 55 and status == "Active") or
        (warnings >= 2 and status == "Active") or
        (courses_failed >= 2 and status == "Active")
    ) else 0

    students.append({
        "student_id":       f"GTC-{str(sid).zfill(5)}",
        "age":              age,
        "gender":           gender,
        "campus":           campus,
        "program":          program,
        "program_length_yrs": program_length,
        "year_enrolled":    year_enrolled,
        "semester_enrolled": semester_enr,
        "expected_grad_year": expected_grad,
        "enrollment_source": source,
        "distance_from_campus_km": distance_km,
        "has_transport":    has_transport,
        "parent_education": parent_edu,
        "has_financial_aid": financial_aid,
        "working_student":  working_student,
        "attendance_rate_pct": attendance_rate,
        "grade_average_pct": grade_avg,
        "courses_failed":   courses_failed,
        "warnings_issued":  warnings,
        "status":           status,
        "at_risk":          at_risk,
    })

df = pd.DataFrame(students)
df.to_csv("student_data.csv", index=False)

# ── PRINT SUMMARY ─────────────────────────────────────────────────────
print(f"\n  ✅  Total students     : {len(df):,}")
print(f"  ✅  Active             : {(df['status']=='Active').sum():,}  ({(df['status']=='Active').mean()*100:.1f}%)")
print(f"  ✅  Graduated          : {(df['status']=='Graduated').sum():,}  ({(df['status']=='Graduated').mean()*100:.1f}%)")
print(f"  ✅  Dropped Out        : {(df['status']=='Dropped Out').sum():,}  ({(df['status']=='Dropped Out').mean()*100:.1f}%)")
print(f"  ✅  On Leave           : {(df['status']=='On Leave').sum():,}  ({(df['status']=='On Leave').mean()*100:.1f}%)")
print(f"  ✅  At-Risk (active)   : {df[df['status']=='Active']['at_risk'].sum():,}  "
      f"({df[df['status']=='Active']['at_risk'].mean()*100:.1f}% of active)")
print(f"  ✅  Avg attendance     : {df['attendance_rate_pct'].mean():.1f}%")
print(f"  ✅  Avg grade          : {df['grade_average_pct'].mean():.1f}%")
print(f"\n  💾  Saved: student_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 70)
