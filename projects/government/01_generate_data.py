"""
BOTSWANA PUBLIC SERVICE - SERVICE REQUEST DATA GENERATOR
Run this first. Generates 5,000 service request records across 9 departments.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os

np.random.seed(42)
random.seed(42)

print("=" * 60)
print("BOTSWANA PUBLIC SERVICE - GENERATING SERVICE DATA")
print("=" * 60)

N_REQUESTS = 5000

DEPARTMENTS = [
    "Health", "Education", "Police", "BURS",
    "Social Welfare", "Immigration", "Land Board", "Works", "Motor Registry"
]

# Service types per department
SERVICE_TYPES = {
    "Health":          ["Medical Certificate", "Specialist Referral", "Patient Query", "Facility Request"],
    "Education":       ["Student Enrollment", "Teacher Posting", "Scholarship Application", "School Admin"],
    "Police":          ["Case Registration", "Clearance Certificate", "Document Request", "Protection Service"],
    "BURS":            ["Tax Registration", "VAT Filing", "Assessment Dispute", "Compliance Certificate"],
    "Social Welfare":  ["Destitute Support", "Old Age Pension", "Orphan Welfare", "Social Grant"],
    "Immigration":     ["Work Permit", "Citizenship Application", "Permanent Residency", "Border Documentation"],
    "Land Board":      ["Land Allocation", "Consent to Transfer", "Land Certificate", "Land Use Approval"],
    "Works":           ["Property Maintenance", "Infrastructure Defect", "Asset Management", "Utility Request"],
    "Motor Registry":  ["Vehicle Licensing", "Driver Licence", "Roadworthy Certificate", "Number Plate"],
}

CHANNELS = ["In-Person", "Digital", "Phone", "Post"]

OFFICERS = {
    "Health":         [f"HLT-{i:03d}" for i in range(1, 12)],
    "Education":      [f"EDU-{i:03d}" for i in range(1, 10)],
    "Police":         [f"POL-{i:03d}" for i in range(1, 15)],
    "BURS":           [f"BRS-{i:03d}" for i in range(1, 13)],
    "Social Welfare": [f"SWL-{i:03d}" for i in range(1, 9)],
    "Immigration":    [f"IMG-{i:03d}" for i in range(1, 8)],
    "Land Board":     [f"LBD-{i:03d}" for i in range(1, 7)],
    "Works":          [f"WRK-{i:03d}" for i in range(1, 10)],
    "Motor Registry": [f"MTR-{i:03d}" for i in range(1, 16)],
}

DISTRICTS = [
    "Gaborone", "Francistown", "Maun", "Serowe",
    "Lobatse", "Kanye", "Molepolole", "Palapye"
]

# SLA targets in days per department
SLA_TARGETS = {
    "Health":          7,
    "Education":      14,
    "Police":          5,
    "BURS":           10,
    "Social Welfare": 21,
    "Immigration":    30,
    "Land Board":     21,
    "Works":          14,
    "Motor Registry":  5,
}

# Dept performance profiles: (avg_resolution_days, std, sla_rate, escalation_rate, satisfaction_base)
DEPT_PROFILE = {
    "Health":          (6.2,  3.0, 0.74, 0.18, 3.5),
    "Education":       (11.5, 4.5, 0.71, 0.16, 3.6),
    "Police":          (4.2,  2.0, 0.78, 0.14, 3.4),
    "BURS":            (8.1,  3.5, 0.76, 0.15, 3.7),
    "Social Welfare":  (18.2, 7.0, 0.65, 0.22, 3.2),
    "Immigration":     (26.5, 9.0, 0.58, 0.28, 3.0),
    "Land Board":      (48.3,18.0, 0.32, 0.42, 2.4),
    "Works":           (12.8, 5.0, 0.69, 0.19, 3.3),
    "Motor Registry":  (2.9,  1.2, 0.92, 0.05, 4.4),
}

# Digital channel advantage (reduces resolution time)
CHANNEL_FACTOR = {
    "Digital":   0.70,
    "Phone":     0.90,
    "In-Person": 1.00,
    "Post":      1.25,
}

# Service type complexity multiplier
COMPLEXITY = {
    # Health
    "Medical Certificate": 0.80, "Specialist Referral": 1.20,
    "Patient Query": 0.70, "Facility Request": 1.10,
    # Education
    "Student Enrollment": 0.90, "Teacher Posting": 1.30,
    "Scholarship Application": 1.40, "School Admin": 0.80,
    # Police
    "Case Registration": 1.10, "Clearance Certificate": 0.85,
    "Document Request": 0.75, "Protection Service": 1.30,
    # BURS
    "Tax Registration": 0.90, "VAT Filing": 1.00,
    "Assessment Dispute": 1.50, "Compliance Certificate": 0.85,
    # Social Welfare
    "Destitute Support": 1.30, "Old Age Pension": 1.10,
    "Orphan Welfare": 1.20, "Social Grant": 1.00,
    # Immigration
    "Work Permit": 1.20, "Citizenship Application": 1.60,
    "Permanent Residency": 1.40, "Border Documentation": 0.90,
    # Land Board
    "Land Allocation": 1.50, "Consent to Transfer": 1.30,
    "Land Certificate": 1.20, "Land Use Approval": 1.60,
    # Works
    "Property Maintenance": 1.00, "Infrastructure Defect": 1.20,
    "Asset Management": 1.10, "Utility Request": 0.90,
    # Motor Registry
    "Vehicle Licensing": 0.90, "Driver Licence": 0.95,
    "Roadworthy Certificate": 1.00, "Number Plate": 0.80,
}

START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2025, 3, 31)

# Distribute requests across departments (weighted)
DEPT_WEIGHTS = {
    "Health": 180, "Education": 140, "Police": 120, "BURS": 110,
    "Social Welfare": 130, "Immigration": 80, "Land Board": 90,
    "Works": 100, "Motor Registry": 150,
}
total_w = sum(DEPT_WEIGHTS.values())
dept_counts = {d: round(N_REQUESTS * w / total_w) for d, w in DEPT_WEIGHTS.items()}

print(f"\n  Generating {N_REQUESTS:,} service request records...")

records = []
pid = 1

for dept, count in dept_counts.items():
    profile = DEPT_PROFILE[dept]
    avg_days, std_days, sla_rate_target, esc_rate, sat_base = profile
    sla_days = SLA_TARGETS[dept]
    officers = OFFICERS[dept]

    for _ in range(count):
        service_type = random.choice(SERVICE_TYPES[dept])
        channel      = random.choices(
            ["In-Person", "Digital", "Phone", "Post"],
            weights=[50, 25, 18, 7]
        )[0]
        officer      = random.choice(officers)
        district     = random.choice(DISTRICTS)

        days_offset  = random.randint(0, (END_DATE - START_DATE).days - 60)
        submit_date  = START_DATE + timedelta(days=days_offset)

        complexity   = COMPLEXITY.get(service_type, 1.0)
        chan_factor   = CHANNEL_FACTOR[channel]

        base_days    = max(1, np.random.normal(avg_days, std_days))
        actual_days  = round(base_days * complexity * chan_factor + random.gauss(0, 1), 1)
        actual_days  = max(1, actual_days)

        within_sla   = actual_days <= sla_days
        resolution_date = submit_date + timedelta(days=int(actual_days))
        if resolution_date > END_DATE:
            resolution_date = None
            status = "Pending"
        else:
            status = "Resolved"

        sla_breach_days = max(0, round(actual_days - sla_days, 1)) if not within_sla else 0

        escalated = False
        if not within_sla:
            esc_prob = min(esc_rate * (1 + sla_breach_days / sla_days), 0.90)
            escalated = random.random() < esc_prob

        # Satisfaction
        if status == "Resolved":
            sat_adj  = 0.5 if within_sla else -0.8
            sat_adj += 0.3 if channel == "Digital" else 0
            sat_adj += -0.5 if escalated else 0
            sat_score = round(max(1.0, min(5.0, sat_base + sat_adj + random.gauss(0, 0.4))), 1)
            if random.random() < 0.25:
                sat_score = None
        else:
            sat_score = None

        records.append({
            "request_id":       f"BPS-{str(pid).zfill(5)}",
            "department":       dept,
            "service_type":     service_type,
            "channel":          channel,
            "district":         district,
            "officer_id":       officer,
            "submit_date":      submit_date.strftime("%Y-%m-%d"),
            "resolution_date":  resolution_date.strftime("%Y-%m-%d") if resolution_date else None,
            "sla_target_days":  sla_days,
            "actual_days":      round(actual_days, 1),
            "within_sla":       int(within_sla),
            "sla_breach_days":  sla_breach_days,
            "escalated":        int(escalated),
            "status":           status,
            "complexity":       round(complexity, 2),
            "citizen_satisfaction": sat_score,
        })
        pid += 1

df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("service_data.csv", index=False)

resolved = df[df["status"] == "Resolved"]
print(f"\n  Total requests         : {len(df):,}")
print(f"  Resolved               : {len(resolved):,}")
print(f"  Pending                : {(df['status']=='Pending').sum():,}")
print(f"  Within SLA             : {resolved['within_sla'].sum():,} ({resolved['within_sla'].mean()*100:.1f}%)")
print(f"  Escalated              : {df['escalated'].sum():,} ({df['escalated'].mean()*100:.1f}%)")
print(f"  Avg resolution days    : {resolved['actual_days'].mean():.1f}")
print(f"  Avg citizen satisfaction: {df['citizen_satisfaction'].dropna().mean():.2f} / 5.0")
print(f"\n  By department:")
for dept in DEPARTMENTS:
    sub = df[df["department"]==dept]
    res = sub[sub["status"]=="Resolved"]
    sla = res["within_sla"].mean()*100 if len(res) else 0
    print(f"    {dept:<20}: {len(sub):>4} requests | SLA: {sla:.0f}%")
print(f"\n  Saved: service_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 60)
