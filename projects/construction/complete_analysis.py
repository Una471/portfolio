# complete_analysis.py

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib

print("="*60)
print("SETSHABA CONSTRUCTION - COMPLETE DATA ANALYSIS")
print("="*60)

# Load data
df = pd.read_csv('project_data.csv')
df['start_date'] = pd.to_datetime(df['start_date'])
df['planned_end_date'] = pd.to_datetime(df['planned_end_date'])
df['actual_end_date'] = pd.to_datetime(df['actual_end_date'], errors='coerce')

print(f"✅ Loaded {len(df)} projects")
print(f"✅ Completed projects: {len(df[df['status'] == 'Completed'])}")
print(f"✅ Active projects: {len(df[df['status'] == 'Active'])}")

# 1. CALCULATE KEY METRICS
total_projects = int(len(df))
completed_projects = int(len(df[df['status'] == 'Completed']))
active_projects = int(len(df[df['status'] == 'Active']))
overrun_projects = int(len(df[df['will_overrun'] == 1]))
overrun_rate = float((overrun_projects / completed_projects) * 100) if completed_projects > 0 else 0

# Cost calculations
total_contracted = float(df['contracted_budget_bwp'].sum())
total_actual = float(df['actual_cost_bwp'].sum())
total_variance = float(total_actual - total_contracted)
total_overrun_cost = float(df[df['will_overrun'] == 1]['cost_variance_bwp'].sum())
total_material_waste = float(df['material_waste_cost_bwp'].sum())
avg_waste_pct = float(df['material_waste_pct'].mean())

# 2. OVERRUN ANALYSIS BY PROJECT TYPE
print("\n" + "="*60)
print("OVERRUN ANALYSIS BY PROJECT TYPE")
print("="*60)

project_type_stats = df.groupby('project_type').agg({
    'project_id': 'count',
    'will_overrun': 'sum',
    'cost_variance_bwp': 'sum',
    'overrun_pct': 'mean'
}).round(2)

project_type_stats['overrun_rate'] = (project_type_stats['will_overrun'] / project_type_stats['project_id']) * 100
project_type_stats = project_type_stats.sort_values('overrun_rate', ascending=False)

print(project_type_stats[['project_id', 'overrun_rate', 'cost_variance_bwp', 'overrun_pct']])

# 3. OVERRUN ANALYSIS BY REGION
print("\n" + "="*60)
print("OVERRUN BY REGION")
print("="*60)

region_stats = df.groupby('region').agg({
    'project_id': 'count',
    'will_overrun': 'sum',
    'cost_variance_bwp': 'sum'
}).round(2)

region_stats['overrun_rate'] = (region_stats['will_overrun'] / region_stats['project_id']) * 100
region_stats = region_stats.sort_values('overrun_rate', ascending=False)

print(region_stats[['project_id', 'overrun_rate', 'cost_variance_bwp']])

# 4. OVERRUN ANALYSIS BY PROJECT MANAGER
print("\n" + "="*60)
print("OVERRUN BY PROJECT MANAGER")
print("="*60)

manager_stats = df.groupby('project_manager').agg({
    'project_id': 'count',
    'will_overrun': 'sum',
    'cost_variance_bwp': 'sum',
    'delay_months': 'mean',
    'material_waste_pct': 'mean',
    'quality_score': 'mean'
}).round(2)

manager_stats['overrun_rate'] = (manager_stats['will_overrun'] / manager_stats['project_id']) * 100
manager_stats = manager_stats.sort_values('overrun_rate', ascending=False)

print(manager_stats[['project_id', 'overrun_rate', 'cost_variance_bwp', 'delay_months', 'material_waste_pct', 'quality_score']])

# 5. DELAY ANALYSIS
print("\n" + "="*60)
print("DELAY ANALYSIS")
print("="*60)

delay_stats = df[df['delay_months'] > 0].groupby('delay_cause').agg({
    'project_id': 'count',
    'delay_months': 'mean',
    'cost_variance_bwp': 'sum',
    'will_overrun': 'sum'
}).round(2)

delay_stats['overrun_rate'] = (delay_stats['will_overrun'] / delay_stats['project_id']) * 100
delay_stats = delay_stats.sort_values('delay_months', ascending=False)

print(delay_stats[['project_id', 'delay_months', 'overrun_rate', 'cost_variance_bwp']])

# 6. MATERIAL WASTE ANALYSIS
print("\n" + "="*60)
print("MATERIAL WASTE ANALYSIS")
print("="*60)

waste_stats = df.groupby('project_type').agg({
    'material_waste_cost_bwp': 'sum',
    'material_waste_pct': 'mean',
    'project_id': 'count'
}).round(2).sort_values('material_waste_pct', ascending=False)

print(waste_stats[['project_id', 'material_waste_cost_bwp', 'material_waste_pct']])

# 7. QUALITY SCORE ANALYSIS
print("\n" + "="*60)
print("QUALITY SCORE ANALYSIS")
print("="*60)

quality_stats = df.groupby('project_manager').agg({
    'quality_score': 'mean',
    'project_id': 'count',
    'will_overrun': 'sum'
}).round(2).sort_values('quality_score', ascending=False)

quality_stats['overrun_rate'] = (quality_stats['will_overrun'] / quality_stats['project_id']) * 100

print(quality_stats[['project_id', 'quality_score', 'overrun_rate']])

# 8. MACHINE LEARNING - OVERRUN PREDICTION MODEL
print("\n" + "="*60)
print("TRAINING OVERRUN PREDICTION MODEL")
print("="*60)

# Prepare data for ML
ml_df = df.copy()

# Select features for model - FIX: Use only completed projects for training
ml_df = ml_df[ml_df['status'] == 'Completed'].copy()
ml_df['will_overrun'] = ml_df['will_overrun'].astype(int)

# Features
features = ['project_type', 'region', 'project_manager', 'tender_type',
            'planned_duration_months', 'contracted_budget_bwp', 
            'workforce_headcount', 'quality_score']

# Encode categorical features
label_encoders = {}
for col in ['project_type', 'region', 'project_manager', 'tender_type']:
    le = LabelEncoder()
    # Handle NaN values in categorical columns
    ml_df[col] = ml_df[col].fillna('Unknown')
    ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
    label_encoders[col] = le

# Handle NaN values in numerical columns - FIX: Use SimpleImputer
numerical_features = ['planned_duration_months', 'contracted_budget_bwp', 
                      'workforce_headcount', 'quality_score']

imputer = SimpleImputer(strategy='median')
ml_df[numerical_features] = imputer.fit_transform(ml_df[numerical_features])

# Prepare X and y
X = ml_df[[col + '_encoded' if col in ['project_type', 'region', 'project_manager', 'tender_type'] else col 
           for col in features]]
y = ml_df['will_overrun']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
print(f"AUC Score: {auc_score:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_names = [col + '_encoded' if col in ['project_type', 'region', 'project_manager', 'tender_type'] else col 
                 for col in features]
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important overrun signals:")
print(importance.head(5))

# 9. HIGH-RISK PROJECTS IDENTIFICATION
print("\n" + "="*60)
print("HIGH-RISK PROJECTS")
print("="*60)

# Predict overrun probability for all active projects
active_projects_df = df[df['status'] == 'Active'].copy()

# FIX: Handle NaN in active projects for prediction
# Create a copy of the imputer fitted on training data
active_projects_df[numerical_features] = imputer.transform(active_projects_df[numerical_features])

# Fill any remaining NaN values
active_projects_df = active_projects_df.fillna(0)

risk_projects = []
for _, row in active_projects_df.iterrows():
    features_encoded = []
    for col in ['project_type', 'region', 'project_manager', 'tender_type']:
        try:
            val = label_encoders[col].transform([row[col]])[0]
        except:
            val = 0
        features_encoded.append(val)
    
    for col in numerical_features:
        features_encoded.append(row[col])
    
    try:
        overrun_prob = model.predict_proba([features_encoded])[0][1]
    except:
        overrun_prob = 0.5  # Default if prediction fails
    
    risk_projects.append({
        'project_id': str(row['project_id']),
        'project_type': str(row['project_type']),
        'region': str(row['region']),
        'project_manager': str(row['project_manager']),
        'contracted_budget_bwp': float(row['contracted_budget_bwp']),
        'overrun_probability': float(overrun_prob),
        'risk_level': 'Critical' if overrun_prob > 0.8 else 'High' if overrun_prob > 0.6 else 'Medium' if overrun_prob > 0.3 else 'Low'
    })

risk_projects = sorted(risk_projects, key=lambda x: x['overrun_probability'], reverse=True)

print(f"Critical risk projects (80%+): {sum(1 for r in risk_projects if r['risk_level'] == 'Critical')}")
print(f"High risk projects (60-80%): {sum(1 for r in risk_projects if r['risk_level'] == 'High')}")
print(f"Medium risk projects (30-60%): {sum(1 for r in risk_projects if r['risk_level'] == 'Medium')}")
print(f"Low risk projects (<30%): {sum(1 for r in risk_projects if r['risk_level'] == 'Low')}")

# 10. SAVE ALL DATA FOR DASHBOARD
print("\n" + "="*60)
print("SAVING DATA FOR DASHBOARD AND SAAS TOOL")
print("="*60)

# Key metrics
key_metrics = {
    'total_projects': int(total_projects),
    'completed_projects': int(completed_projects),
    'active_projects': int(active_projects),
    'overrun_projects': int(overrun_projects),
    'overrun_rate': float(overrun_rate),
    'total_contracted': float(total_contracted),
    'total_actual': float(total_actual),
    'total_variance': float(total_variance),
    'total_overrun_cost': float(total_overrun_cost),
    'total_material_waste': float(total_material_waste),
    'avg_waste_pct': float(avg_waste_pct),
    'model_accuracy': float(accuracy * 100),
    'model_auc': float(auc_score),
    'top_overrun_type': str(project_type_stats.index[0]),
    'top_overrun_region': str(region_stats.index[0]),
    'top_overrun_manager': str(manager_stats.index[0])
}

# Convert stats to dict with string keys
project_type_stats_dict = {}
for idx, row in project_type_stats.iterrows():
    project_type_stats_dict[str(idx)] = {
        'project_id': int(row['project_id']),
        'will_overrun': int(row['will_overrun']),
        'cost_variance_bwp': float(row['cost_variance_bwp']),
        'overrun_pct': float(row['overrun_pct']),
        'overrun_rate': float(row['overrun_rate'])
    }

region_stats_dict = {}
for idx, row in region_stats.iterrows():
    region_stats_dict[str(idx)] = {
        'project_id': int(row['project_id']),
        'will_overrun': int(row['will_overrun']),
        'cost_variance_bwp': float(row['cost_variance_bwp']),
        'overrun_rate': float(row['overrun_rate'])
    }

manager_stats_dict = {}
for idx, row in manager_stats.iterrows():
    manager_stats_dict[str(idx)] = {
        'project_id': int(row['project_id']),
        'will_overrun': int(row['will_overrun']),
        'cost_variance_bwp': float(row['cost_variance_bwp']),
        'delay_months': float(row['delay_months']),
        'material_waste_pct': float(row['material_waste_pct']),
        'quality_score': float(row['quality_score']),
        'overrun_rate': float(row['overrun_rate'])
    }

delay_stats_dict = {}
for idx, row in delay_stats.iterrows():
    delay_stats_dict[str(idx)] = {
        'project_id': int(row['project_id']),
        'delay_months': float(row['delay_months']),
        'will_overrun': int(row['will_overrun']),
        'overrun_rate': float(row['overrun_rate']),
        'cost_variance_bwp': float(row['cost_variance_bwp'])
    }

waste_stats_dict = {}
for idx, row in waste_stats.iterrows():
    waste_stats_dict[str(idx)] = {
        'project_id': int(row['project_id']),
        'material_waste_cost_bwp': float(row['material_waste_cost_bwp']),
        'material_waste_pct': float(row['material_waste_pct'])
    }

# Save to JSON files
with open('dashboard_data.json', 'w') as f:
    json.dump({
        'metrics': key_metrics,
        'project_types': project_type_stats_dict,
        'regions': region_stats_dict,
        'managers': manager_stats_dict,
        'delays': delay_stats_dict,
        'waste': waste_stats_dict,
        'risk_projects': risk_projects[:20]  # Top 20 riskiest projects
    }, f, indent=2)

# Save model and encoders
joblib.dump(model, 'overrun_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("\n✅ All data saved successfully!")
print(f"📊 Dashboard data: dashboard_data.json")
print(f"🧠 Model: overrun_model.pkl")
print(f"🔑 Encoders: label_encoders.pkl")

# Print summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY")
print("="*60)
print(f"Total Projects: {key_metrics['total_projects']:,}")
print(f"Completed Projects: {key_metrics['completed_projects']:,}")
print(f"Active Projects: {key_metrics['active_projects']:,}")
print(f"Projects with Overruns: {key_metrics['overrun_projects']:,}")
print(f"Overall Overrun Rate: {key_metrics['overrun_rate']:.1f}%")
print(f"Total Contracted: P{key_metrics['total_contracted']:,.2f}")
print(f"Total Actual Cost: P{key_metrics['total_actual']:,.2f}")
print(f"Total Variance: P{key_metrics['total_variance']:,.2f}")
print(f"Total Overrun Cost: P{key_metrics['total_overrun_cost']:,.2f}")
print(f"Total Material Waste: P{key_metrics['total_material_waste']:,.2f}")
print(f"Average Waste %: {key_metrics['avg_waste_pct']:.1f}%")
print(f"Model Accuracy: {key_metrics['model_accuracy']:.1f}%")
print(f"Model AUC: {key_metrics['model_auc']:.3f}")
print(f"Highest Overrun Type: {key_metrics['top_overrun_type']}")
print(f"Highest Overrun Region: {key_metrics['top_overrun_region']}")
print(f"Highest Overrun Manager: {key_metrics['top_overrun_manager']}")
print("\n" + "="*60)