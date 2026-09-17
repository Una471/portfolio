# complete_analysis.py

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("="*60)
print("MOLAO LEGAL ASSOCIATES - COMPLETE DATA ANALYSIS")
print("="*60)

# Load data
df = pd.read_csv('matter_data.csv')
df['open_date'] = pd.to_datetime(df['open_date'])
df['close_date'] = pd.to_datetime(df['close_date'], errors='coerce')

print(f"✅ Loaded {len(df)} matters")
print(f"✅ Active matters: {len(df[df['status'] == 'Active'])}")
print(f"✅ Completed matters: {len(df[df['status'] == 'Completed'])}")
print(f"✅ On Hold matters: {len(df[df['status'] == 'On Hold'])}")

# 1. CALCULATE KEY METRICS
total_matters = len(df)
active_matters = len(df[df['status'] == 'Active'])
completed_matters = len(df[df['status'] == 'Completed'])
on_hold_matters = len(df[df['status'] == 'On Hold'])

# Revenue metrics
total_potential = df['potential_fees_bwp'].sum()
total_billed = df['billed_fees_bwp'].sum()
total_leakage = df['leakage_bwp'].sum()
total_disbursements = df['disbursements_bwp'].sum()
total_outstanding = df['outstanding_bwp'].sum()

# Recording rate
avg_recording_rate = df['recording_rate'].mean() * 100

# 2. ANALYSIS BY PRACTICE AREA
print("\n" + "="*60)
print("ANALYSIS BY PRACTICE AREA")
print("="*60)

practice_area_stats = df.groupby('practice_area').agg({
    'matter_id': 'count',
    'potential_fees_bwp': 'sum',
    'billed_fees_bwp': 'sum',
    'leakage_bwp': 'sum',
    'recording_rate': 'mean',
    'outstanding_bwp': 'sum'
}).round(2).sort_values('billed_fees_bwp', ascending=False)

practice_area_stats['leakage_pct'] = (practice_area_stats['leakage_bwp'] / practice_area_stats['potential_fees_bwp']) * 100
practice_area_stats['recording_rate'] = practice_area_stats['recording_rate'] * 100

print(practice_area_stats[['matter_id', 'billed_fees_bwp', 'leakage_bwp', 'leakage_pct', 'recording_rate']])

# 3. ANALYSIS BY PARTNER
print("\n" + "="*60)
print("ANALYSIS BY PARTNER")
print("="*60)

partner_stats = df.groupby('partner').agg({
    'matter_id': 'count',
    'potential_fees_bwp': 'sum',
    'billed_fees_bwp': 'sum',
    'leakage_bwp': 'sum',
    'recording_rate': 'mean',
    'outstanding_bwp': 'sum'
}).round(2).sort_values('billed_fees_bwp', ascending=False)

partner_stats['leakage_pct'] = (partner_stats['leakage_bwp'] / partner_stats['potential_fees_bwp']) * 100
partner_stats['recording_rate'] = partner_stats['recording_rate'] * 100

print(partner_stats[['matter_id', 'billed_fees_bwp', 'leakage_bwp', 'leakage_pct', 'recording_rate']])

# 4. ANALYSIS BY CLIENT TYPE
print("\n" + "="*60)
print("ANALYSIS BY CLIENT TYPE")
print("="*60)

client_type_stats = df.groupby('client_type').agg({
    'matter_id': 'count',
    'billed_fees_bwp': 'sum',
    'leakage_bwp': 'sum',
    'outstanding_bwp': 'sum'
}).round(2).sort_values('billed_fees_bwp', ascending=False)

print(client_type_stats)

# 5. ANALYSIS BY CLIENT (TOP 10)
print("\n" + "="*60)
print("TOP 10 CLIENTS BY BILLINGS")
print("="*60)

client_stats = df.groupby('client_id').agg({
    'matter_id': 'count',
    'billed_fees_bwp': 'sum',
    'leakage_bwp': 'sum',
    'outstanding_bwp': 'sum'
}).round(2).sort_values('billed_fees_bwp', ascending=False).head(10)

print(client_stats)

# Top 10 client concentration
top_10_billings = client_stats['billed_fees_bwp'].sum()
total_billings = df['billed_fees_bwp'].sum()
concentration_pct = (top_10_billings / total_billings) * 100

print(f"\nTop 10 client concentration: {concentration_pct:.1f}% of total billings")

# 6. ANALYSIS BY YEAR
print("\n" + "="*60)
print("ANALYSIS BY YEAR")
print("="*60)

year_stats = df.groupby('year').agg({
    'matter_id': 'count',
    'billed_fees_bwp': 'sum',
    'leakage_bwp': 'sum',
    'recording_rate': 'mean'
}).round(2).sort_index()

year_stats['recording_rate'] = year_stats['recording_rate'] * 100

print(year_stats[['matter_id', 'billed_fees_bwp', 'leakage_bwp', 'recording_rate']])

# 7. OUTSTANDING DEBTORS ANALYSIS
print("\n" + "="*60)
print("OUTSTANDING DEBTORS ANALYSIS")
print("="*60)

# Outstanding by client type
outstanding_by_type = df.groupby('client_type')['outstanding_bwp'].sum().sort_values(ascending=False)
print(outstanding_by_type)

# Outstanding by practice area
outstanding_by_area = df.groupby('practice_area')['outstanding_bwp'].sum().sort_values(ascending=False)
print("\nOutstanding by practice area:")
print(outstanding_by_area)

# 8. SATISFACTION ANALYSIS
print("\n" + "="*60)
print("CLIENT SATISFACTION ANALYSIS")
print("="*60)

satisfaction_stats = df[df['satisfaction'].notna()].groupby('practice_area')['satisfaction'].mean().round(2).sort_values(ascending=False)
print(satisfaction_stats)

# 9. DURATION ANALYSIS
print("\n" + "="*60)
print("MATTER DURATION ANALYSIS")
print("="*60)

duration_stats = df.groupby('practice_area')['duration_days'].agg(['mean', 'median', 'count']).round(2).sort_values('mean', ascending=False)
print(duration_stats)

# 10. MACHINE LEARNING - LEAKAGE PREDICTION MODEL
print("\n" + "="*60)
print("TRAINING LEAKAGE PREDICTION MODEL")
print("="*60)

# Prepare data for ML - predict leakage based on matter characteristics
ml_df = df.copy()

# Select features
features = ['practice_area', 'partner', 'associate', 'client_type', 
            'duration_days', 'actual_hours', 'recorded_hours', 'hourly_rate',
            'disbursements_bwp']

# Encode categorical features
label_encoders = {}
for col in ['practice_area', 'partner', 'associate', 'client_type']:
    le = LabelEncoder()
    ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
    label_encoders[col] = le

# Prepare X and y (predict leakage)
X = ml_df[[col + '_encoded' if col in ['practice_area', 'partner', 'associate', 'client_type'] else col 
           for col in features]]
y = ml_df['leakage_bwp']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = model.score(X_test, y_test)
mae = np.mean(np.abs(y_test - y_pred))

print(f"Model R²: {r2:.4f} ({r2*100:.1f}% accuracy)")
print(f"Mean Absolute Error: P{mae:,.2f}")

# Feature importance
feature_names = [col + '_encoded' if col in ['practice_area', 'partner', 'associate', 'client_type'] else col 
                 for col in features]
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important factors for leakage:")
print(importance.head(5))

# 11. HIGH LEAKAGE MATTERS IDENTIFICATION
print("\n" + "="*60)
print("HIGH LEAKAGE MATTERS")
print("="*60)

# Identify matters with highest leakage
high_leakage = df[df['leakage_bwp'] > 0].sort_values('leakage_bwp', ascending=False).head(20)
high_leakage = high_leakage[['matter_id', 'practice_area', 'partner', 'recording_rate', 
                             'actual_hours', 'recorded_hours', 'leakage_bwp']]

print("Top 20 matters by leakage amount:")
print(high_leakage)

# 12. SAVE ALL DATA FOR DASHBOARD
print("\n" + "="*60)
print("SAVING DATA FOR DASHBOARD AND SAAS TOOL")
print("="*60)

# Key metrics
key_metrics = {
    'total_matters': int(total_matters),
    'active_matters': int(active_matters),
    'completed_matters': int(completed_matters),
    'on_hold_matters': int(on_hold_matters),
    'total_potential': float(total_potential),
    'total_billed': float(total_billed),
    'total_leakage': float(total_leakage),
    'total_disbursements': float(total_disbursements),
    'total_outstanding': float(total_outstanding),
    'avg_recording_rate': float(avg_recording_rate),
    'model_r2': float(r2),
    'model_accuracy': float(r2 * 100),
    'top_client_concentration': float(concentration_pct),
    'top_leakage_area': str(practice_area_stats['leakage_bwp'].idxmax()),
    'lowest_recording_partner': str(partner_stats['recording_rate'].idxmin())
}

# Convert stats to dict with string keys
practice_area_stats_dict = {}
for idx, row in practice_area_stats.iterrows():
    practice_area_stats_dict[str(idx)] = {
        'matter_id': int(row['matter_id']),
        'billed_fees_bwp': float(row['billed_fees_bwp']),
        'leakage_bwp': float(row['leakage_bwp']),
        'leakage_pct': float(row['leakage_pct']),
        'recording_rate': float(row['recording_rate'])
    }

partner_stats_dict = {}
for idx, row in partner_stats.iterrows():
    partner_stats_dict[str(idx)] = {
        'matter_id': int(row['matter_id']),
        'billed_fees_bwp': float(row['billed_fees_bwp']),
        'leakage_bwp': float(row['leakage_bwp']),
        'leakage_pct': float(row['leakage_pct']),
        'recording_rate': float(row['recording_rate'])
    }

client_type_stats_dict = {}
for idx, row in client_type_stats.iterrows():
    client_type_stats_dict[str(idx)] = {
        'matter_id': int(row['matter_id']),
        'billed_fees_bwp': float(row['billed_fees_bwp']),
        'leakage_bwp': float(row['leakage_bwp']),
        'outstanding_bwp': float(row['outstanding_bwp'])
    }

year_stats_dict = {}
for idx, row in year_stats.iterrows():
    year_stats_dict[str(idx)] = {
        'matter_id': int(row['matter_id']),
        'billed_fees_bwp': float(row['billed_fees_bwp']),
        'leakage_bwp': float(row['leakage_bwp']),
        'recording_rate': float(row['recording_rate'])
    }

# Top clients
top_clients_dict = {}
for idx, row in client_stats.iterrows():
    top_clients_dict[str(idx)] = {
        'matter_id': int(row['matter_id']),
        'billed_fees_bwp': float(row['billed_fees_bwp']),
        'leakage_bwp': float(row['leakage_bwp']),
        'outstanding_bwp': float(row['outstanding_bwp'])
    }

# High leakage matters
high_leakage_dict = []
for _, row in high_leakage.iterrows():
    high_leakage_dict.append({
        'matter_id': str(row['matter_id']),
        'practice_area': str(row['practice_area']),
        'partner': str(row['partner']),
        'recording_rate': float(row['recording_rate'] * 100),
        'actual_hours': float(row['actual_hours']),
        'recorded_hours': float(row['recorded_hours']),
        'leakage_bwp': float(row['leakage_bwp'])
    })

# Save to JSON files
with open('dashboard_data.json', 'w') as f:
    json.dump({
        'metrics': key_metrics,
        'practice_areas': practice_area_stats_dict,
        'partners': partner_stats_dict,
        'client_types': client_type_stats_dict,
        'years': year_stats_dict,
        'top_clients': top_clients_dict,
        'high_leakage': high_leakage_dict
    }, f, indent=2)

# Save model and encoders
joblib.dump(model, 'leakage_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

# Save reference data for SaaS tool
reference_data = {
    'partners': list(partner_stats.index),
    'practice_areas': list(practice_area_stats.index),
    'client_types': list(client_type_stats.index),
    'associates': list(df['associate'].unique())
}

with open('reference_data.json', 'w') as f:
    json.dump(reference_data, f, indent=2)

print("\n✅ All data saved successfully!")
print(f"📊 Dashboard data: dashboard_data.json")
print(f"🧠 Model: leakage_model.pkl")
print(f"🔑 Encoders: label_encoders.pkl")
print(f"📈 Reference data: reference_data.json")

# Print summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY")
print("="*60)
print(f"Total Matters: {key_metrics['total_matters']:,}")
print(f"Active Matters: {key_metrics['active_matters']:,}")
print(f"Completed Matters: {key_metrics['completed_matters']:,}")
print(f"Total Potential Fees: P{key_metrics['total_potential']:,.2f}")
print(f"Total Billed Fees: P{key_metrics['total_billed']:,.2f}")
print(f"Total Leakage: P{key_metrics['total_leakage']:,.2f}")
print(f"Average Recording Rate: {key_metrics['avg_recording_rate']:.1f}%")
print(f"Total Outstanding: P{key_metrics['total_outstanding']:,.2f}")
print(f"Top 10 Client Concentration: {key_metrics['top_client_concentration']:.1f}%")
print(f"Highest Leakage Area: {key_metrics['top_leakage_area']}")
print(f"Lowest Recording Partner: {key_metrics['lowest_recording_partner']}")
print(f"Model Accuracy: {key_metrics['model_accuracy']:.1f}%")
print("\n" + "="*60)