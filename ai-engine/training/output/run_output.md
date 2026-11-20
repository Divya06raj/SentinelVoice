# SentinelVoice — Training Run Output

**Run Date:** 2026-10-29 11:24:53

---

## Full Terminal Output — `advanced_training.py`

```
================================================================================
🎓 SENTINELVOICE - ADVANCED MODEL TRAINING & RESEARCH
================================================================================
Training Started: 2026-10-29 11:24:53
================================================================================
📊 STEP 1: Generating Realistic Dataset...
--------------------------------------------------------------------------------
ℹ  CERT r4.2 CSV not found on disk.
   Loading CERT r4.2 statistically-derived benchmark data...
   (Based on Glasser & Lindauer 2013, Table II & III)
   To use real CSV: place cert_r4.2.csv in training/data/
📌 Data Source : CERT r4.2 Statistically-Derived Benchmark (Glasser & Lindauer 2013)
✅ Dataset Loaded:
   - Total Records   : 500
   - Normal Employees: 470
   - Insider Threats : 30
   - Threat Ratio    : 6.00%
   - Feature Dims    : 8
📋 Sample Data (first 10 rows):
   Login_Time  Session_Duration_Hours  Downloads  Failed_Logins  Data_Transfer_MB  Emails_Sent  USB_Usage  After_Hours_Access  Label
0    9.499084                9.709340          2              0         85.996208           18          0                   0    1.0
1    9.656082                7.603136          3              0        145.969477            9          0                   0    1.0
2    9.734681                7.978580          1              1         49.995583           11          0                   0    1.0
3   11.409743                7.174523          7              0        281.498330           19          0                   0    1.0
4    7.681608                8.049711          4              0         90.377571           17          0                   0    1.0
5    9.938696                6.980858          6              0         15.422369           12          0                   0    1.0
6    6.205139                8.850056          4              0         63.894175           19          0                   0    1.0
7   10.122454                6.269906          4              0        172.148825           13          0                   0    1.0
8   10.154007                4.922945          5              1         96.488327           15          0                   0    1.0
9    8.789030                7.435333          2              0         24.026281           14          0                   0    1.0
📈 Statistical Summary:
       Login_Time  Session_Duration_Hours  Downloads  Failed_Logins  Data_Transfer_MB  Emails_Sent  USB_Usage  After_Hours_Access    Label
count     500.000                 500.000    500.000        500.000           500.000      500.000    500.000             500.000  500.000
mean        9.375                   7.427      9.516          0.612           407.576       13.326      0.088               0.094    0.880
std         2.901                   1.786     24.475          1.642          1288.521        4.254      0.284               0.292    0.475
min         0.485                   0.558      0.000          0.000            11.069        0.000      0.000               0.000   -1.000
25%         8.041                   6.726      3.000          0.000            54.072       11.000      0.000               0.000    1.000
50%         9.044                   7.705      4.000          0.000            94.555       13.000      0.000               0.000    1.000
75%         9.981                   8.477      6.000          1.000           170.732       16.000      0.000               0.000    1.000
max        23.521                  11.666    151.000         17.000          8861.885       24.000      1.000               1.000    1.000
⚙ STEP 2: Feature Engineering & Preprocessing...
--------------------------------------------------------------------------------
✅ Data Split:
   - Training Set: 350 samples (329 normal, 21 threats)
   - Testing Set : 150 samples (141 normal, 9 threats)
✅ Data Normalized (StandardScaler)
🧠 STEP 3: Training Multiple Anomaly Detection Models...
--------------------------------------------------------------------------------
[1/3] Training Isolation Forest...
✅ Isolation Forest trained
[2/3] Training One-Class SVM...
✅ One-Class SVM trained
[3/3] Training Local Outlier Factor...
✅ Local Outlier Factor trained
🗳 STEP 4: Ensemble Voting Mechanism...
--------------------------------------------------------------------------------
Novel Approach: Combining predictions from all 3 models using majority voting
✅ Ensemble model created using majority voting
📊 STEP 5: Model Evaluation & Comparison...
--------------------------------------------------------------------------------
================================================================================
📈 MODEL COMPARISON RESULTS
================================================================================
               Model  Accuracy  Precision  Recall  F1-Score
    Isolation Forest  0.920000   0.428571     1.0   0.60000
       One-Class SVM  0.920000   0.428571     1.0   0.60000
Local Outlier Factor  0.960000   0.600000     1.0   0.75000
 🏆 Ensemble (Voting)  0.926667   0.450000     1.0   0.62069
================================================================================
🏆 BEST MODEL: Local Outlier Factor
   F1-Score: 0.7500
📉 STEP 6: Generating Visualizations & Analysis...
--------------------------------------------------------------------------------
✅ Saved: 1_model_comparison.png
✅ Saved: 2_confusion_matrix.png
✅ Saved: 3_feature_distribution.png
✅ Saved: 4_pca_projection.png
💾 STEP 7: Saving Trained Models & Artifacts...
--------------------------------------------------------------------------------
✅ All models saved: trained_models.pkl
✅ Results saved: model_results.csv
📄 STEP 8: Generating Research Report...
--------------------------------------------------------------------------------
✅ Research report saved: RESEARCH_REPORT.md
================================================================================
✅ TRAINING COMPLETED SUCCESSFULLY!
================================================================================
📁 OUTPUT FILES:
   1. trained_models.pkl       - All trained models
   2. model_results.csv         - Comparison metrics
   3. RESEARCH_REPORT.md        - Detailed report
   4. 1_model_comparison.png    - Performance charts
   5. 2_confusion_matrix.png    - Confusion matrix
   6. 3_feature_distribution.png - Feature analysis
   7. 4_pca_projection.png      - 2D visualization
🎯 NEXT STEPS:
   1. Review RESEARCH_REPORT.md for detailed findings
   2. Analyze visualizations in output/ folder
   3. Present results to professor
================================================================================
🎓 Thank you for using SentinelVoice Research Framework!
================================================================================
📄 Generating Word Document...
✅  Word document saved successfully!
📄  Path: .../output/SentinelVoice_Research_Report.docx
📦  Size: 886 KB
```

---

## MODEL COMPARISON RESULTS Table

| Model                | Accuracy | Precision | Recall | F1-Score |
|----------------------|----------|-----------|--------|----------|
| Isolation Forest     | 0.9200   | 0.4286    | 1.0000 | 0.6000   |
| One-Class SVM        | 0.9200   | 0.4286    | 1.0000 | 0.6000   |
| Local Outlier Factor | 0.9600   | 0.6000    | 1.0000 | 0.7500   |
| 🏆 Ensemble (Voting)  | 0.9267   | 0.4500    | 1.0000 | 0.6207   |

**Best Model:** Local Outlier Factor — F1-Score: 0.7500

---

## model_results.csv Contents

| Model                | Accuracy   | Precision          | Recall | F1-Score           |
|----------------------|------------|--------------------|--------|--------------------|
| Isolation Forest     | 0.92       | 0.42857142857142855 | 1.0    | 0.6                |
| One-Class SVM        | 0.92       | 0.42857142857142855 | 1.0    | 0.6                |
| Local Outlier Factor | 0.96       | 0.6                | 1.0    | 0.75               |
| 🏆 Ensemble (Voting)  | 0.9266666666666666 | 0.45     | 1.0    | 0.6206896551724138 |

---

## Verification Checklist

| File                             | Status |
|----------------------------------|--------|
| `1_model_comparison.png`         | ✅     |
| `2_confusion_matrix.png`         | ✅     |
| `3_feature_distribution.png`     | ✅     |
| `4_pca_projection.png`           | ✅     |
| `RESEARCH_REPORT.md`             | ✅     |
| `SentinelVoice_Research_Report.docx` | ✅ |
| `trained_models.pkl`             | ✅     |
| `model_results.csv`              | ✅     |

All 8 expected output files are present. ✅

---

## File Sizes

| File                             | Size   |
|----------------------------------|--------|
| `SentinelVoice_Research_Report.docx` | 886 KB |
| `trained_models.pkl`             | 1.8 MB |
| `1_model_comparison.png`         | 367 KB |
| `2_confusion_matrix.png`         | 74 KB  |
| `3_feature_distribution.png`     | 373 KB |
| `4_pca_projection.png`           | 236 KB |
| `RESEARCH_REPORT.md`             | 2.3 KB |
| `model_results.csv`              | 247 B  |
