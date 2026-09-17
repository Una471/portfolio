"""05_case_study.py — TRANSDELTA LOGISTICS"""

# COMPANY
"""
Transdelta Logistics (Pty) Ltd | Gaborone, A1 Corridor | Founded 2006
P118M annual revenue | 430 employees | 140 vehicles | Citizen-owned
Road freight, refrigerated transport, cross-border forwarding, warehousing, courier
Routes: Botswana-wide + South Africa, Zimbabwe, Zambia, Namibia
"""

# THE PROBLEM
"""
P12-16M per year in avoidable fuel and maintenance costs due to:
- Unoptimised routing (experience-based dispatch, not data-driven)
- Unmonitored driver behaviour (harsh braking, speeding, idling driving up fuel)
- Reactive calendar-based maintenance (missing early failure signals)
- No on-time delivery KPIs (SLA compliance unknown until client complains)

GPS telematics exists on all 140 vehicles but is only used for real-time tracking.
No one is extracting the performance data from it.

FUEL IMPACT:
  Fuel = 38% of operating costs
  At P118M revenue, fuel spend is approx P45M/year
  10% efficiency improvement = P4.5M annual saving

MAINTENANCE IMPACT:
  Calendar-based servicing leads to both over-servicing (waste) and
  missed early failure detection (breakdown on long-haul routes = direct
  repair cost + SLA penalty from mining clients with penalty clauses)

DRIVER IMPACT:
  Harsh braking increases fuel consumption by up to 15%
  Speeding accelerates tyre and brake wear
  Neither metric has ever been measured or acted on
"""

# APPROACH
"""
STEP 1 - DATA GENERATION
  140 vehicles across 5 types (Long-Haul Articulated, Refrigerated, B-Train,
  Light Commercial, Courier Van). 8,000 deliveries across 8 route corridors,
  January 2023 to March 2025. Driver skill scores drive fuel consumption,
  harsh braking rates, and on-time performance.

STEP 2 - EDA
  Route performance: on-time rate, fuel cost as % of revenue, avg border wait.
  Driver performance: composite score (fuel 30%, on-time 25%, safety 25%, reliability 20%).
  Fleet maintenance: ML model to predict maintenance probability from age, km, wear signals.

STEP 3 - MODELS
  Driver Performance Score (0-100 composite, 140 drivers tiered into 4 bands).
  Predictive Maintenance Model (GradientBoosting, AUC 1.0 on clean synthetic data).

STEP 4 - DELIVERABLES
  03_dashboard.html: Orange/charcoal dark fleet analytics dashboard. 5 pages:
    Overview, Routes, Drivers, Fleet & Maintenance, Trip Log. 4 sidebar slicers.
  04_software_tool.html: RouteIQ — trip efficiency checker. Forest green/white
    professional theme with animated truck hero. Checks fuel, load, driver behaviour,
    delivery status. Returns efficiency score 0-100 with savings estimate and actions.
"""

# RESULTS
"""
FLEET OVERVIEW
  Total deliveries                : 8,000
  Total revenue                   : P68.4M (2-year sample)
  Total fuel cost                 : P17.2M (25.2% of revenue)
  On-time delivery rate           : 49.0%
  Avg load utilisation            : 80.0%
  Avg fuel per 100km              : 33.0L
  Total harsh braking events      : 4,721
  Total km driven                 : 4,960,235

DRIVER FINDINGS
  140 drivers scored on composite index
  Top performers: significantly better fuel per 100km and on-time rates
  Bottom quartile: harsh events 3-5x higher than top performers

ROUTE FINDINGS
  Gaborone-Windhoek: highest fuel cost ratio (long distance + border delays)
  Local Gaborone: best on-time performance, lowest absolute fuel cost
  Cross-border routes: avg border delay adds 1.5-3h per trip

MAINTENANCE FINDINGS
  Predictive model identifies high-risk vehicles before breakdown
  Key features: vehicle age, total km, harsh events, avg fuel consumption
"""
