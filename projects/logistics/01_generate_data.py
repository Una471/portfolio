"""
TRANSDELTA LOGISTICS - FLEET & DELIVERY DATA GENERATOR
Generates 140 vehicles, 8,000+ deliveries, 2 years of telematics data.
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
print("TRANSDELTA LOGISTICS - GENERATING DATA")
print("=" * 60)

# ── CONSTANTS ────────────────────────────────────────────────
N_VEHICLES   = 140
N_DELIVERIES = 8000
N_DRIVERS    = 140

VEHICLE_TYPES = {
    "Long-Haul Articulated": {"count": 55, "fuel_avg": 42, "capacity_tons": 30},
    "Refrigerated":          {"count": 25, "fuel_avg": 45, "capacity_tons": 18},
    "B-Train":               {"count": 30, "fuel_avg": 48, "capacity_tons": 40},
    "Light Commercial":      {"count": 20, "fuel_avg": 14, "capacity_tons": 3},
    "Courier Van":           {"count": 10, "fuel_avg": 11, "capacity_tons": 1},
}

ROUTES = [
    {"name": "Gaborone-Francistown",  "distance_km": 400,  "border": False, "avg_hrs": 5.0},
    {"name": "Gaborone-Johannesburg", "distance_km": 360,  "border": True,  "avg_hrs": 6.5},
    {"name": "Gaborone-Maun",         "distance_km": 680,  "border": False, "avg_hrs": 8.0},
    {"name": "Francistown-Harare",    "distance_km": 490,  "border": True,  "avg_hrs": 9.0},
    {"name": "Gaborone-Palapye",      "distance_km": 240,  "border": False, "avg_hrs": 3.0},
    {"name": "Gaborone-Windhoek",     "distance_km": 1400, "border": True,  "avg_hrs": 18.0},
    {"name": "Gaborone-Lusaka",       "distance_km": 1300, "border": True,  "avg_hrs": 20.0},
    {"name": "Local Gaborone",        "distance_km": 35,   "border": False, "avg_hrs": 1.5},
]

SECTORS = ["Mining", "Retail", "FMCG", "Construction", "Agriculture", "Pharmaceutical"]
CARGO_TYPES = ["General Goods", "Mining Supplies", "Fresh Produce", "Pharmaceuticals",
               "Construction Materials", "FMCG Cargo", "Agricultural Produce"]

START = datetime(2023, 1, 1)
END   = datetime(2025, 3, 31)

# ── VEHICLES ─────────────────────────────────────────────────
print("\n  Generating vehicle fleet...")
vehicles = []
vid = 1
for vtype, specs in VEHICLE_TYPES.items():
    for i in range(specs["count"]):
        manufacture_year = random.randint(2015, 2022)
        odometer = random.randint(80000, 450000)
        last_service_km = odometer - random.randint(5000, 35000)
        vehicles.append({
            "vehicle_id":        f"TD-{str(vid).zfill(3)}",
            "vehicle_type":      vtype,
            "manufacture_year":  manufacture_year,
            "age_years":         2025 - manufacture_year,
            "odometer_km":       odometer,
            "last_service_km":   last_service_km,
            "km_since_service":  odometer - last_service_km,
            "capacity_tons":     specs["capacity_tons"],
            "base_fuel_per100":  specs["fuel_avg"],
            "region":            random.choice(["Gaborone", "Francistown", "Maun", "Palapye"]),
        })
        vid += 1

vehicles_df = pd.DataFrame(vehicles)

# ── DRIVERS ──────────────────────────────────────────────────
print("  Generating driver profiles...")
drivers = []
for did in range(1, N_DRIVERS + 1):
    # Skill level drives most performance metrics
    skill = random.gauss(0.72, 0.15)
    skill = max(0.35, min(0.98, skill))

    harsh_brake_rate = max(0, 0.18 - skill * 0.12 + random.gauss(0, 0.02))
    speeding_rate    = max(0, 0.22 - skill * 0.16 + random.gauss(0, 0.03))
    idle_pct         = max(5, 28 - skill * 18 + random.gauss(0, 3))
    fuel_efficiency  = 0.7 + skill * 0.28 + random.gauss(0, 0.03)
    fuel_efficiency  = max(0.60, min(1.05, fuel_efficiency))

    drivers.append({
        "driver_id":        f"DRV-{str(did).zfill(3)}",
        "skill_score":      round(skill, 3),
        "harsh_brake_rate": round(harsh_brake_rate, 3),
        "speeding_rate":    round(speeding_rate, 3),
        "idle_pct":         round(idle_pct, 1),
        "fuel_efficiency":  round(fuel_efficiency, 3),
        "assigned_vehicle": vehicles[did - 1]["vehicle_id"] if did <= N_VEHICLES else None,
        "region":           random.choice(["Gaborone", "Francistown", "Maun", "Palapye"]),
    })

drivers_df = pd.DataFrame(drivers)

# ── DELIVERIES ───────────────────────────────────────────────
print("  Generating delivery records...")
deliveries = []
for i in range(N_DELIVERIES):
    route    = random.choice(ROUTES)
    vehicle  = random.choice(vehicles)
    driver   = random.choice(drivers)
    sector   = random.choice(SECTORS)
    cargo    = random.choice(CARGO_TYPES)

    days_off = random.randint(0, (END - START).days - 2)
    dep_date = START + timedelta(days=days_off)
    dep_time = dep_date + timedelta(hours=random.choice([5,6,7,8,14,15,16]))

    # Actual hours affected by driver skill, border wait, vehicle age
    border_delay = random.uniform(1.0, 4.5) if route["border"] else 0
    vehicle_age_factor = 1 + (vehicle["age_years"] - 5) * 0.02
    actual_hrs = route["avg_hrs"] * vehicle_age_factor + border_delay + random.gauss(0, 0.5)
    actual_hrs = max(route["avg_hrs"] * 0.85, actual_hrs)
    arr_time   = dep_time + timedelta(hours=actual_hrs)

    on_time = actual_hrs <= route["avg_hrs"] * 1.15
    delay_hrs = max(0, actual_hrs - route["avg_hrs"] * 1.15)

    # Fuel consumption
    base_fuel_per_100 = vehicle["base_fuel_per100"]
    driver_factor     = 2 - driver["fuel_efficiency"]
    load_factor       = random.uniform(0.6, 1.0)
    fuel_per_100      = base_fuel_per_100 * driver_factor * load_factor
    fuel_used_L       = route["distance_km"] / 100 * fuel_per_100
    fuel_cost_bwp     = fuel_used_L * random.uniform(9.8, 11.2)

    # Load utilisation
    load_tons = vehicle["capacity_tons"] * load_factor
    load_pct  = round(load_factor * 100, 1)

    # Harsh events
    harsh_events  = int(np.random.poisson(driver["harsh_brake_rate"] * route["distance_km"] / 100))
    speeding_events = int(np.random.poisson(driver["speeding_rate"] * route["distance_km"] / 100))
    idle_time_hrs = actual_hrs * driver["idle_pct"] / 100

    # Maintenance flag
    km_since_svc = vehicle["km_since_service"]
    maint_flag   = km_since_svc > 40000 or vehicle["age_years"] > 8

    # Revenue estimate
    base_rate_per_km = {"Long-Haul Articulated": 14, "Refrigerated": 18, "B-Train": 16,
                        "Light Commercial": 22, "Courier Van": 28}.get(vehicle["vehicle_type"], 14)
    revenue_bwp = route["distance_km"] * base_rate_per_km * load_factor

    deliveries.append({
        "delivery_id":     f"DLV-{str(i+1).zfill(5)}",
        "vehicle_id":      vehicle["vehicle_id"],
        "vehicle_type":    vehicle["vehicle_type"],
        "driver_id":       driver["driver_id"],
        "route":           route["name"],
        "distance_km":     route["distance_km"],
        "is_cross_border": int(route["border"]),
        "sector":          sector,
        "cargo_type":      cargo,
        "departure_date":  dep_time.strftime("%Y-%m-%d"),
        "planned_hrs":     route["avg_hrs"],
        "actual_hrs":      round(actual_hrs, 2),
        "on_time":         int(on_time),
        "delay_hrs":       round(delay_hrs, 2),
        "border_delay_hrs":round(border_delay, 2),
        "fuel_per_100km":  round(fuel_per_100, 1),
        "fuel_used_L":     round(fuel_used_L, 1),
        "fuel_cost_bwp":   round(fuel_cost_bwp, 0),
        "revenue_bwp":     round(revenue_bwp, 0),
        "load_tons":       round(load_tons, 1),
        "load_pct":        load_pct,
        "harsh_events":    harsh_events,
        "speeding_events": speeding_events,
        "idle_time_hrs":   round(idle_time_hrs, 2),
        "maint_flag":      int(maint_flag),
        "vehicle_age":     vehicle["age_years"],
        "year":            dep_time.year,
        "month":           f"{dep_time.year}-{dep_time.month:02d}",
    })

df = pd.DataFrame(deliveries)
df.to_csv("delivery_data.csv", index=False)

total_fuel_cost    = df["fuel_cost_bwp"].sum()
total_revenue      = df["revenue_bwp"].sum()
on_time_rate       = df["on_time"].mean() * 100
avg_fuel_per_100   = df["fuel_per_100km"].mean()
avg_load_pct       = df["load_pct"].mean()
total_harsh        = df["harsh_events"].sum()
maint_flagged      = df["maint_flag"].sum()

print(f"\n  Deliveries generated       : {len(df):,}")
print(f"  Total fuel cost            : P{total_fuel_cost:,.0f}")
print(f"  Total revenue              : P{total_revenue:,.0f}")
print(f"  On-time delivery rate      : {on_time_rate:.1f}%")
print(f"  Avg fuel per 100km         : {avg_fuel_per_100:.1f}L")
print(f"  Avg load utilisation       : {avg_load_pct:.1f}%")
print(f"  Total harsh braking events : {total_harsh:,}")
print(f"  Vehicles flagged for maint : {maint_flagged:,}")
print(f"\n  Saved: delivery_data.csv")
print("\n  Next: python 02_eda_ml.py")
print("=" * 60)
