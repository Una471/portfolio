"""05_case_study.py — TECHPULSE SAAS"""

# COMPANY
"""
TechPulse SaaS | Gaborone Innovation Hub | Founded 2020
P14.4M ARR | 3,000 registered users | 38 employees
Cloud BI platform for SMEs: financial tracking, inventory, sales pipeline, reporting
Four tiers: Free, Starter (P245/mo), Professional (P798/mo), Enterprise (P2,299/mo)
"""

# THE PROBLEM
"""
35% overall churn rate — rebuilding nearly a third of the customer base every year.
Free plan converts at a rate too low to sustain the growth model.
Customer success team operating reactively with no data-driven prioritisation.

PROBLEM 1 - NO CHURN EARLY WARNING
  Customer success only finds out an account is churning when it cancels.
  By the time a cancellation request arrives, the customer has already
  mentally left — usually weeks or months earlier. The disengagement
  signal (fewer logins, fewer features used) is visible in usage data
  but was never being monitored systematically.

PROBLEM 2 - FREE PLAN FUNNEL FAILURE
  60% of Free users churn without ever converting to a paid tier.
  The Free plan has no conversion urgency: indefinite free access
  removes the pressure to upgrade, and Free users adopt only 2.1
  features on average — not enough to reach the value realisation
  moment that triggers a paid conversion.

PROBLEM 3 - CUSTOMER SUCCESS AT SCALE WITHOUT DATA
  5 CS reps covering 3,000 accounts cannot run proactive outreach
  without knowing which accounts to prioritise. Without a churn
  risk score, outreach defaults to arbitrary or the loudest voice —
  which means low-risk accounts get attention while silent churners
  go undetected until they cancel.
"""

# APPROACH
"""
STEP 1 - DATA ANALYSIS
  Analysed 3,000 customer records covering subscription plan, usage
  behaviour (logins, features, sessions), onboarding completion,
  payment history, NPS, and acquisition channel from June 2020
  to March 2025.

STEP 2 - EDA
  Identified that login frequency is the strongest single behavioural
  predictor of churn. Customers logging in fewer than 2 times per week
  show dramatically higher churn rates. Feature adoption below 3 in the
  first 30 days is the second strongest signal. These two signals together
  identify the majority of churn cases before the cancellation decision.

STEP 3 - CHURN MODEL
  Gradient Boosting classifier trained on 80% of the dataset and validated
  on 20%. AUC: 0.87. Features: plan, industry, channel, logins, features,
  sessions, onboarding, support tickets, payment failures, upgrade/downgrade
  history, MRR.

STEP 4 - DELIVERABLES
  03_dashboard.html: Retention analytics dashboard with four pages —
  Overview, Plans, Behaviour, Churn Risk. Five sidebar slicers.
  All charts recalculate from the filtered customer dataset.

  04_software_tool.html: RetainIQ, a customer churn risk scorer.
  CS reps enter an account's subscription and usage details and receive
  an immediate health score, behavioural signal breakdown, three
  prioritised CS actions, and a management recommendation.
"""

# RESULTS
"""
FINANCIAL IMPACT IDENTIFIED
  Active MRR                   : P1,017,861
  Annual ARR                   : P12,214,332
  Free plan: 91% churn, P0 MRR contribution
  Enterprise: 4% churn, P492K MRR — most valuable cohort
  Revenue saved if churn reduced from 35% to 22%: P2-3M ARR

KEY FINDINGS
  - Login frequency below 2/week is the highest-weight churn signal
  - Feature adoption above 5 reduces churn probability by ~18 percentage points
  - Customers who complete onboarding churn at significantly lower rates
  - Referral and Partnership channels produce the lowest churn rates
  - Downgrade history is a strong churn precursor — 15 percentage point uplift
"""
