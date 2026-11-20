"""
SentinelVoice - Model Training Script
Train Isolation Forest model for anomaly detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pickle
import os
from datetime import datetime

print("=" * 60)
print("🧠 SENTINELVOICE - MODEL TRAINING STARTED")
print("=" * 60)

# ============================================
# STEP 1: Load Training Data
# ============================================
print("\n📦 Step 1: Generating 1 Lakh Synthetic Records...")

    # Hum 99,000 normal employees aur 1,000 hackers ka data banayenge
n_normal = 99000
n_threats = 1000

    # 1. Normal Employees ka Data (Subah ka time, kam downloads)
normal_data = {
        'Login_Time': np.random.randint(9, 18, n_normal),         # 9 AM se 6 PM
        'Downloads': np.random.randint(1, 15, n_normal),          # 1 se 14 files
        'Failed_Logins': np.random.randint(0, 2, n_normal),       # 0 ya 1 fail
        'Data_Transfer_MB': np.random.uniform(10, 150, n_normal)  # 10MB se 150MB
    }
df_normal = pd.DataFrame(normal_data)

    # 2. Hackers/Threats ka Data (Raat ka time, massive downloads)
threat_data = {
        'Login_Time': np.random.choice([1, 2, 3, 22, 23], n_threats), # Raat 10 baje se 3 baje tak
        'Downloads': np.random.randint(1000, 5000, n_threats),        # 1000+ files
        'Failed_Logins': np.random.randint(5, 20, n_threats),         # Bahut saare wrong passwords
        'Data_Transfer_MB': np.random.uniform(5000, 10000, n_threats) # 5GB se 10GB transfer
    }
df_threats = pd.DataFrame(threat_data)

    # 3. Dono data ko mix (combine) karna aur shuffle (upar-neeche) karna
df = pd.concat([df_normal, df_threats]).sample(frac=1).reset_index(drop=True)

print(f"✅ Data loaded successfully! Total records: {len(df)}")
print("\nData Preview:")
print(df.head())

# ============================================
# STEP 2: Data Preprocessing
# ============================================
print("\n⚙️ Step 2: Preprocessing Data...")

# Feature columns ko select karna
features = df[['Login_Time', 'Downloads', 'Failed_Logins', 'Data_Transfer_MB']]

# Data ko normalize karna (scaling) - Yeh zaroori hai taaki model sahi se seekhe
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

print("✅ Data normalized successfully!")
print(f"Shape after scaling: {features_scaled.shape}")

# ============================================
# STEP 3: Model Training
# ============================================
print("\n🧠 Step 3: Training Isolation Forest Model...")

# Isolation Forest model banate hain
# Isolation Forest model banate hain
model = IsolationForest(
    contamination=0.01,  # <-- Isey 0.18 se 0.01 kar do (1% threats)
    random_state=42,
    n_estimators=100
)
# MODEL TRAINING - Yahan actual training hoti hai
model.fit(features_scaled)

print("✅ Model trained successfully!")

# ============================================
# STEP 4: Predictions
# ============================================
print("\n🔍 Step 4: Making Predictions...")

# Model se predictions le rahe hain
predictions = model.predict(features_scaled)
anomaly_scores = model.score_samples(features_scaled)

# Results ko dataframe mein add karna
df['Prediction'] = predictions
df['Anomaly_Score'] = anomaly_scores
df['Status'] = df['Prediction'].apply(lambda x: '🔴 THREAT' if x == -1 else '🟢 NORMAL')

print("\n" + "=" * 60)
print("📊 PREDICTION RESULTS")
print("=" * 60)
print(df[['Login_Time', 'Downloads', 'Status', 'Anomaly_Score']])


# ============================================
# STEP 5: Visualization
# ============================================
print("\n📈 Step 5: Creating Visualization...")

plt.figure(figsize=(12, 6))

# Normal vs Anomaly plot
normal = df[df['Prediction'] == 1]
anomaly = df[df['Prediction'] == -1]

# 1. Normal data mein thoda 'jitter' (spread) add kiya taaki 99,000 dots ka cloud dikhe
# 2. Marker size (s) ko chota kiya (Normal=10, Threat=30)
plt.scatter(normal['Login_Time'] + np.random.uniform(-0.3, 0.3, len(normal)), 
            normal['Downloads'] + np.random.uniform(-0.4, 0.4, len(normal)), 
            c='green', label='Normal', s=10, alpha=0.4)

plt.scatter(anomaly['Login_Time'], anomaly['Downloads'], 
            c='red', label='Threat Detected', s=30, alpha=0.8, edgecolors='black', marker='X')

plt.xlabel('Login Time (Hour)', fontsize=12)
plt.ylabel('Downloads (Files)', fontsize=12)
plt.title('SentinelVoice - Anomaly Detection Results', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Save plot
output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)
plot_path = os.path.join(output_dir, 'anomaly_detection_plot.png')
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"✅ Plot saved: {plot_path}")

# ============================================
# STEP 6: Save Trained Model
# ============================================
print("\n💾 Step 6: Saving Trained Model...")

model_path = os.path.join(output_dir, 'isolation_forest_model.pkl')
scaler_path = os.path.join(output_dir, 'scaler.pkl')

# Model aur scaler dono save karna zaroori hai
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Model saved: {model_path}")
print(f"✅ Scaler saved: {scaler_path}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("📋 TRAINING SUMMARY")
print("=" * 60)
print(f"Total Records: {len(df)}")
print(f"Normal Activities: {len(normal)}")
print(f"Threats Detected: {len(anomaly)}")
print(f"Accuracy: {(len(normal) / len(df)) * 100:.2f}% Normal Rate")
print("\n✅ Model training completed successfully!")
print("=" * 60)

# Show plot
plt.show()
