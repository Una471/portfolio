"""
MOLAO LEGAL ASSOCIATES - MATTER AND CLIENT DATA GENERATOR
Generates 800 legal matters across 5 practice areas, 2018-2025.
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
print("MOLAO LEGAL ASSOCIATES - GENERATING DATA")
print("=" * 60)

N_MATTERS  = 800
N_CLIENTS  = 120

PRACTICE_AREAS = [
    "Commercial Law",
    "Litigation",
    "Property & Conveyancing",
    "Employment Law",
    "Mining & Resources",
    "Regulatory & Compliance",
]

PARTNERS = [
    "Partner_Molao",       # Commercial Law lead
    "Partner_Setlhabi",    # Litigation lead
    "Partner_Gaobuse",     # Property lead
    "Partner_Mmolawa",     # Employment lead
    "Partner_Thapelo",     # Mining & Resources lead
]

PARTNER_AREA = {
    "Partner_Molao":    "Commercial Law",
    "Partner_Setlhabi": "Litigation",
    "Partner_Gaobuse":  "Property & Conveyancing",
    "Partner_Mmolawa":  "Employment Law",
    "Partner_Thapelo":  "Mining & Resources",
}

ASSOCIATES = [f"Associate_{i:02d}" for i in range(1, 21)]

CLIENT_TYPES = ["Large Corporate", "Government / Parastatal", "Financial Institution",
                "Mining Company", "High-Net-Worth Individual", "SME"]

OFFICES = ["Gaborone", "Francistown", "Maun"]

MATTER_STATUS = ["Completed", "Active", "On Hold"]

START = datetime(2018, 1, 1)
END   = datetime(2025, 3, 31)

# Practice area fee rates (P per hour)
HOURLY_RATES = {
    "Commercial Law":          3200,
    "Litigation":              2800,
    "Property & Conveyancing": 1800,
    "Employment Law":          2200,
    "Mining & Resources":      3800,
    "Regulatory & Compliance": 2600,
}

# Expected hours per matter
MATTER_HOURS_AVG = {
    "Commercial Law":          85,
    "Litigation":             140,
    "Property & Conveyancing": 28,
    "Employment Law":          55,
    "Mining & Resources":     200,
    "Regulatory & Compliance": 65,
}

# Recording rate (% of actual hours recorded) - law firm under-recording problem
RECORDING_RATE = {
    "Partner_Molao":    0.88,
    "Partner_Setlhabi": 0.82,
    "Partner_Gaobuse":  0.91,
    "Partner_Mmolawa":  0.78,
    "Partner_Thapelo":  0.85,
}

# Partner workload (matters per year)
PARTNER_LOAD = {
    "Partner_Molao":    38,
    "Partner_Setlhabi": 45,
    "Partner_Gaobuse":  62,
    "Partner_Mmolawa":  30,
    "Partner_Thapelo":  22,
}

# Assign clients
clients = []
for cid in range(1, N_CLIENTS + 1):
    ctype = random.choices(
        CLIENT_TYPES,
        weights=[25, 22, 18, 12, 13, 10])[0]
    first_year = random.randint(2018, 2022)
    is_top10 = cid <= 10

    clients.append({
        "client_id":    f"CLT-{cid:03d}",
        "client_type":  ctype,
        "first_year":   first_year,
        "is_top10":     is_top10,
        "office":       random.choices(OFFICES, weights=[65, 25, 10])[0],
    })

clients_df = pd.DataFrame(clients)

# Generate matters
print(f"\n  Generating {N_MATTERS} matters...")

matters = []
for mid in range(1, N_MATTERS + 1):
    area    = random.choices(
        PRACTICE_AREAS,
        weights=[22, 20, 18, 15, 12, 13])[0]

    # Assign partner by area mostly
    partner_area_match = [p for p, a in PARTNER_AREA.items() if a == area]
    if partner_area_match and random.random() < 0.75:
        partner = partner_area_match[0]
    else:
        partner = random.choice(PARTNERS)

    associate = random.choice(ASSOCIATES)

    client_idx = random.choices(
        range(N_CLIENTS),
        weights=[5 if i < 10 else 1 for i in range(N_CLIENTS)])[0]
    client = clients[client_idx]

    days_off = random.randint(0, (END - START).days - 60)
    open_date = START + timedelta(days=days_off)

    avg_hrs = MATTER_HOURS_AVG[area]
    actual_hours = max(5, np.random.normal(avg_hrs, avg_hrs * 0.35))

    rec_rate = RECORDING_RATE[partner] * random.uniform(0.80, 1.10)
    rec_rate = max(0.55, min(1.0, rec_rate))
    recorded_hours = actual_hours * rec_rate

    rate = HOURLY_RATES[area]
    potential_fees = actual_hours * rate
    billed_fees    = recorded_hours * rate
    leakage        = potential_fees - billed_fees

    # Matter duration
    base_days = {
        "Commercial Law": 90, "Litigation": 240,
        "Property & Conveyancing": 45, "Employment Law": 80,
        "Mining & Resources": 300, "Regulatory & Compliance": 120,
    }[area]

    overloaded = PARTNER_LOAD[partner] > 50
    delay_factor = 1.3 if overloaded else 1.0
    duration = max(14, int(np.random.normal(base_days, base_days * 0.4) * delay_factor))

    close_date = open_date + timedelta(days=duration)
    if close_date > END:
        status = "Active"
        close_date = None
    else:
        status = random.choices(
            ["Completed", "Active", "On Hold"],
            weights=[80, 15, 5])[0]

    # Disbursements (court fees, travel etc)
    disbursements = round(billed_fees * random.uniform(0.05, 0.18), 0)

    # Payment behaviour
    paid_pct = random.choices(
        [1.0, 0.75, 0.5, 0.0],
        weights=[65, 20, 10, 5])[0]
    outstanding = round(billed_fees * (1 - paid_pct), 0)

    # Satisfaction (1-5, only for completed matters)
    satisfaction = None
    if status == "Completed" and random.random() < 0.60:
        base_sat = 3.8
        if rec_rate < 0.75: base_sat -= 0.3
        if overloaded:      base_sat -= 0.4
        satisfaction = round(max(1, min(5, np.random.normal(base_sat, 0.7))), 1)

    matters.append({
        "matter_id":        f"MLA-{mid:04d}",
        "practice_area":    area,
        "partner":          partner,
        "associate":        associate,
        "client_id":        client["client_id"],
        "client_type":      client["client_type"],
        "office":           client["office"],
        "open_date":        open_date.strftime("%Y-%m-%d"),
        "close_date":       close_date.strftime("%Y-%m-%d") if close_date else None,
        "status":           status,
        "duration_days":    duration if close_date else (END - open_date).days,
        "actual_hours":     round(actual_hours, 1),
        "recorded_hours":   round(recorded_hours, 1),
        "recording_rate":   round(rec_rate, 3),
        "hourly_rate":      rate,
        "potential_fees_bwp":round(potential_fees, 0),
        "billed_fees_bwp":  round(billed_fees, 0),
        "disbursements_bwp":disbursements,
        "outstanding_bwp":  outstanding,
        "leakage_bwp":      round(leakage, 0),
        "satisfaction":     satisfaction,
        "year":             open_date.year,
    })

df = pd.DataFrame(matters)
df.to_csv("matter_data.csv", index=False)

print(f"\n  Total matters          : {len(df):,}")
print(f"  Completed              : {(df['status']=='Completed').sum():,}")
print(f"  Active                 : {(df['status']=='Active').sum():,}")
print(f"  Total potential fees   : P{df['potential_fees_bwp'].sum():,.0f}")
print(f"  Total billed fees      : P{df['billed_fees_bwp'].sum():,.0f}")
print(f"  Total leakage          : P{df['leakage_bwp'].sum():,.0f}")
print(f"  Leakage %              : {df['leakage_bwp'].sum()/df['potential_fees_bwp'].sum()*100:.1f}%")
print(f"  Avg recording rate     : {df['recording_rate'].mean()*100:.1f}%")
print(f"  Total outstanding      : P{df['outstanding_bwp'].sum():,.0f}")
print(f"\n  Saved: matter_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 60)
