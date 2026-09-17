# complete_analysis.py

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("="*60)
print("TECHPULSE SAAS - COMPLETE DATA ANALYSIS")
print("="*60)

# Load data
df = pd.read_csv('customer_data.csv')
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['churn_date'] = pd.to_datetime(df['churn_date'], errors='coerce')

print(f"✅ Loaded {len(df)} customers")
print(f"✅ Active customers: {len(df[df['status'] == 'Active'])}")
print(f"✅ Churned customers: {len(df[df['status'] == 'Churned'])}")

# 1. CALCULATE KEY METRICS
total_customers = int(len(df))
active_customers = int(len(df[df['status'] == 'Active']))
churned_customers = int(len(df[df['status'] == 'Churned']))
churn_rate = float((churned_customers / total_customers) * 100)

# MRR calculations
active_mrr = float(df[df['status'] == 'Active']['mrr_bwp'].sum())
churned_mrr = float(df[df['status'] == 'Churned']['mrr_bwp'].sum())
total_mrr = float(df['mrr_bwp'].sum())

# Plan distribution
plan_stats = df.groupby('plan').agg({
    'customer_id': 'count',
    'mrr_bwp': 'sum',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)

plan_stats['churn_rate'] = (plan_stats['status'] / plan_stats['customer_id']) * 100

# 2. CHURN ANALYSIS BY PLAN
print("\n" + "="*60)
print("CHURN ANALYSIS BY PLAN")
print("="*60)
print(plan_stats[['customer_id', 'mrr_bwp', 'churn_rate']])

# 3. CHURN ANALYSIS BY INDUSTRY
industry_stats = df.groupby('industry').agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
industry_stats['churn_rate'] = (industry_stats['status'] / industry_stats['customer_id']) * 100
industry_stats = industry_stats.sort_values('churn_rate', ascending=False)

print("\n" + "="*60)
print("CHURN BY INDUSTRY")
print("="*60)
print(industry_stats[['customer_id', 'churn_rate']])

# 4. CHURN ANALYSIS BY ACQUISITION CHANNEL
channel_stats = df.groupby('acquisition_channel').agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
channel_stats['churn_rate'] = (channel_stats['status'] / channel_stats['customer_id']) * 100
channel_stats = channel_stats.sort_values('churn_rate', ascending=False)

print("\n" + "="*60)
print("CHURN BY ACQUISITION CHANNEL")
print("="*60)
print(channel_stats[['customer_id', 'churn_rate']])

# 5. BEHAVIORAL ANALYSIS - LOGINS
print("\n" + "="*60)
print("BEHAVIORAL ANALYSIS - LOGIN FREQUENCY")
print("="*60)

# Create login categories
df['login_category'] = pd.cut(df['logins_per_week'], 
                               bins=[0, 1, 2, 5, 100], 
                               labels=['<1', '1-2', '2-5', '5+'])

login_churn = df.groupby('login_category', observed=False).agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
login_churn['churn_rate'] = (login_churn['status'] / login_churn['customer_id']) * 100

print(login_churn[['customer_id', 'churn_rate']])

# 6. BEHAVIORAL ANALYSIS - FEATURES ADOPTED
print("\n" + "="*60)
print("BEHAVIORAL ANALYSIS - FEATURES ADOPTED")
print("="*60)

df['feature_category'] = pd.cut(df['features_adopted'], 
                                 bins=[-1, 2, 4, 6, 100], 
                                 labels=['0-2', '3-4', '5-6', '7+'])

feature_churn = df.groupby('feature_category', observed=False).agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
feature_churn['churn_rate'] = (feature_churn['status'] / feature_churn['customer_id']) * 100

print(feature_churn[['customer_id', 'churn_rate']])

# 7. ONBOARDING IMPACT
print("\n" + "="*60)
print("ONBOARDING IMPACT")
print("="*60)

onboarding_stats = df.groupby('onboarding_complete').agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
onboarding_stats['churn_rate'] = (onboarding_stats['status'] / onboarding_stats['customer_id']) * 100

print(onboarding_stats[['customer_id', 'churn_rate']])

# 8. SUPPORT TICKETS IMPACT
print("\n" + "="*60)
print("SUPPORT TICKETS IMPACT")
print("="*60)

ticket_stats = df.groupby('support_tickets').agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
ticket_stats['churn_rate'] = (ticket_stats['status'] / ticket_stats['customer_id']) * 100

print(ticket_stats[['customer_id', 'churn_rate']])

# 9. NPS SCORE IMPACT
print("\n" + "="*60)
print("NPS SCORE IMPACT")
print("="*60)

df['nps_category'] = pd.cut(df['nps_score'], 
                             bins=[-100, 0, 50, 100], 
                             labels=['Detractors', 'Passives', 'Promoters'])

nps_churn = df.groupby('nps_category', observed=False).agg({
    'customer_id': 'count',
    'status': lambda x: (x == 'Churned').sum()
}).round(2)
nps_churn['churn_rate'] = (nps_churn['status'] / nps_churn['customer_id']) * 100

print(nps_churn[['customer_id', 'churn_rate']])

# 10. MACHINE LEARNING - CHURN PREDICTION MODEL
print("\n" + "="*60)
print("TRAINING CHURN PREDICTION MODEL")
print("="*60)

# Prepare data for ML - FIX: Handle NaN values
ml_df = df.copy()
ml_df['is_churned'] = (ml_df['status'] == 'Churned').astype(int)

# Select features for model
features = ['plan', 'industry', 'region', 'acquisition_channel', 
            'logins_per_week', 'features_adopted', 'sessions_per_month',
            'onboarding_complete', 'support_tickets', 'nps_score', 
            'failed_payments', 'has_upgraded', 'has_downgraded']

# Encode categorical features
label_encoders = {}
for col in ['plan', 'industry', 'region', 'acquisition_channel']:
    le = LabelEncoder()
    # Handle NaN values in categorical columns
    ml_df[col] = ml_df[col].fillna('Unknown')
    ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
    label_encoders[col] = le

# Handle NaN values in numerical columns - FIX: Impute with median
numerical_features = ['logins_per_week', 'features_adopted', 'sessions_per_month',
                      'onboarding_complete', 'support_tickets', 'nps_score', 
                      'failed_payments', 'has_upgraded', 'has_downgraded']

imputer = SimpleImputer(strategy='median')
ml_df[numerical_features] = imputer.fit_transform(ml_df[numerical_features])

# Prepare X and y
X = ml_df[[col + '_encoded' if col in ['plan', 'industry', 'region', 'acquisition_channel'] else col 
           for col in features]]
y = ml_df['is_churned']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_names = [col + '_encoded' if col in ['plan', 'industry', 'region', 'acquisition_channel'] else col 
                 for col in features]
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important churn signals:")
print(importance.head(5))

# 11. HIGH-RISK CUSTOMERS IDENTIFICATION
print("\n" + "="*60)
print("HIGH-RISK CUSTOMERS")
print("="*60)

# Predict churn probability for all active customers
active_customers_df = df[df['status'] == 'Active'].copy()

# Handle NaN in active customers for prediction
for col in ['plan', 'industry', 'region', 'acquisition_channel']:
    active_customers_df[col] = active_customers_df[col].fillna('Unknown')

for col in numerical_features:
    active_customers_df[col] = active_customers_df[col].fillna(active_customers_df[col].median())

risk_customers = []
for _, row in active_customers_df.iterrows():
    features_encoded = []
    for col in ['plan', 'industry', 'region', 'acquisition_channel']:
        try:
            val = label_encoders[col].transform([row[col]])[0]
        except:
            val = 0
        features_encoded.append(val)
    
    for col in numerical_features:
        features_encoded.append(row[col])
    
    churn_prob = model.predict_proba([features_encoded])[0][1]
    
    risk_customers.append({
        'customer_id': str(row['customer_id']),
        'plan': str(row['plan']),
        'industry': str(row['industry']),
        'mrr_bwp': float(row['mrr_bwp']),
        'churn_probability': float(churn_prob),
        'risk_level': 'Critical' if churn_prob > 0.8 else 'High' if churn_prob > 0.6 else 'Medium' if churn_prob > 0.3 else 'Low'
    })

risk_customers = sorted(risk_customers, key=lambda x: x['churn_probability'], reverse=True)

print(f"Critical risk customers (80%+): {sum(1 for r in risk_customers if r['risk_level'] == 'Critical')}")
print(f"High risk customers (60-80%): {sum(1 for r in risk_customers if r['risk_level'] == 'High')}")
print(f"Medium risk customers (30-60%): {sum(1 for r in risk_customers if r['risk_level'] == 'Medium')}")
print(f"Low risk customers (<30%): {sum(1 for r in risk_customers if r['risk_level'] == 'Low')}")

# 12. SAVE ALL DATA FOR DASHBOARD
print("\n" + "="*60)
print("SAVING DATA FOR DASHBOARD AND SAAS TOOL")
print("="*60)

# Key metrics - FIX: Ensure all values are native Python types
key_metrics = {
    'total_customers': int(total_customers),
    'active_customers': int(active_customers),
    'churned_customers': int(churned_customers),
    'churn_rate': float(churn_rate),
    'active_mrr': float(active_mrr),
    'churned_mrr': float(churned_mrr),
    'total_mrr': float(total_mrr),
    'model_accuracy': float(accuracy * 100),
    'top_churn_industry': str(industry_stats.index[0]),
    'top_churn_channel': str(channel_stats.index[0])
}

# Convert stats to dict with string keys
plan_stats_dict = {}
for idx, row in plan_stats.iterrows():
    plan_stats_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'mrr_bwp': float(row['mrr_bwp']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

industry_stats_dict = {}
for idx, row in industry_stats.iterrows():
    industry_stats_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

channel_stats_dict = {}
for idx, row in channel_stats.iterrows():
    channel_stats_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

login_churn_dict = {}
for idx, row in login_churn.iterrows():
    login_churn_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

feature_churn_dict = {}
for idx, row in feature_churn.iterrows():
    feature_churn_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

onboarding_stats_dict = {}
for idx, row in onboarding_stats.iterrows():
    onboarding_stats_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

nps_churn_dict = {}
for idx, row in nps_churn.iterrows():
    nps_churn_dict[str(idx)] = {
        'customer_id': int(row['customer_id']),
        'churned': int(row['status']),
        'churn_rate': float(row['churn_rate'])
    }

# Save to JSON files
with open('dashboard_data.json', 'w') as f:
    json.dump({
        'metrics': key_metrics,
        'plans': plan_stats_dict,
        'industries': industry_stats_dict,
        'channels': channel_stats_dict,
        'logins': login_churn_dict,
        'features': feature_churn_dict,
        'onboarding': onboarding_stats_dict,
        'nps': nps_churn_dict,
        'risk_customers': risk_customers[:20]  # Top 20 riskiest customers
    }, f, indent=2)

# Save model and encoders
joblib.dump(model, 'churn_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("\n✅ All data saved successfully!")
print(f"📊 Dashboard data: dashboard_data.json")
print(f"🧠 Model: churn_model.pkl")
print(f"🔑 Encoders: label_encoders.pkl")

# Print summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY")
print("="*60)
print(f"Total Customers: {key_metrics['total_customers']:,}")
print(f"Active Customers: {key_metrics['active_customers']:,}")
print(f"Churned Customers: {key_metrics['churned_customers']:,}")
print(f"Overall Churn Rate: {key_metrics['churn_rate']:.1f}%")
print(f"Active MRR: P{key_metrics['active_mrr']:,.2f}")
print(f"Churned MRR: P{key_metrics['churned_mrr']:,.2f}")
print(f"Total MRR: P{key_metrics['total_mrr']:,.2f}")
print(f"Model Accuracy: {key_metrics['model_accuracy']:.1f}%")
print(f"Highest Churn Industry: {key_metrics['top_churn_industry']}")
print(f"Highest Churn Channel: {key_metrics['top_churn_channel']}")
print("\n" + "="*60)