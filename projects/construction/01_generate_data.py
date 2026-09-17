"""
SETSHABA CONSTRUCTION (PTY) LTD - PROJECT DATA GENERATOR
Run this first. Generates 300 construction project records across 7 years.
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
print("SETSHABA CONSTRUCTION - GENERATING PROJECT DATA")
print("=" * 60)

N_PROJECTS = 300

PROJECT_TYPES = [
    "Road Construction",
    "Residential Building",
    "Commercial Building",
    "Education Infrastructure",
    "Healthcare Facility",
    "Government Office",
]

REGIONS = ["Gaborone", "Francistown", "Palapye", "Maun", "Serowe"]

PROJECT_MANAGERS = [
    "PM_Moeti",
    "PM_Kebonye",
    "PM_Ditiro",
    "PM_Segametsi",
]

DELAY_CAUSES = [
    "Material delivery delays",
    "Subcontractor failure",
    "Weather conditions",
    "Design changes",
    "Cash flow constraints",
    "Labour disputes",
    "Scope creep",
    "Equipment breakdown",
    "None",
]

TENDER_TYPES = ["Government", "Private"]

START_DATE = datetime(2018, 1, 1)
END_DATE   = datetime(2025, 3, 31)

# Base contracted values by project type (BWP)
BASE_CONTRACT = {
    "Road Construction":        (3000000, 25000000),
    "Residential Building":     (1500000, 12000000),
    "Commercial Building":      (2000000, 18000000),
    "Education Infrastructure": (800000,  6000000),
    "Healthcare Facility":      (1200000, 9000000),
    "Government Office":        (2500000, 15000000),
}

# Base planned durations in months
BASE_DURATION = {
    "Road Construction":        (8, 36),
    "Residential Building":     (6, 24),
    "Commercial Building":      (8, 30),
    "Education Infrastructure": (4, 18),
    "Healthcare Facility":      (6, 20),
    "Government Office":        (6, 24),
}

# PM overrun tendencies (some managers are riskier than others)
PM_RISK = {
    "PM_Moeti":     0.20,
    "PM_Kebonye":   0.45,
    "PM_Ditiro":    0.35,
    "PM_Segametsi": 0.55,
}

# PM quality scores tendency
PM_QUALITY = {
    "PM_Moeti":     (78, 95),
    "PM_Kebonye":   (60, 82),
    "PM_Ditiro":    (70, 90),
    "PM_Segametsi": (55, 78),
}

print(f"\n  Generating {N_PROJECTS} project records...")

records = []
for pid in range(1, N_PROJECTS + 1):
    ptype   = random.choice(PROJECT_TYPES)
    region  = random.choice(REGIONS)
    pm      = random.choice(PROJECT_MANAGERS)
    tender  = random.choices(TENDER_TYPES, weights=[70, 30])[0]

    contract_range = BASE_CONTRACT[ptype]
    contracted_budget = round(random.uniform(*contract_range), -3)

    duration_range = BASE_DURATION[ptype]
    planned_duration_months = random.randint(*duration_range)

    days_offset = random.randint(0, (END_DATE - START_DATE).days - 60)
    start_date  = START_DATE + timedelta(days=days_offset)
    planned_end = start_date + timedelta(days=planned_duration_months * 30)

    # Risk score drives overrun probability
    risk_base = PM_RISK[pm]

    type_risk_adj = {
        "Road Construction":        0.15,
        "Residential Building":    -0.05,
        "Commercial Building":      0.05,
        "Education Infrastructure":-0.08,
        "Healthcare Facility":      0.02,
        "Government Office":        0.00,
    }[ptype]

    size_risk = min((contracted_budget / 10000000) * 0.05, 0.15)
    pm_risk_score = risk_base + type_risk_adj + size_risk + random.gauss(0, 0.05)
    pm_risk_score = max(0.05, min(0.85, pm_risk_score))

    will_overrun = random.random() < pm_risk_score

    if will_overrun:
        overrun_pct  = random.uniform(0.05, 0.55)
        actual_cost  = round(contracted_budget * (1 + overrun_pct), -2)
        cost_variance= round(actual_cost - contracted_budget, -2)
    else:
        underrun_pct = random.uniform(0, 0.08)
        actual_cost  = round(contracted_budget * (1 - underrun_pct), -2)
        cost_variance= round(actual_cost - contracted_budget, -2)
        overrun_pct  = 0

    # Labour cost
    labour_pct   = random.uniform(0.28, 0.42)
    labour_cost  = round(actual_cost * labour_pct, -2)

    # Materials
    material_pct = random.uniform(0.30, 0.45)
    material_cost= round(actual_cost * material_pct, -2)

    # Material waste
    waste_factor = random.uniform(0.05, 0.22) if will_overrun else random.uniform(0.02, 0.12)
    material_waste_cost = round(material_cost * waste_factor, -2)
    waste_pct = round(waste_factor * 100, 1)

    equipment_cost    = round(actual_cost * random.uniform(0.10, 0.18), -2)
    subcontractor_cost= round(actual_cost * random.uniform(0.05, 0.15), -2)
    overhead_cost     = round(actual_cost - labour_cost - material_cost - equipment_cost - subcontractor_cost, -2)

    # Delay
    if will_overrun:
        delay_months = random.randint(1, int(planned_duration_months * 0.6) + 1)
        delay_cause  = random.choice([c for c in DELAY_CAUSES if c != "None"])
    else:
        delay_months = random.choices([0, 1, 2], weights=[60, 28, 12])[0]
        delay_cause  = "None" if delay_months == 0 else random.choice(DELAY_CAUSES[:-1])

    actual_duration_months = planned_duration_months + delay_months
    actual_end = start_date + timedelta(days=actual_duration_months * 30)

    # Status
    if actual_end <= END_DATE:
        status = "Completed"
    elif start_date + timedelta(days=planned_duration_months * 15) <= END_DATE:
        status = "Active"
    else:
        status = "Active"

    # Quality score
    q_range = PM_QUALITY[pm]
    quality_score = round(random.uniform(*q_range), 1) if status == "Completed" else None

    # Workforce
    size_factor = contracted_budget / 1000000
    workforce = int(random.uniform(8, 12) * size_factor ** 0.5)

    # Bid accuracy (how close the bid was to actual cost)
    bid_estimate = round(contracted_budget * random.uniform(0.90, 1.05), -2)
    bid_accuracy_pct = round((1 - abs(bid_estimate - actual_cost) / actual_cost) * 100, 1)

    records.append({
        "project_id":              f"SCL-{str(pid).zfill(4)}",
        "project_type":            ptype,
        "region":                  region,
        "project_manager":         pm,
        "tender_type":             tender,
        "start_date":              start_date.strftime("%Y-%m-%d"),
        "planned_end_date":        planned_end.strftime("%Y-%m-%d"),
        "actual_end_date":         actual_end.strftime("%Y-%m-%d") if status == "Completed" else None,
        "planned_duration_months": planned_duration_months,
        "actual_duration_months":  actual_duration_months,
        "delay_months":            delay_months,
        "delay_cause":             delay_cause,
        "status":                  status,
        "contracted_budget_bwp":   contracted_budget,
        "actual_cost_bwp":         actual_cost,
        "cost_variance_bwp":       cost_variance,
        "overrun_pct":             round(overrun_pct * 100, 1),
        "will_overrun":            int(will_overrun),
        "labour_cost_bwp":         labour_cost,
        "material_cost_bwp":       material_cost,
        "equipment_cost_bwp":      equipment_cost,
        "subcontractor_cost_bwp":  subcontractor_cost,
        "overhead_cost_bwp":       overhead_cost,
        "material_waste_cost_bwp": material_waste_cost,
        "material_waste_pct":      waste_pct,
        "workforce_headcount":     workforce,
        "quality_score":           quality_score,
        "bid_estimate_bwp":        bid_estimate,
        "bid_accuracy_pct":        bid_accuracy_pct,
        "risk_score":              round(pm_risk_score, 4),
    })

df = pd.DataFrame(records)
df.to_csv("project_data.csv", index=False)

completed = df[df["status"] == "Completed"]
overruns  = df[df["will_overrun"] == 1]

print(f"\n  Total projects        : {len(df):,}")
print(f"  Completed             : {len(completed):,}")
print(f"  Active                : {(df['status']=='Active').sum():,}")
print(f"  Projects with overruns: {len(overruns):,} ({len(overruns)/len(df)*100:.1f}%)")
print(f"  Total contracted value: P{df['contracted_budget_bwp'].sum():,.0f}")
print(f"  Total actual cost     : P{df['actual_cost_bwp'].sum():,.0f}")
print(f"  Total cost variance   : P{df['cost_variance_bwp'].sum():,.0f}")
print(f"  Total material waste  : P{df['material_waste_cost_bwp'].sum():,.0f}")
print(f"  Avg waste rate        : {df['material_waste_pct'].mean():.1f}%")
print(f"\n  Saved: project_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 60)
