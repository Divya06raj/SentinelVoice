# 🛡️ SentinelVoice — AI-Powered Insider Threat Detection

> **Research Project | Department of Computer Science | October 2026**

[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://python.org)
[![ML](https://img.shields.io/badge/ML-Isolation%20Forest%20%2B%20Autoencoder-green)](https://scikit-learn.org)
[![Dataset](https://img.shields.io/badge/Dataset-CMU%20CERT%20r4.2-orange)](https://doi.org/10.1184/R1/12841247.v1)
[![Accuracy](https://img.shields.io/badge/Accuracy-100%25-brightgreen)](https://github.com/Divya06raj/SentinelVoice)

---

## 👥 Team

| Name | Role |
|------|------|
| Vaibhav Sharma | Leader |
| Ayush Pandey | Member |
| Sudhanshu Pandey | Member |

---

## 🎯 What Is This Project?

SentinelVoice is an AI system that monitors employee activity logs and automatically detects **insider threats** — employees who steal data, sabotage systems, or leak confidential information.

**Problem:** Traditional rule-based systems cannot detect insiders because they already have authorized access.

**Our Solution:** Machine learning that learns what *normal* employee behavior looks like, then flags deviations as potential threats.

---

## 🔬 Novel Contribution — 2-Stage Hybrid Pipeline

Unlike existing work that simply compares algorithms, we built a genuinely novel architecture:

```
500 Employee Records (CERT r4.2)
        │
        ▼
┌─────────────────────┐
│  STAGE 1            │  ← Isolation Forest as FILTER
│  IF Filter          │    (continuous suspicion score, not -1/+1)
└─────────────────────┘
        │              │
   123 NORMAL ✅    27 Suspicious
   (Direct pass)       │
                        ▼
               ┌─────────────────────┐
               │  STAGE 2            │  ← Autoencoder Neural Network
               │  Autoencoder        │    trained on NORMAL data only
               │  8→4→2→4→8         │    pure NumPy, no TensorFlow
               └─────────────────────┘
                        │
                        ▼
               ┌─────────────────────┐
               │  STAGE 3            │  ← Score-Level Fusion (NOVEL)
               │  Risk Score 0-100   │    0.4×IF + 0.6×AE_error
               └─────────────────────┘
                        │
              ┌─────────┴──────────┐
           NORMAL ✅           THREAT 🔴
```

### Why Is This Novel?
1. **IF as Filter** — existing papers use IF as final classifier. We use it as a filter giving continuous scores.
2. **Autoencoder on normal-only data** — threats cannot be reconstructed (24.5× higher error than normal).
3. **Score-Level Fusion** — combines continuous numbers 0–1, not binary yes/no votes like existing work.

---

## 📊 Results

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Standalone Isolation Forest | 100.00% | 100.00% | 100.00% | 1.000 |
| Standalone Autoencoder | 94.00% | 50.00% | 100.00% | 0.667 |
| 3-Algorithm Ensemble (old) | 88.41% | 54.55% | 66.67% | 0.600 |
| **2-Stage Hybrid Pipeline ★** | **100.00%** | **100.00%** | **100.00%** | **1.000** |

**Key Finding:** Autoencoder reconstruction error separation = **24.5×** (normal: 0.362 vs threat: 8.874)

---

## 📂 Dataset

**CMU CERT Insider Threat Dataset v4.2**
- Publisher: Carnegie Mellon University, Software Engineering Institute
- Paper: Glasser & Lindauer (2013), IEEE Security & Privacy Workshops, pp. 98–104
- DOI: https://doi.org/10.1109/SPW.2013.37
- Download: https://doi.org/10.1184/R1/12841247.v1

**500 records | 470 normal | 30 threats | 3 real scenarios | 8 features**

---

## 🚀 How To Run

```bash
# 1. Clone the repo
git clone https://github.com/Divya06raj/SentinelVoice.git
cd SentinelVoice

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r ai-engine/requirements.txt

# 4. Run the novel hybrid pipeline
cd ai-engine/training
python3 hybrid_pipeline.py

# 5. Generate Word report
python3 generate_report.py

# 6. Generate PPT
python3 make_ppt.py
```

---

## 📁 Project Structure

```
SentinelVoice/
├── frontend/                          ← React.js Web Interface
│   └── src/components/
│       ├── Dashboard.js
│       ├── LoginPage.js
│       └── ModelStats.js
├── backend/                           ← Node.js + Express API
│   ├── routes/
│   └── engine/anomalyDetector.js
└── ai-engine/
    └── training/
        ├── hybrid_pipeline.py         ← ⭐ MAIN: Novel 2-Stage Pipeline
        ├── advanced_training.py       ← 3-model comparison
        ├── generate_report.py         ← Auto Word doc generator
        ├── make_ppt.py                ← PPT generator
        ├── PPT_MATERIAL_FOR_DESIGNER.md
        └── output/
            ├── SentinelVoice_Research_Report.docx
            ├── SentinelVoice_Presentation.pptx
            ├── 5_hybrid_pipeline_diagram.png
            ├── 6_reconstruction_error_dist.png
            └── 8_hybrid_vs_baselines.png
```

---

## 📈 Output Visualizations

| File | Description |
|------|-------------|
| `1_model_comparison.png` | 4 metrics bar chart for all models |
| `2_confusion_matrix.png` | Perfect classification matrix |
| `5_hybrid_pipeline_diagram.png` | Pipeline architecture diagram |
| `6_reconstruction_error_dist.png` | Normal vs Threat AE error distribution |
| `8_hybrid_vs_baselines.png` | Hybrid vs standalone model comparison |

---

## 📚 References

1. Glasser, J. & Lindauer, B. (2013). *Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data.* IEEE SPW. DOI: 10.1109/SPW.2013.37
2. Liu, F.T. et al. (2008). *Isolation Forest.* ICDM 2008.
3. Schölkopf, B. et al. (2001). *One-Class SVM.* Neural Computation.
4. Breunig, M.M. et al. (2000). *LOF.* ACM SIGMOD.
5. Pedregosa, F. et al. (2011). *Scikit-learn.* JMLR 12.
