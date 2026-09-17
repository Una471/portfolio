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
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("BOTSWANA PUBLIC SERVICE - COMPLETE DATA ANALYSIS")
print("="*60)

# Load data
df = pd.read_csv('service_data.csv')
df['submit_date'] = pd.to_datetime(df['submit_date'])
df['resolution_date'] = pd.to_datetime(df['resolution_date'], errors='coerce')

print(f"✅ Loaded {len(df)} service requests")
print(f"✅ Resolved requests: {len(df[df['status'] == 'Resolved'])}")
print(f"✅ Pending requests: {len(df[df['status'] == 'Pending'])}")

# 1. CALCULATE KEY METRICS
total_requests = int(len(df))
resolved_requests = int(len(df[df['status'] == 'Resolved']))
pending_requests = int(len(df[df['status'] == 'Pending']))
escalated_requests = int(len(df[df['escalated'] == 1]))
escalation_rate = float((escalated_requests / total_requests) * 100)

# SLA compliance
within_sla = int(len(df[df['within_sla'] == 1]))
sla_compliance_rate = float((within_sla / resolved_requests) * 100) if resolved_requests > 0 else 0

# Average resolution time
avg_resolution_days = float(df[df['status'] == 'Resolved']['actual_days'].mean())
avg_sla_breach = float(df[df['within_sla'] == 0]['sla_breach_days'].mean()) if len(df[df['within_sla'] == 0]) > 0 else 0

# 2. DEPARTMENT PERFORMANCE
print("\n" + "="*60)
print("DEPARTMENT PERFORMANCE ANALYSIS")
print("="*60)

dept_stats = df.groupby('department').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'escalated': 'sum',
    'actual_days': 'mean'
}).round(2)

dept_stats['sla_rate'] = (dept_stats['within_sla'] / dept_stats['request_id']) * 100
dept_stats['escalation_rate'] = (dept_stats['escalated'] / dept_stats['request_id']) * 100
dept_stats = dept_stats.sort_values('sla_rate', ascending=True)

print(dept_stats[['request_id', 'sla_rate', 'escalation_rate', 'actual_days']])

# 3. CHANNEL PERFORMANCE
print("\n" + "="*60)
print("CHANNEL PERFORMANCE ANALYSIS")
print("="*60)

channel_stats = df.groupby('channel').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'actual_days': 'mean'
}).round(2)

channel_stats['sla_rate'] = (channel_stats['within_sla'] / channel_stats['request_id']) * 100
channel_stats = channel_stats.sort_values('sla_rate', ascending=False)

print(channel_stats[['request_id', 'sla_rate', 'actual_days']])

# 4. DISTRICT ANALYSIS
print("\n" + "="*60)
print("DISTRICT PERFORMANCE ANALYSIS")
print("="*60)

district_stats = df.groupby('district').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'escalated': 'sum',
    'actual_days': 'mean'
}).round(2)

district_stats['sla_rate'] = (district_stats['within_sla'] / district_stats['request_id']) * 100
district_stats['escalation_rate'] = (district_stats['escalated'] / district_stats['request_id']) * 100
district_stats = district_stats.sort_values('sla_rate', ascending=True)

print(district_stats[['request_id', 'sla_rate', 'escalation_rate', 'actual_days']])

# 5. ESCALATION PATTERNS
print("\n" + "="*60)
print("ESCALATION PATTERNS")
print("="*60)

escalation_by_dept = df[df['escalated'] == 1].groupby('department').agg({
    'request_id': 'count'
}).round(2).sort_values('request_id', ascending=False)

print(escalation_by_dept)

# 6. SERVICE TYPE ANALYSIS
print("\n" + "="*60)
print("SERVICE TYPE ANALYSIS")
print("="*60)

service_stats = df.groupby('service_type').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'actual_days': 'mean'
}).round(2)

service_stats['sla_rate'] = (service_stats['within_sla'] / service_stats['request_id']) * 100
service_stats = service_stats.sort_values('sla_rate', ascending=True)

print(service_stats[['request_id', 'sla_rate', 'actual_days']])

# 7. COMPLEXITY IMPACT
print("\n" + "="*60)
print("COMPLEXITY IMPACT ANALYSIS")
print("="*60)

complexity_stats = df.groupby('complexity').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'escalated': 'sum',
    'actual_days': 'mean'
}).round(2)

complexity_stats['sla_rate'] = (complexity_stats['within_sla'] / complexity_stats['request_id']) * 100
complexity_stats['escalation_rate'] = (complexity_stats['escalated'] / complexity_stats['request_id']) * 100
complexity_stats = complexity_stats.sort_values('complexity')

print(complexity_stats[['request_id', 'sla_rate', 'escalation_rate', 'actual_days']])

# 8. OFFICER-LEVEL ANALYSIS
print("\n" + "="*60)
print("OFFICER PERFORMANCE ANALYSIS")
print("="*60)

# Calculate officer workload and performance
officer_stats = df.groupby('officer_id').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'actual_days': 'mean'
}).round(2)

officer_stats['sla_rate'] = (officer_stats['within_sla'] / officer_stats['request_id']) * 100
officer_stats = officer_stats[officer_stats['request_id'] >= 5].sort_values('sla_rate', ascending=False)

print(f"Top 10 officers by SLA compliance (min 5 requests):")
print(officer_stats.head(10)[['request_id', 'sla_rate', 'actual_days']])

# 9. MONTHLY TREND
print("\n" + "="*60)
print("MONTHLY TREND ANALYSIS")
print("="*60)

df['month'] = df['submit_date'].dt.to_period('M')
monthly_stats = df.groupby('month').agg({
    'request_id': 'count',
    'within_sla': 'sum',
    'escalated': 'sum'
}).round(2)

monthly_stats['sla_rate'] = (monthly_stats['within_sla'] / monthly_stats['request_id']) * 100
monthly_stats['escalation_rate'] = (monthly_stats['escalated'] / monthly_stats['request_id']) * 100

print(monthly_stats[['request_id', 'sla_rate', 'escalation_rate']])

# 10. MACHINE LEARNING - ESCALATION PREDICTION MODEL
print("\n" + "="*60)
print("TRAINING ESCALATION PREDICTION MODEL")
print("="*60)

# Prepare data for ML
ml_df = df.copy()
ml_df['escalated'] = ml_df['escalated'].astype(int)

# Select features for model
features = ['department', 'service_type', 'channel', 'district', 
            'sla_target_days', 'complexity']

# Encode categorical features
label_encoders = {}
for col in ['department', 'service_type', 'channel', 'district']:
    le = LabelEncoder()
    # Handle NaN values in categorical columns
    ml_df[col] = ml_df[col].fillna('Unknown')
    ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
    label_encoders[col] = le

# Handle NaN values in numerical columns
numerical_features = ['sla_target_days', 'complexity']
imputer = SimpleImputer(strategy='median')
ml_df[numerical_features] = imputer.fit_transform(ml_df[numerical_features])

# Prepare X and y
X = ml_df[[col + '_encoded' if col in ['department', 'service_type', 'channel', 'district'] else col 
           for col in features]]
y = ml_df['escalated']

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
feature_names = [col + '_encoded' if col in ['department', 'service_type', 'channel', 'district'] else col 
                 for col in features]
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important escalation signals:")
print(importance.head(5))

# 11. HIGH-RISK PENDING REQUESTS
print("\n" + "="*60)
print("HIGH-RISK PENDING REQUESTS")
print("="*60)

# Predict escalation probability for pending requests
pending_df = df[df['status'] == 'Pending'].copy()

# Handle NaN in pending requests for prediction
for col in ['department', 'service_type', 'channel', 'district']:
    pending_df[col] = pending_df[col].fillna('Unknown')

for col in numerical_features:
    pending_df[col] = pending_df[col].fillna(pending_df[col].median())

high_risk_requests = []
for _, row in pending_df.iterrows():
    features_encoded = []
    for col in ['department', 'service_type', 'channel', 'district']:
        try:
            val = label_encoders[col].transform([row[col]])[0]
        except:
            val = 0
        features_encoded.append(val)
    
    for col in numerical_features:
        features_encoded.append(row[col])
    
    try:
        escalation_prob = model.predict_proba([features_encoded])[0][1]
    except:
        escalation_prob = 0.5  # Default if prediction fails
    
    high_risk_requests.append({
        'request_id': str(row['request_id']),
        'department': str(row['department']),
        'service_type': str(row['service_type']),
        'channel': str(row['channel']),
        'submitted': str(row['submit_date'].date()) if pd.notna(row['submit_date']) else 'Unknown',
        'escalation_probability': float(escalation_prob),
        'risk_level': 'Critical' if escalation_prob > 0.8 else 'High' if escalation_prob > 0.6 else 'Medium' if escalation_prob > 0.3 else 'Low'
    })

high_risk_requests = sorted(high_risk_requests, key=lambda x: x['escalation_probability'], reverse=True)

print(f"Critical risk requests (80%+): {sum(1 for r in high_risk_requests if r['risk_level'] == 'Critical')}")
print(f"High risk requests (60-80%): {sum(1 for r in high_risk_requests if r['risk_level'] == 'High')}")
print(f"Medium risk requests (30-60%): {sum(1 for r in high_risk_requests if r['risk_level'] == 'Medium')}")
print(f"Low risk requests (<30%): {sum(1 for r in high_risk_requests if r['risk_level'] == 'Low')}")

# 12. SAVE ALL DATA FOR DASHBOARD
print("\n" + "="*60)
print("SAVING DATA FOR DASHBOARD AND SAAS TOOL")
print("="*60)

# Key metrics - ensure all are native Python types
key_metrics = {
    'total_requests': int(total_requests),
    'resolved_requests': int(resolved_requests),
    'pending_requests': int(pending_requests),
    'escalated_requests': int(escalated_requests),
    'escalation_rate': float(escalation_rate),
    'within_sla': int(within_sla),
    'sla_compliance_rate': float(sla_compliance_rate),
    'avg_resolution_days': float(avg_resolution_days),
    'avg_sla_breach': float(avg_sla_breach),
    'model_accuracy': float(accuracy * 100),
    'model_auc': float(auc_score),
    'best_department': str(dept_stats[dept_stats['sla_rate'] == dept_stats['sla_rate'].max()].index[0]),
    'worst_department': str(dept_stats[dept_stats['sla_rate'] == dept_stats['sla_rate'].min()].index[0]),
    'best_channel': str(channel_stats[channel_stats['sla_rate'] == channel_stats['sla_rate'].max()].index[0])
}

# Convert stats to dict with string keys
dept_stats_dict = {}
for idx, row in dept_stats.iterrows():
    dept_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'escalated': int(row['escalated']),
        'actual_days': float(row['actual_days']),
        'sla_rate': float(row['sla_rate']),
        'escalation_rate': float(row['escalation_rate'])
    }

channel_stats_dict = {}
for idx, row in channel_stats.iterrows():
    channel_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'actual_days': float(row['actual_days']),
        'sla_rate': float(row['sla_rate'])
    }

district_stats_dict = {}
for idx, row in district_stats.iterrows():
    district_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'escalated': int(row['escalated']),
        'actual_days': float(row['actual_days']),
        'sla_rate': float(row['sla_rate']),
        'escalation_rate': float(row['escalation_rate'])
    }

service_stats_dict = {}
for idx, row in service_stats.iterrows():
    service_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'actual_days': float(row['actual_days']),
        'sla_rate': float(row['sla_rate'])
    }

escalation_by_dept_dict = {}
for idx, row in escalation_by_dept.iterrows():
    escalation_by_dept_dict[str(idx)] = {
        'request_id': int(row['request_id'])
    }

complexity_stats_dict = {}
for idx, row in complexity_stats.iterrows():
    complexity_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'escalated': int(row['escalated']),
        'actual_days': float(row['actual_days']),
        'sla_rate': float(row['sla_rate']),
        'escalation_rate': float(row['escalation_rate'])
    }

monthly_stats_dict = {}
for idx, row in monthly_stats.iterrows():
    monthly_stats_dict[str(idx)] = {
        'request_id': int(row['request_id']),
        'within_sla': int(row['within_sla']),
        'escalated': int(row['escalated']),
        'sla_rate': float(row['sla_rate']),
        'escalation_rate': float(row['escalation_rate'])
    }

# Save to JSON files
with open('dashboard_data.json', 'w') as f:
    json.dump({
        'metrics': key_metrics,
        'departments': dept_stats_dict,
        'channels': channel_stats_dict,
        'districts': district_stats_dict,
        'services': service_stats_dict,
        'escalations': escalation_by_dept_dict,
        'complexity': complexity_stats_dict,
        'monthly': monthly_stats_dict,
        'high_risk': high_risk_requests[:20]  # Top 20 riskiest pending requests
    }, f, indent=2)

# Save model and encoders
joblib.dump(model, 'escalation_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("\n✅ All data saved successfully!")
print(f"📊 Dashboard data: dashboard_data.json")
print(f"🧠 Model: escalation_model.pkl")
print(f"🔑 Encoders: label_encoders.pkl")

# Print summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY")
print("="*60)
print(f"Total Service Requests: {key_metrics['total_requests']:,}")
print(f"Resolved Requests: {key_metrics['resolved_requests']:,}")
print(f"Pending Requests: {key_metrics['pending_requests']:,}")
print(f"Escalated Requests: {key_metrics['escalated_requests']:,}")
print(f"Escalation Rate: {key_metrics['escalation_rate']:.1f}%")
print(f"SLA Compliance Rate: {key_metrics['sla_compliance_rate']:.1f}%")
print(f"Average Resolution Time: {key_metrics['avg_resolution_days']:.1f} days")
print(f"Average SLA Breach: {key_metrics['avg_sla_breach']:.1f} days")
print(f"Model Accuracy: {key_metrics['model_accuracy']:.1f}%")
print(f"Model AUC: {key_metrics['model_auc']:.3f}")
print(f"Best Department: {key_metrics['best_department']}")
print(f"Worst Department: {key_metrics['worst_department']}")
print(f"Best Channel: {key_metrics['best_channel']}")
print("\n" + "="*60)