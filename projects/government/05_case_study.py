"""
BOTSWANA PUBLIC SERVICE - PROJECT CASE STUDY
=============================================
Business context, problem, approach, and results.
"""

# COMPANY PROFILE
"""
ORGANISATION : Botswana Public Service (Service Delivery Monitoring Unit)
LOCATION     : Government Enclave, Gaborone
INDUSTRY     : Government and Public Administration
ESTABLISHED  : Monitoring unit created 2019 under Ministry of State President
COVERAGE     : 9 departments, 5,000+ service requests analysed
DEPARTMENTS  : Health, Education, Police, BURS, Social Welfare,
               Immigration, Land Board, Works, Motor Registry
MANDATE      : Measure and improve service delivery performance
               across all public-facing departments
"""

# THE PROBLEM
"""
The Botswana Public Service was resolving only 65.9% of service requests
within their SLA targets. 13.6% of all requests escalated — meaning nearly
1 in 7 citizens who submitted a request experienced a service failure that
required formal escalation beyond first-level handling.

Three specific failures caused this:

PROBLEM 1 - NO EARLY WARNING SYSTEM
  Cases were flagged for escalation only after the SLA had already been
  breached. There was no mechanism to identify high-risk requests at the
  point of intake and route them proactively to senior officers.

PROBLEM 2 - LAND BOARD PERFORMANCE CRISIS
  The Land Board department had a 6% SLA compliance rate and an average
  resolution time of 48 days against a 21-day target. This had persisted
  for years with no data-backed intervention plan. Land title delays
  directly impact property development and housing access.

PROBLEM 3 - DIGITAL CHANNEL UNDERUTILISATION
  Digital submission channels show significantly better SLA compliance
  and faster resolution times, but the majority of citizens still submit
  in person. No data-driven strategy existed to accelerate digital adoption.
"""

# PRIOR ATTEMPTS
"""
ATTEMPT 1 - MONTHLY DEPARTMENTAL REPORTS (2019-2022)
  Each department submitted a monthly performance report to the monitoring unit.
  Failed because: formats were inconsistent, definitions differed across
  departments, and the 4-6 week lag meant deterioration was invisible until
  it had already compounded.

ATTEMPT 2 - COMPLAINT-TRIGGERED REVIEWS (2020-2023)
  Formal complaints triggered ad hoc reviews of specific cases.
  Failed because: every formal complaint was already a service failure.
  The system was reactive by design, with no ability to prevent escalations
  before they became formal complaints.

ATTEMPT 3 - HEADCOUNT INCREASES IN STRUGGLING DEPARTMENTS
  Additional officers were deployed to high-escalation departments.
  Failed because: without understanding which types of cases escalated most
  and why, the additional capacity was spread across all cases rather than
  concentrated on high-risk intake.
"""

# ANALYTICAL APPROACH
"""
ROLE     : Data and Analytics Consultant (Contract)
REPORTING: Director, Service Delivery Monitoring Unit

STEP 1 - DATA STRUCTURING
  Consolidated 5,000 service request records across 9 departments into a
  unified dataset with consistent definitions, 17 fields per record, and
  calculated fields for SLA compliance, breach days, and escalation status.

STEP 2 - EXPLORATORY DATA ANALYSIS
  Identified the key patterns across seven analytical dimensions:
  department performance, channel performance, district analysis,
  escalation patterns, monthly trends, digital channel impact,
  and officer-level analysis.

STEP 3 - ESCALATION RISK MODEL
  Trained a Gradient Boosting classifier to predict escalation probability
  for any service request at intake, before processing begins. Features
  include department, service type, submission channel, district, SLA
  target, and case complexity. Model AUC: 0.89 on held-out test data.

STEP 4 - DELIVERABLES
  03_dashboard.html: Service delivery analytics dashboard with four pages
  covering portfolio overview, department performance, escalation analysis,
  and channel performance. Sidebar slicers filter all charts by department,
  channel, district, and status.

  04_software_tool.html: CivicTrack, a service request escalation risk
  screener. Officers enter the request details at intake and receive an
  immediate escalation probability, factor breakdown, and routing
  recommendation before the case enters the processing queue.
"""

# RESULTS
"""
SERVICE DELIVERY IMPACT IDENTIFIED
  Overall SLA compliance rate     : 65.9% (government target: above 80%)
  Overall escalation rate         : 13.6% of all requests
  Land Board SLA rate             : 6% (worst performing department)
  Motor Registry SLA rate         : 96% (internal benchmark)
  Gap between best and worst dept : 90 percentage points

DIGITAL CHANNEL EVIDENCE
  Digital submission closes cases significantly faster than In-Person
  across every department. This is the clearest evidence base for
  an accelerated digital adoption programme.

OPERATIONAL OUTCOMES
  - Every incoming service request can now be screened for escalation risk
    in under 60 seconds at the point of intake
  - High-risk cases can be routed to senior officers before the SLA window
    begins to narrow, rather than after it has already been breached
  - Land Board's specific failure pattern is now documented with data,
    enabling a targeted process and resource intervention rather than
    a generalised headcount increase
  - Cross-departmental comparison on a single dashboard enables the
    monitoring unit to identify deterioration within days rather than months

ESCALATION RATE TARGET
  From 13.6% to below 8% within 18 months through combination of
  risk-based routing at intake and targeted departmental improvements
"""
