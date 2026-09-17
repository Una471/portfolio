# complete_analysis.py

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("="*60)
print("PULA PROPERTY GROUP - COMPLETE DATA ANALYSIS")
print("="*60)

# Load data
df = pd.read_csv('property_data.csv')
df['listing_date'] = pd.to_datetime(df['listing_date'])
df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

print(f"✅ Loaded {len(df)} properties")
print(f"✅ Active listings: {len(df[df['deal_status'] == 'Active'])}")
print(f"✅ Closed deals: {len(df[df['deal_status'] == 'Closed'])}")

# 1. FILTER CLOSED DEALS
closed_df = df[df['deal_status'] == 'Closed'].copy()

# 2. CALCULATE KEY METRICS
total_commission = float(closed_df['commission_earned_bwp'].sum())
total_lost = float(closed_df['commission_lost_bwp'].sum())
potential_revenue = total_commission + total_lost
recovery_rate = (total_commission / potential_revenue) * 100 if potential_revenue > 0 else 0

active_listings = int(len(df[df['deal_status'] == 'Active']))
avg_days = float(closed_df['days_on_market'].mean())
avg_pricing_error = float(closed_df['pricing_error_pct'].mean())

# 3. AGENT PERFORMANCE
agent_stats = closed_df.groupby('agent').agg({
    'property_id': 'count',
    'commission_earned_bwp': 'sum',
    'commission_lost_bwp': 'sum',
    'pricing_error_pct': 'mean'
}).round(2).sort_values('commission_earned_bwp', ascending=False)

# 4. PROPERTY TYPE ANALYSIS
property_type_stats = closed_df.groupby('property_type').agg({
    'commission_earned_bwp': 'sum',
    'commission_lost_bwp': 'sum',
    'property_id': 'count'
}).round(2)

# 5. CITY ANALYSIS
city_stats = closed_df.groupby('city').agg({
    'commission_earned_bwp': 'sum',
    'commission_lost_bwp': 'sum',
    'property_id': 'count'
}).round(2)

# 6. MONTHLY TREND - FIX: Convert Period to string
df['month'] = df['listing_date'].dt.to_period('M')
monthly_stats = df[df['deal_status'] == 'Closed'].groupby('month').agg({
    'commission_earned_bwp': 'sum',
    'property_id': 'count'
}).round(2)

# Convert Period indices to strings for JSON serialization
monthly_stats_dict = {}
for idx, row in monthly_stats.iterrows():
    monthly_stats_dict[str(idx)] = {
        'commission_earned_bwp': float(row['commission_earned_bwp']),
        'property_id': int(row['property_id'])
    }

# 7. REFERRAL SOURCE
referral_stats = closed_df.groupby('referral_source').agg({
    'property_id': 'count',
    'commission_earned_bwp': 'sum',
    'days_on_market': 'mean'
}).round(2).sort_values('property_id', ascending=False)

# 8. MACHINE LEARNING MODEL
print("\n" + "="*60)
print("TRAINING VALUATION MODEL")
print("="*60)

# Prepare data for ML
ml_df = closed_df.copy()
features = ['city', 'suburb', 'property_type', 'bedrooms', 'bathrooms', 
            'floor_area_sqm', 'plot_size_sqm', 'age_years', 'has_pool', 
            'has_garage', 'is_gated_community']

# Encode categorical features
label_encoders = {}
for col in ['city', 'suburb', 'property_type']:
    le = LabelEncoder()
    ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
    label_encoders[col] = le

# Prepare X and y
X = ml_df[[col + '_encoded' if col in ['city', 'suburb', 'property_type'] else col 
           for col in features]]
y = ml_df['true_market_value']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = model.score(X_test, y_test)

print(f"Model R²: {r2:.4f} ({r2*100:.1f}% accuracy)")
print(f"Mean Absolute Error: P{np.mean(np.abs(y_test - y_pred)):,.2f}")

# Feature importance
feature_names = [col + '_encoded' if col in ['city', 'suburb', 'property_type'] else col 
                 for col in features]
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important features:")
print(importance.head(5))

# 9. GET SAMPLE PROPERTIES FOR LISTINGS
active_sample = df[df['deal_status'] == 'Active'].head(10)
active_listings_data = []
for _, row in active_sample.iterrows():
    # Predict market value using the model
    features_encoded = []
    for col in ['city', 'suburb', 'property_type']:
        try:
            val = label_encoders[col].transform([row[col]])[0]
        except:
            val = 0
        features_encoded.append(val)
    
    for col in ['bedrooms', 'bathrooms', 'floor_area_sqm', 'plot_size_sqm', 
                'age_years', 'has_pool', 'has_garage', 'is_gated_community']:
        features_encoded.append(row[col])
    
    pred_value = model.predict([features_encoded])[0]
    
    active_listings_data.append({
        'property_id': str(row['property_id']),
        'location': f"{row['suburb']}, {row['city']}",
        'type': str(row['property_type']),
        'listed_price': float(row['listed_price']),
        'market_value': float(pred_value),
        'days_on_market': int(row['days_on_market']),
        'agent': str(row['agent']),
        'status': str(row['deal_status'])
    })

# 10. SAVE ALL DATA FOR DASHBOARD
print("\n" + "="*60)
print("SAVING DATA FOR DASHBOARD AND SAAS TOOL")
print("="*60)

# Key metrics - ensure all values are JSON serializable
key_metrics = {
    'total_properties': int(len(df)),
    'total_commission': float(total_commission),
    'total_lost': float(total_lost),
    'potential_revenue': float(potential_revenue),
    'recovery_rate': float(recovery_rate),
    'active_listings': int(active_listings),
    'avg_days_on_market': float(avg_days),
    'avg_pricing_error': float(avg_pricing_error),
    'model_r2': float(r2),
    'model_accuracy': float(r2 * 100),
    'top_agent': str(agent_stats.index[0]),
    'top_agent_commission': float(agent_stats.iloc[0]['commission_earned_bwp'])
}

# Convert agent_stats to dict with string keys
agent_stats_dict = {}
for idx, row in agent_stats.iterrows():
    agent_stats_dict[str(idx)] = {
        'property_id': int(row['property_id']),
        'commission_earned_bwp': float(row['commission_earned_bwp']),
        'commission_lost_bwp': float(row['commission_lost_bwp']),
        'pricing_error_pct': float(row['pricing_error_pct'])
    }

# Convert property_type_stats to dict with string keys
property_type_stats_dict = {}
for idx, row in property_type_stats.iterrows():
    property_type_stats_dict[str(idx)] = {
        'commission_earned_bwp': float(row['commission_earned_bwp']),
        'commission_lost_bwp': float(row['commission_lost_bwp']),
        'property_id': int(row['property_id'])
    }

# Convert city_stats to dict with string keys
city_stats_dict = {}
for idx, row in city_stats.iterrows():
    city_stats_dict[str(idx)] = {
        'commission_earned_bwp': float(row['commission_earned_bwp']),
        'commission_lost_bwp': float(row['commission_lost_bwp']),
        'property_id': int(row['property_id'])
    }

# Convert referral_stats to dict with string keys
referral_stats_dict = {}
for idx, row in referral_stats.iterrows():
    referral_stats_dict[str(idx)] = {
        'property_id': int(row['property_id']),
        'commission_earned_bwp': float(row['commission_earned_bwp']),
        'days_on_market': float(row['days_on_market'])
    }

# Save to JSON files
with open('dashboard_data.json', 'w') as f:
    json.dump({
        'metrics': key_metrics,
        'agents': agent_stats_dict,
        'property_types': property_type_stats_dict,
        'cities': city_stats_dict,
        'referrals': referral_stats_dict,
        'monthly': monthly_stats_dict,
        'active_listings': active_listings_data
    }, f, indent=2)

# Save model and encoders
joblib.dump(model, 'valuation_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

# Save reference data for SaaS tool
valuation_data = {}
for city in df['city'].unique():
    valuation_data[city] = {}
    for prop_type in df['property_type'].unique():
        subset = df[(df['city'] == city) & (df['property_type'] == prop_type) & (df['deal_status'] == 'Closed')]
        if len(subset) > 0:
            # Handle division by zero
            floor_areas = subset['floor_area_sqm'].replace(0, 1)
            sqm_rates = subset['true_market_value'] / floor_areas
            valuation_data[city][prop_type] = {
                'avg_price': float(subset['true_market_value'].mean()),
                'avg_sqm_rate': float(sqm_rates.mean()),
                'count': int(len(subset))
            }

with open('valuation_reference.json', 'w') as f:
    json.dump(valuation_data, f, indent=2)

print("✅ All data saved successfully!")
print(f"📊 Dashboard data: dashboard_data.json")
print(f"🧠 Model: valuation_model.pkl")
print(f"🔑 Encoders: label_encoders.pkl")
print(f"📈 Reference data: valuation_reference.json")

# Print some summary statistics
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print(f"Total Properties: {key_metrics['total_properties']:,}")
print(f"Total Commission Earned: P{key_metrics['total_commission']:,.2f}")
print(f"Total Commission Lost: P{key_metrics['total_lost']:,.2f}")
print(f"Potential Revenue: P{key_metrics['potential_revenue']:,.2f}")
print(f"Recovery Rate: {key_metrics['recovery_rate']:.1f}%")
print(f"Active Listings: {key_metrics['active_listings']}")
print(f"Average Days on Market: {key_metrics['avg_days_on_market']:.1f} days")
print(f"Average Pricing Error: {key_metrics['avg_pricing_error']:.1f}%")
print(f"Model R²: {key_metrics['model_r2']:.4f} ({key_metrics['model_accuracy']:.1f}% accuracy)")
print(f"Top Agent: {key_metrics['top_agent']} (P{key_metrics['top_agent_commission']:,.2f})")
print("\n" + "="*60)