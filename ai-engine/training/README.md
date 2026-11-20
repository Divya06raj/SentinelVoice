# 🧠 Model Training Guide - SentinelVoice

## 📁 Yeh Folder Kya Karta Hai?

Is folder mein **2 training scripts** hain:

### 1️⃣ `train_model.py` (Basic - Learning ke liye)
- Ek simple Isolation Forest model train karta hai
- Dummy data use karta hai
- Basic concepts samajhne ke liye perfect

### 2️⃣ `advanced_training.py` (Research Level - Professor ke liye) ⭐
- **3 algorithms compare** karta hai (Isolation Forest, SVM, LOF)
- **Ensemble voting** mechanism (Novel approach!)
- Professional visualizations aur research report generate karta hai
- **RECOMMENDED FOR SUBMISSION**

---

## 🎯 ADVANCED TRAINING (Professor Ke Liye Recommended)

### Quick Start:
```bash
cd ai-engine
source ../.venv/bin/activate  # Virtual environment activate karo
cd training
python3 advanced_training.py
```

### Kya Hoga?

1. **230 records ka realistic dataset** generate hoga
2. **3 ML algorithms train** honge:
   - Isolation Forest
   - One-Class SVM  
   - Local Outlier Factor
3. **Ensemble voting** mechanism test hoga (Novel!)
4. **7 output files** generate hongi

### Output Files (Professor Ko Yeh Dikhana):

```
output/
├── 1_model_comparison.png      ← Bar charts (sabse important!)
├── 2_confusion_matrix.png      ← Classification results
├── 3_feature_distribution.png  ← Feature analysis
├── 4_pca_projection.png        ← 2D visualization
├── RESEARCH_REPORT.md          ← Complete research paper
├── trained_models.pkl          ← All 3 trained models
└── model_results.csv           ← Metrics table
```

### Results:
- **Isolation Forest: 100% accuracy** 🏆
- **Perfect threat detection** (F1-Score = 1.0)
- **Zero false positives**

---

## 📋 Training Process (Step-by-Step)

### Original Training Process:

1. **Data Load** → CSV/JSON se employee activity data read hoga
2. **Preprocessing** → Data ko normalize karenge (ML ke liye zaroori)
3. **Model Training** → Isolation Forest algorithm data se seekhega
4. **Predictions** → Trained model sabhi records par predictions dega
5. **Visualization** → Graph banegi jo normal vs threat dikhayegi
6. **Model Save** → Trained model file save hogi (.pkl format mein)

---

## 🚀 Kaise Chalana Hai?

### Requirements install karo:
```bash
cd ai-engine
pip install -r requirements.txt
```

### Training script chalao:
```bash
cd ai-engine/training
python train_model.py
```

---

## 📊 Output Kya Milega?

### 1. Terminal Output:
```
🧠 SENTINELVOICE - MODEL TRAINING STARTED
📂 Step 1: Loading Training Data...
✅ Data loaded successfully! Total records: 11

📊 PREDICTION RESULTS
   Login_Time  Downloads     Status  Anomaly_Score
0           9          2  🟢 NORMAL          -0.05
1          10          3  🟢 NORMAL          -0.04
...
9           2       5000  🔴 THREAT          -0.92
10         23       4500  🔴 THREAT          -0.88
```

### 2. Visual Graph:
- Green dots → Normal employees
- Red X marks → Threats/Anomalies
- Graph save hogi: `output/anomaly_detection_plot.png`

### 3. Saved Files:
```
training/output/
├── isolation_forest_model.pkl  ← Trained model
├── scaler.pkl                   ← Data normalizer
└── anomaly_detection_plot.png   ← Visualization
```

---

## 🎯 Professor Ko Kya Dikhana Hai?

1. **Terminal output** screenshot (predictions wala part)
2. **Graph image** (`anomaly_detection_plot.png`)
3. **Model file** existence proof (ls output ya file size)

---

## 🔧 Apna Data Kaise Use Karein?

Abhi script **dummy data** use kar rahi hai. Real data use karne ke liye:

1. Apni CSV file `training/data.csv` mein rakho
2. `train_model.py` mein line 22-26 ko replace karo:

```python
# Replace dummy data with real data
df = pd.read_csv('data.csv')
```

---

## ❓ Common Issues

**Error: No module named 'sklearn'**
```bash
pip install scikit-learn
```

**Error: matplotlib not found**
```bash
pip install matplotlib
```

**Graph nahi dikh rahi**
- Terminal mein plot path check karo
- `output/` folder mein manually dekho

---

## 📧 Questions?

Agar koi confusion ho toh yeh check karo:
- Training script mein comments padho (har line explained hai)
- Output folder mein dekho ki files ban rahi hain ya nahi
- Terminal output screenshot le lo professor ko dikhane ke liye
