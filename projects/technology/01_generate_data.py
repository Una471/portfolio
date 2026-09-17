"""
TECHPULSE SAAS - CUSTOMER DATA GENERATOR
Run this first. Generates 3,000 customer records across 4 subscription plans.
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
print("TECHPULSE SAAS - GENERATING CUSTOMER DATA")
print("=" * 60)

N_CUSTOMERS = 3000

PLANS = ["Free", "Starter", "Professional", "Enterprise"]

PLAN_PRICE = {
    "Free": 0,
    "Starter": 245,
    "Professional": 798,
    "Enterprise": 2299,
}

PLAN_WEIGHTS = [40, 32, 20, 8]  # % distribution

INDUSTRIES = [
    "Retail", "Professional Services", "Hospitality", "Construction",
    "Healthcare", "Education", "Agriculture", "Logistics", "Finance", "NGO"
]

REGIONS = ["Gaborone", "Francistown", "Maun", "Serowe", "Palapye", "Lobatse"]

FEATURES = [
    "Financial Dashboard", "Expense Tracking", "Invoice Management",
    "Sales Pipeline", "Inventory Management", "Custom Reports",
    "API Integrations", "Multi-User Access", "VAT Compliance",
    "Payment Tracking",
]

PLAN_FEATURE_ACCESS = {
    "Free":         FEATURES[:3],
    "Starter":      FEATURES[:5],
    "Professional": FEATURES[:8],
    "Enterprise":   FEATURES,
}

CHURN_BASE = {
    "Free":         0.60,
    "Starter":      0.38,
    "Professional": 0.22,
    "Enterprise":   0.08,
}

START_DATE = datetime(2020, 6, 1)
END_DATE   = datetime(2025, 3, 31)

ACQUISITION_CHANNELS = [
    "Organic Search", "Referral", "Social Media",
    "Direct Sales", "Partnership", "Event"
]

print(f"\n  Generating {N_CUSTOMERS:,} customer records...")

records = []
for cid in range(1, N_CUSTOMERS + 1):
    plan = random.choices(PLANS, weights=PLAN_WEIGHTS)[0]
    industry = random.choice(INDUSTRIES)
    region   = random.choices(
        REGIONS, weights=[45, 20, 10, 10, 8, 7])[0]
    channel  = random.choice(ACQUISITION_CHANNELS)

    # Signup date spread
    days_offset = random.randint(0, (END_DATE - START_DATE).days - 90)
    signup_date = START_DATE + timedelta(days=days_offset)

    # Usage behaviour (correlated with plan)
    plan_usage_factor = {"Free": 0.4, "Starter": 0.65, "Professional": 0.85, "Enterprise": 0.95}[plan]

    logins_per_week = max(0, np.random.normal(
        {"Free": 1.4, "Starter": 2.8, "Professional": 4.5, "Enterprise": 6.2}[plan],
        {"Free": 1.2, "Starter": 1.5, "Professional": 1.8, "Enterprise": 2.0}[plan]
    ))

    features_adopted = min(
        len(PLAN_FEATURE_ACCESS[plan]),
        max(0, int(np.random.normal(
            {"Free": 2.1, "Starter": 3.4, "Professional": 5.8, "Enterprise": 8.6}[plan],
            {"Free": 0.9, "Starter": 1.2, "Professional": 1.4, "Enterprise": 1.1}[plan]
        )))
    )

    sessions_per_month = max(0, np.random.normal(
        logins_per_week * 4.3, logins_per_week * 1.5))

    onboarding_complete = random.random() < {
        "Free": 0.25, "Starter": 0.48, "Professional": 0.71, "Enterprise": 0.92}[plan]

    support_tickets = max(0, int(np.random.poisson(
        {"Free": 0.4, "Starter": 1.2, "Professional": 2.1, "Enterprise": 3.5}[plan])))

    nps_score = None
    if random.random() < 0.55:
        nps_base = {"Free": 18, "Starter": 28, "Professional": 38, "Enterprise": 55}[plan]
        nps_score = max(-100, min(100, int(np.random.normal(nps_base, 25))))

    # Payment health
    failed_payments = 0
    if plan != "Free":
        failed_payments = max(0, int(np.random.poisson(
            {"Starter": 0.5, "Professional": 0.3, "Enterprise": 0.1}[plan])))

    # Upgrade/downgrade history
    has_upgraded   = plan != "Free" and random.random() < 0.35
    has_downgraded = plan in ["Starter", "Free"] and random.random() < 0.12

    # Churn calculation
    churn_base = CHURN_BASE[plan]
    churn_adj  = 0.0

    if logins_per_week < 2:      churn_adj += 0.18
    if features_adopted <= 2:    churn_adj += 0.15
    if not onboarding_complete:  churn_adj += 0.10
    if failed_payments > 0:      churn_adj += 0.12
    if support_tickets > 3:      churn_adj += 0.08
    if has_downgraded:           churn_adj += 0.15
    if nps_score is not None and nps_score < 0: churn_adj += 0.10
    if features_adopted >= 5:    churn_adj -= 0.12
    if logins_per_week >= 4:     churn_adj -= 0.15
    if has_upgraded:             churn_adj -= 0.10

    churn_prob = max(0.02, min(0.95, churn_base + churn_adj + random.gauss(0, 0.04)))
    did_churn  = random.random() < churn_prob

    # Days to churn (if churned)
    tenure_days = None
    churn_date  = None
    status      = "Active"

    max_days = (END_DATE - signup_date).days
    if did_churn and max_days > 30:
        if plan == "Free":
            avg_churn_days = 45
        elif plan == "Starter":
            avg_churn_days = 120
        elif plan == "Professional":
            avg_churn_days = 220
        else:
            avg_churn_days = 380

        days_to_churn = max(30, min(max_days - 1,
            int(np.random.exponential(avg_churn_days))))
        churn_date = signup_date + timedelta(days=days_to_churn)
        tenure_days = days_to_churn
        status = "Churned"
    else:
        tenure_days = (END_DATE - signup_date).days
        status = "Active"

    # MRR
    mrr = PLAN_PRICE[plan]

    # Churn risk level
    if churn_prob >= 0.65:   risk_level = "Critical"
    elif churn_prob >= 0.45: risk_level = "High"
    elif churn_prob >= 0.25: risk_level = "Medium"
    else:                    risk_level = "Low"

    # Cohort (year of signup)
    cohort = signup_date.year

    records.append({
        "customer_id":        f"TP-{str(cid).zfill(5)}",
        "plan":               plan,
        "industry":           industry,
        "region":             region,
        "acquisition_channel":channel,
        "signup_date":        signup_date.strftime("%Y-%m-%d"),
        "churn_date":         churn_date.strftime("%Y-%m-%d") if churn_date else None,
        "status":             status,
        "tenure_days":        tenure_days,
        "cohort":             cohort,
        "mrr_bwp":            mrr,
        "logins_per_week":    round(logins_per_week, 2),
        "features_adopted":   features_adopted,
        "sessions_per_month": round(sessions_per_month, 1),
        "onboarding_complete":int(onboarding_complete),
        "support_tickets":    support_tickets,
        "nps_score":          nps_score,
        "failed_payments":    failed_payments,
        "has_upgraded":       int(has_upgraded),
        "has_downgraded":     int(has_downgraded),
        "churn_probability":  round(churn_prob, 4),
        "risk_level":         risk_level,
    })

df = pd.DataFrame(records)
df.to_csv("customer_data.csv", index=False)

churned = df[df["status"] == "Churned"]
active  = df[df["status"] == "Active"]
paid    = df[df["plan"] != "Free"]

print(f"\n  Total customers        : {len(df):,}")
print(f"  Active                 : {len(active):,}")
print(f"  Churned                : {len(churned):,} ({len(churned)/len(df)*100:.1f}%)")
print(f"  Total MRR              : P{df[df['status']=='Active']['mrr_bwp'].sum():,.0f}")
print(f"  Annual Recurring Rev   : P{df[df['status']=='Active']['mrr_bwp'].sum()*12:,.0f}")
print(f"  Avg churn probability  : {df['churn_probability'].mean()*100:.1f}%")
print(f"\n  By plan:")
for plan in PLANS:
    sub     = df[df["plan"] == plan]
    ch      = sub[sub["status"] == "Churned"]
    mrr_tot = sub[sub["status"]=="Active"]["mrr_bwp"].sum()
    print(f"    {plan:<15}: {len(sub):>4} customers | Churn: {len(ch)/len(sub)*100:.0f}% | MRR: P{mrr_tot:,.0f}")
print(f"\n  Saved: customer_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 60)
