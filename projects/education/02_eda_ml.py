"""
GABORONE TECHNICAL COLLEGE — EDA & EARLY WARNING SYSTEM MODEL
Run this SECOND after 01_generate_data.py
"""

import pandas as pd
import numpy as np
import json, joblib, warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings("ignore")

print("=" * 70)
print("GABORONE TECHNICAL COLLEGE — EDA & MODEL TRAINING")
print("=" * 70)

df = pd.read_csv("student_data.csv")
print(f"\n📂 Loaded {len(df):,} student records")

# ─── PART 1: EDA ──────────────────────────────────────────────────────
print("\n" + "─"*70)
print("PART 1 — EXPLORATORY DATA ANALYSIS")
print("─"*70)

print(f"\n[1] Shape          : {df.shape}")
print(f"[1] Missing values : {df.isnull().sum().sum()}")

print(f"\n[2] ENROLLMENT OVERVIEW:")
print(f"    Total students enrolled  : {len(df):,}")
print(f"    Active students          : {(df['status']=='Active').sum():,}")
print(f"    Graduated                : {(df['status']=='Graduated').sum():,}")
print(f"    Dropped out              : {(df['status']=='Dropped Out').sum():,}")
print(f"    Dropout rate             : {(df['status']=='Dropped Out').sum()/len(df)*100:.1f}%")
print(f"    Average attendance       : {df['attendance_rate_pct'].mean():.1f}%")
print(f"    Average grade            : {df['grade_average_pct'].mean():.1f}%")

print(f"\n[3] AT-RISK STUDENTS (CURRENTLY ACTIVE):")
active = df[df["status"] == "Active"]
at_risk = active[active["at_risk"] == 1]
print(f"    Active students           : {len(active):,}")
print(f"    At-risk (need intervention): {len(at_risk):,}  ({len(at_risk)/len(active)*100:.1f}%)")
print(f"    Avg attendance (at-risk)  : {at_risk['attendance_rate_pct'].mean():.1f}%")
print(f"    Avg grade (at-risk)       : {at_risk['grade_average_pct'].mean():.1f}%")

print(f"\n[4] DROPOUT RATE BY PROGRAM:")
pg = df.groupby("program").agg(
    total=("student_id","count"),
    dropped=("status", lambda x: (x=="Dropped Out").sum()),
    graduated=("status", lambda x: (x=="Graduated").sum())
).reset_index()
pg["dropout_rate"] = (pg["dropped"]/pg["total"]*100).round(1)
pg = pg.sort_values("dropout_rate", ascending=False)
print(pg.to_string(index=False))

print(f"\n[5] ENROLLMENT SOURCE EFFECTIVENESS:")
src = df.groupby("enrollment_source").agg(
    enrollments=("student_id","count"),
    dropped=("status", lambda x: (x=="Dropped Out").sum()),
    graduated=("status", lambda x: (x=="Graduated").sum())
).reset_index()
src["dropout_rate"] = (src["dropped"]/src["enrollments"]*100).round(1)
src["completion_rate"] = (src["graduated"]/src["enrollments"]*100).round(1)
src = src.sort_values("enrollments", ascending=False)
print(src.to_string(index=False))

print(f"\n[6] RISK FACTOR COMPARISON — GRADUATES vs DROPOUTS:")
cols = ["attendance_rate_pct","grade_average_pct","courses_failed",
        "distance_from_campus_km","has_transport","has_financial_aid",
        "working_student","warnings_issued"]
for c in cols:
    grads = df[df["status"]=="Graduated"][c].mean()
    drops = df[df["status"]=="Dropped Out"][c].mean()
    diff  = (drops-grads)/grads*100 if grads != 0 else 0
    arr   = "↑" if diff > 0 else "↓"
    print(f"    {c:<30} Grads: {grads:>8.2f}  |  Dropouts: {drops:>8.2f}  {arr}{abs(diff):.0f}%")

print(f"\n[7] CAMPUS PERFORMANCE:")
camp = df.groupby("campus").agg(
    students=("student_id","count"),
    dropout_rate=("status", lambda x: (x=="Dropped Out").sum()/len(x)*100),
    avg_attendance=("attendance_rate_pct","mean"),
    avg_grade=("grade_average_pct","mean")
).reset_index()
camp["dropout_rate"] = camp["dropout_rate"].round(1)
print(camp.to_string(index=False))

# ─── PART 2: FEATURE ENGINEERING ──────────────────────────────────────
print("\n" + "─"*70)
print("PART 2 — FEATURE ENGINEERING")
print("─"*70)

# Risk flags
df["attendance_low"]  = (df["attendance_rate_pct"] < 75).astype(int)
df["grade_low"]       = (df["grade_average_pct"] < 55).astype(int)
df["failed_multiple"] = (df["courses_failed"] >= 2).astype(int)
df["distance_far"]    = (df["distance_from_campus_km"] > 40).astype(int)
df["age_mature"]      = (df["age"] > 30).astype(int)
df["parent_edu_low"]  = df["parent_education"].isin(["None","Primary"]).astype(int)

# Encode categoricals
le_campus  = LabelEncoder(); df["campus_enc"]  = le_campus.fit_transform(df["campus"])
le_program = LabelEncoder(); df["program_enc"] = le_program.fit_transform(df["program"])
le_source  = LabelEncoder(); df["source_enc"]  = le_source.fit_transform(df["enrollment_source"])
le_parent  = LabelEncoder(); df["parent_enc"]  = le_parent.fit_transform(df["parent_education"])
le_gender  = LabelEncoder(); df["gender_enc"]  = le_gender.fit_transform(df["gender"])

print("  ✅ attendance_low, grade_low, failed_multiple, distance_far, age_mature, parent_edu_low")
print("  ✅ Encoded: campus, program, enrollment_source, parent_education, gender")

# ─── PART 3: MODEL — PREDICT DROPOUT ──────────────────────────────────
print("\n" + "─"*70)
print("PART 3 — EARLY WARNING SYSTEM (DROPOUT PREDICTION)")
print("─"*70)

# Target = will the student drop out?
# Only include students who have a final outcome (exclude "On Leave" and currently "Active")
model_df = df[df["status"].isin(["Graduated","Dropped Out"])].copy()
model_df["will_dropout"] = (model_df["status"] == "Dropped Out").astype(int)

FEATURES = [
    "age","distance_from_campus_km","has_transport","has_financial_aid",
    "working_student","attendance_rate_pct","grade_average_pct","courses_failed",
    "warnings_issued","program_length_yrs","year_enrolled",
    "campus_enc","program_enc","source_enc","parent_enc","gender_enc",
    "attendance_low","grade_low","failed_multiple","distance_far",
    "age_mature","parent_edu_low",
]
TARGET = "will_dropout"

X, y = model_df[FEATURES], model_df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

print(f"\n  Train: {len(X_train):,}  |  Test: {len(X_test):,}")
print(f"  Dropout rate: {y.mean()*100:.1f}%")

print("\n  Training Gradient Boosting...")
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.08,
                                  max_depth=4, random_state=42)
gb.fit(X_train, y_train)
gb_pred  = gb.predict(X_test)
gb_proba = gb.predict_proba(X_test)[:,1]
gb_auc   = roc_auc_score(y_test, gb_proba)

print("  Training Random Forest...")
rf = RandomForestClassifier(n_estimators=200, max_depth=10,
                             class_weight="balanced", random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred  = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:,1]
rf_auc   = roc_auc_score(y_test, rf_proba)

# Pick best
if gb_auc >= rf_auc:
    best,best_pred,best_proba,best_auc,best_name = gb,gb_pred,gb_proba,gb_auc,"GradientBoosting"
else:
    best,best_pred,best_proba,best_auc,best_name = rf,rf_pred,rf_proba,rf_auc,"RandomForest"

print(f"\n  GB  AUC : {gb_auc:.4f}")
print(f"  RF  AUC : {rf_auc:.4f}")
print(f"  Winner  : {best_name}")
print(f"\n{classification_report(y_test, best_pred, target_names=['Will Graduate','Will Dropout'])}")

cm = confusion_matrix(y_test, best_pred)
tn,fp,fn,tp = cm.ravel()
print(f"  Early Warning System caught {tp/(tp+fn)*100:.1f}% of dropouts before they left")
print(f"  False alarm rate: {fp/(fp+tn)*100:.2f}%")

# Feature importance
fi = pd.DataFrame({"feature":FEATURES,"importance":best.feature_importances_})
fi = fi.sort_values("importance", ascending=False)
print(f"\n  TOP 10 PREDICTORS OF DROPOUT:")
for _,r in fi.head(10).iterrows():
    bar = "█" * int(r["importance"]*200)
    print(f"  {r['feature']:<30} {bar}  {r['importance']:.4f}")

# ─── PART 4: SCORE ALL CURRENT STUDENTS ───────────────────────────────
print("\n" + "─"*70)
print("PART 4 — SCORING ALL ACTIVE STUDENTS")
print("─"*70)

active = df[df["status"] == "Active"].copy()
active["dropout_probability"] = best.predict_proba(active[FEATURES])[:,1]
active["risk_level"] = pd.cut(active["dropout_probability"],
    bins=[0,0.30,0.55,0.75,1.0],
    labels=["Low Risk","Medium Risk","High Risk","Critical"])

rc = active["risk_level"].value_counts()
print(f"\n  🔴 Critical    : {rc.get('Critical',0):>5,}  (needs urgent intervention)")
print(f"  🟠 High Risk   : {rc.get('High Risk',0):>5,}  (schedule meeting this week)")
print(f"  🟡 Medium Risk : {rc.get('Medium Risk',0):>5,}  (monitor closely)")
print(f"  🟢 Low Risk    : {rc.get('Low Risk',0):>5,}  (on track)")

# ─── PART 5: SAVE ─────────────────────────────────────────────────────
print("\n" + "─"*70)
print("PART 5 — SAVING")
print("─"*70)

joblib.dump(best,      "model.pkl")
joblib.dump(le_campus, "le_campus.pkl")
joblib.dump(le_program,"le_program.pkl")
joblib.dump(le_source, "le_source.pkl")
joblib.dump(le_parent, "le_parent.pkl")
joblib.dump(le_gender, "le_gender.pkl")
with open("features.json","w") as f: json.dump(FEATURES, f)

meta = {"model":best_name,"auc":round(best_auc,4),
        "sensitivity":round(tp/(tp+fn),4),"trained":str(pd.Timestamp.now().date())}
with open("model_meta.json","w") as f: json.dump(meta, f, indent=2)

# Save scored data for dashboard
df.to_csv("student_data_scored.csv", index=False)

print("  ✅ model.pkl  |  encoders  |  features.json  |  model_meta.json")
print("  ✅ student_data_scored.csv (all 2,500 students with risk scores)")
print("\nNext:")
print("  streamlit run 03_dashboard.py --server.port 8501")
print("  streamlit run 04_software.py  --server.port 8502")
print("=" * 70)
