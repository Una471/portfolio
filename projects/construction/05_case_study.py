"""
SETSHABA CONSTRUCTION (PTY) LTD - PROJECT CASE STUDY
=====================================================
Business context, problem, approach, and results.
"""

# COMPANY PROFILE
"""
COMPANY     : Setshaba Construction (Pty) Ltd
LOCATION    : Gaborone, Botswana (offices in Francistown and Palapye)
INDUSTRY    : Construction and Civil Engineering
FOUNDED     : 2004
SIZE        : 280-400 staff | 300+ projects over 7 years | P65-80M annual revenue
OPERATING   : Gaborone, Francistown, Palapye, Maun, Serowe
WEBSITE     : setshaba.co.bw

Setshaba Construction executes government and private sector contracts across
roads, residential buildings, commercial structures, schools, clinics, and
government offices. Between 2018 and 2025 the company managed 300 projects
with a combined contracted value exceeding P450 million.
"""

# THE PROBLEM
"""
52% of all projects exceeded their contracted budget.
Aggregate cost overruns across the 300-project portfolio: P75 million.
Material waste averaged 12.1% of total material cost: P24 million in preventable loss.
No system existed to identify at-risk projects before overruns became unrecoverable.

Three specific failures caused this:

PROBLEM 1 - NO EARLY WARNING SYSTEM
  Financial variances were only discovered at periodic cost review meetings,
  typically when the project was already 40-60% complete and corrective
  action was expensive or impossible. By the time overruns were visible,
  they were already embedded in the project cost.

PROBLEM 2 - MANAGER PERFORMANCE OPACITY
  Four project managers each carried concurrent portfolios. No objective data
  existed to compare their overrun rates, delay patterns, waste levels, or
  quality scores. Managers were assigned projects based on availability and
  seniority, not on data-driven matching of manager risk profile to project type.

PROBLEM 3 - REACTIVE BID PRICING
  Tender bids were priced based on individual manager experience and informal
  comparable estimates. No systematic model connected project type, scale,
  region, and workforce requirements to expected cost outcomes. Contingency
  was guessed rather than calculated, leading to bids that were either too
  tight (creating negative-margin contracts) or too conservative (losing tenders).
"""

# PRIOR ATTEMPTS
"""
ATTEMPT 1 - SPREADSHEET COST REPORTS (2018-2023)
  Each site supervisor maintained their own Excel cost report per project.
  Failed because: reports were never aggregated, formats were inconsistent
  across sites, and no one was analysing patterns across the portfolio.

ATTEMPT 2 - MONTHLY PROJECT REVIEW MEETINGS (2020-2024)
  Senior managers held monthly reviews with project managers to discuss
  status verbally.
  Failed because: discussions were retrospective, data was anecdotal,
  and there was no consistent framework for escalating at-risk projects.

ATTEMPT 3 - EXTERNAL QUANTITY SURVEYOR REVIEWS (2022)
  Two projects used external QS firms to review cost plans at bid stage.
  Failed because: expensive, slow, and not scalable across the full tender
  pipeline. Applied only to the largest contracts, leaving the majority of
  projects without any quantitative review.
"""

# ANALYTICAL APPROACH
"""
ROLE     : Data and Analytics Consultant (Contract)
REPORTING: Managing Director and Finance Director

STEP 1 - DATA EXTRACTION
  Extracted 300 project records from site spreadsheets, accounting system,
  and procurement records covering 2018 to 2025. Cleaned and standardised
  into a unified dataset with 27 fields per project.

STEP 2 - EXPLORATORY DATA ANALYSIS
  Identified the key patterns: which project types overrun most, which
  managers have the highest variance rates, which regions carry the most
  delivery risk, and what delay causes drive the largest cost impacts.

STEP 3 - RISK MODEL DEVELOPMENT
  Trained a Gradient Boosting classifier on the 300-project dataset to
  predict overrun probability for any new tender at bid stage. Features
  include project type, region, assigned manager, contracted budget,
  planned duration, and workforce headcount. Model AUC: 0.8+ on test data.

STEP 4 - DELIVERABLES
  03_dashboard.html: Portfolio intelligence dashboard for management with
  four pages covering portfolio overview, financial performance, project
  manager scorecards, and risk register.

  04_software_tool.html: SiteRisk, a bid-stage project risk assessment tool
  that gives any construction company a data-backed overrun probability score,
  risk factor breakdown, comparable project benchmarks, and management
  recommendation before any tender is submitted.
"""

# RESULTS
"""
FINANCIAL IMPACT IDENTIFIED
  Total cost variance across 300 projects    : P308 million
  Material waste cost (preventable)          : P107 million
  Annualised overrun exposure                : P44 million per year

OPERATIONAL OUTCOMES
  - Four project managers now have objective quarterly scorecards covering
    overrun rate, delay months, waste percentage, and quality score
  - Every new tender can be assessed for overrun risk in under two minutes
    before submission, enabling right-sized contingency pricing
  - Active project risk register flags 109 Critical and 19 High Risk
    projects for management attention
  - Material waste patterns identified by project type and region, enabling
    targeted procurement forecasting

INVESTMENT AND RETURN
  Analytics engagement cost : P95,000
  Overrun rate target       : From 43% to below 30% over 24 months
  Annual benefit if achieved: P12-15 million in recovered margin
  ROI projection            : 126x over 24 months
"""
