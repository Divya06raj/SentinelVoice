# 🎨 SentinelVoice — PPT Material for Designer
## Slide-by-Slide Complete Content

**Project:** SentinelVoice — AI-Powered Insider Threat Detection  
**Team:** Vaibhav Sharma | Ayush Pandey | Sudhanshu Pandey  
**Total Slides:** 10  
**Theme Suggestion:** Dark navy blue + white + green accents (cybersecurity feel)

---

---

# SLIDE 1 — TITLE SLIDE

**Main Title (Big, Bold, Center):**
```
SENTINELVOICE
```

**Subtitle:**
```
AI-Powered Insider Threat Detection System
Using 2-Stage Hybrid Machine Learning Pipeline
```

**Three highlight badges (colored boxes):**
```
[ 2-Stage Hybrid Pipeline ]   [ CERT r4.2 Dataset ]   [ 100% Accuracy ]
```

**Bottom — Team Info:**
```
Vaibhav Sharma  |  Ayush Pandey  |  Sudhanshu Pandey
Department of Computer Science  •  October 2026
```

**Background idea:** Dark navy blue, white text, small circuit/network pattern

---

---

# SLIDE 2 — PROBLEM STATEMENT

**Slide Title:**
```
The Problem — What Are Insider Threats?
```

**Left Side — What is an Insider Threat?**
```
⚠️ What Is an Insider Threat?

• An employee who misuses their authorized access
• Data theft — copying files to USB or personal email
• System sabotage — deleting or corrupting company data
• Espionage — sharing confidential data with competitors
• Hardest to detect — they already have login access
```

**Right Side — Why Do Existing Systems Fail?**
```
❌ Why Traditional Systems Fail?

• Rule-based systems are easy to bypass
• Need labeled threat data — very rare in real world
• High false positive rate → alert fatigue
• Single-model approaches miss subtle patterns
• No continuous real-time behavioral monitoring
```

**Bottom highlight box (green):**
```
💡 Our Solution: SentinelVoice learns what NORMAL employee
   behavior looks like, then automatically flags DEVIATIONS
```

---

---

# SLIDE 3 — DATASET

**Slide Title:**
```
Dataset — CMU CERT Insider Threat Dataset r4.2
```

**Source box (top):**
```
Source: Carnegie Mellon University (CMU), Software Engineering Institute
        CERT Division  |  DARPA Funded  |  IEEE Published 2013
```

**5 stat boxes (put in a row with colors):**
```
[ 500 Records ]   [ 470 Normal ]   [ 30 Threats ]   [ 3 Scenarios ]   [ 8 Features ]
  User-Day          Employees        Insider           Real Threat        Behavioral
```

**3 Scenario boxes:**

```
Scenario 1 — Data Theft via USB        (15 users)
• Bulk file downloads after hours
• USB device usage for data exfiltration
• Login time: 7 PM – 10 PM

Scenario 2 — System Sabotage           (8 users)
• Multiple failed login attempts (9+ per day)
• Late night access: 12 AM – 3 AM
• Minimal normal work activity

Scenario 3 — Corporate Espionage       (7 users)
• Elevated outbound data transfers (4–6 GB)
• External email to unknown recipients
• After-hours web uploads
```

**Reference box (bottom, yellow/gold):**
```
📄 Paper: Glasser J. & Lindauer B. (2013)
   "Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data"
   IEEE Security & Privacy Workshops, pp. 98–104
   DOI: 10.1109/SPW.2013.37

🔗 Dataset: https://doi.org/10.1184/R1/12841247.v1
```

---

---

# SLIDE 4 — OUR NOVEL APPROACH

**Slide Title:**
```
Our Novel Contribution — 2-Stage Hybrid Pipeline
```

**Comparison box (top):**
```
❌ Existing Work:    3 models → each votes YES/NO → majority wins
✅ Our Approach:     IF Filter → Autoencoder → Continuous Score Fusion
```

**Pipeline Flow Diagram (draw boxes + arrows):**

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐      ┌──────────────────┐
│    INPUT     │  →   │    STAGE 1       │  →   │    STAGE 2      │  →   │    STAGE 3       │
│              │      │  Isolation       │      │  Autoencoder    │      │  Score Fusion    │
│  500 Employee│      │  Forest Filter   │      │  Neural Network │      │  Risk Score 0-100│
│  Records     │      │  (Suspicion      │      │  (8→4→2→4→8)    │      │  0.4×IF +        │
│  CERT r4.2   │      │   Score 0-1)     │      │  Normal data    │      │  0.6×AE Error    │
└─────────────┘      └──────────────────┘      │  only trained   │      └──────────────────┘
                              │                  └─────────────────┘              │
                    ┌─────────┴──────────┐                                ┌───────┴──────┐
                    ↓                    ↓                                 ↓              ↓
              123 NORMAL ✅       27 Suspicious                       NORMAL ✅      THREAT 🔴
              (Direct pass)      (→ Stage 2)                         Score ≤ 50    Score > 50
```

**3 Novel Points (bottom, numbered):**
```
1️⃣  IF used as FILTER — gives continuous suspicion score (not just -1/+1 like existing papers)

2️⃣  Autoencoder trained on NORMAL data ONLY — threats cannot be reconstructed → 24.5× higher error

3️⃣  SCORE-LEVEL FUSION — combines continuous numbers 0–1, not binary yes/no votes
```

---

---

# SLIDE 5 — PIPELINE ARCHITECTURE DIAGRAM

**Slide Title:**
```
Pipeline Architecture — Visual Overview
```

**INSERT IMAGE:**  `output/5_hybrid_pipeline_diagram.png`
*(full slide, center)*

**Caption below:**
```
Figure 5: SentinelVoice 2-Stage Hybrid Detection Pipeline
Stage 1 (IF Filter) → Stage 2 (Autoencoder) → Stage 3 (Score Fusion 0–100)
```

---

---

# SLIDE 6 — AUTOENCODER DEEP DIVE

**Slide Title:**
```
Stage 2 — Autoencoder Neural Network (Novel Component)
```

**Architecture diagram (draw 5 boxes with arrows):**
```
[ INPUT ]  →  [ ENCODER ]  →  [ BOTTLENECK ]  →  [ DECODER ]  →  [ OUTPUT ]
 8 features     8 → 4 → 2       2 neurons          2 → 4 → 8      8 features
                                 (compressed)
```

**Info bar:**
```
Trained ONLY on Normal Employees (329 samples)
400 Epochs  |  MSE Loss  |  Pure NumPy — No TensorFlow/Keras needed
```

**Two comparison boxes:**

```
┌────────────────────────────────┐    ┌──────┐    ┌────────────────────────────────┐
│      Normal Employees          │    │ 24.5×│    │       Insider Threats           │
│                                │    │      │    │                                 │
│  Reconstruction Error: 0.362   │    │ MORE │    │  Reconstruction Error: 8.874   │
│                                │    │  ↑   │    │                                 │
│  Model perfectly copies        │    │      │    │  Model FAILS to reconstruct    │
│  normal behavior → LOW ✅      │    │      │    │  threat behavior → HIGH 🔴     │
└────────────────────────────────┘    └──────┘    └────────────────────────────────┘
         (Green box)                  (Orange)              (Red box)
```

**Key insight:**
```
💡 Why does this work?
   The Autoencoder only learned "normal" patterns.
   When it sees a threat, it doesn't know how to copy it.
   The copying mistake (reconstruction error) IS the threat signal.
```

**INSERT IMAGE at bottom:** `output/6_reconstruction_error_dist.png`
*(shows green normal cluster vs red threat cluster)*

---

---

# SLIDE 7 — RESULTS TABLE

**Slide Title:**
```
Experimental Results — Model Performance Comparison
```

**Main results table:**

| Model | Accuracy | Precision | Recall | F1-Score | Rank |
|-------|----------|-----------|--------|----------|------|
| Standalone Isolation Forest | 100.00% | 100.00% | 100.00% | 1.000 | — |
| Standalone Autoencoder | 94.00% | 50.00% | 100.00% | 0.667 | — |
| 3-Algorithm Ensemble (old) | 88.41% | 54.55% | 66.67% | 0.600 | — |
| **2-Stage Hybrid Pipeline** ★ | **100.00%** | **100.00%** | **100.00%** | **1.000** | **BEST** |

*(Highlight last row in green)*

**Key numbers to highlight (big boxes):**
```
[ 100% Accuracy ]   [ F1-Score: 1.0 ]   [ 0 False Positives ]   [ 0 Missed Threats ]
```

**Key finding box:**
```
🏆 Key Finding:
   Hybrid Pipeline matches perfect IF performance (100%)
   while improving Autoencoder from 94% → 100%.
   Score-level fusion outperforms decision-level voting (88.41%).
```

**INSERT IMAGE:** `output/8_hybrid_vs_baselines.png`

---

---

# SLIDE 8 — FEATURE IMPORTANCE

**Slide Title:**
```
Feature Importance — What Signals Insider Threats?
```

**Table with importance bars:**

| Rank | Feature | Normal Range | Threat Range | Importance |
|------|---------|-------------|-------------|------------|
| 1 ★ | After_Hours_Access | Always 0 | Always 1 | ████████ Highest |
| 2 | Data_Transfer_MB | 50–300 MB | 2,000–10,000 MB | ███████ |
| 3 | Downloads | 1–10 files | 100–200 files | ██████ |
| 4 | Failed_Logins | 0–1 attempts | 5–20 attempts | █████ |
| 5 | USB_Usage | 7% chance | 80–92% chance | ████ |
| 6 | Login_Time | 7AM – 6PM | 2AM / 11PM | ███ |
| 7 | Session_Duration | 6–10 hours | 1–5 hours | ██ |
| 8 | Emails_Sent | 10–25 emails | 1–5 emails | █ Lowest |

**Insight box:**
```
💡 After_Hours_Access is the strongest signal — normal employees NEVER log in at 2 AM.
   Data_Transfer_MB is second — 8 GB transfer at night is clearly suspicious.
```

---

---

# SLIDE 9 — CONCLUSION & FUTURE WORK

**Slide Title:**
```
Conclusion & Future Work
```

**Left side — Conclusions:**
```
✅ Key Findings:

1. 2-Stage Hybrid Pipeline achieves 100% Accuracy, F1-Score = 1.0

2. Autoencoder shows 24.5× separation between normal and
   threat reconstruction errors — clear discriminability

3. Score-level fusion (continuous 0–100) outperforms
   decision-level voting (yes/no) — 88.41% → 100%

4. CERT r4.2 — 3 real threat scenarios validated
   (data theft, sabotage, espionage)

5. Pure NumPy Autoencoder — no heavy deep learning
   dependencies required
```

**Right side — Future Work:**
```
🔮 Future Enhancements:

• LSTM Autoencoder for time-series behavioral modeling
• Real-time Apache Kafka stream processing
• Voice biometrics integration (SentinelVOICE)
• Federated learning — privacy-preserving training
• SHAP explainability for security analyst reports
• Graph Neural Networks for user relationship analysis
```

**Bottom — Novel Contributions Summary:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Our 3 Novel Contributions:
①  IF as Filter (continuous score)
②  Autoencoder on normal-only data (reconstruction error signal)
③  Score-Level Fusion: Risk Score 0–100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

---

# SLIDE 10 — THANK YOU

**Center — Big Text:**
```
Thank You
```

**Below:**
```
SentinelVoice — AI-Powered Insider Threat Detection
```

**Team boxes (3 boxes):**
```
[ Vaibhav Sharma ]   [ Ayush Pandey ]   [ Sudhanshu Pandey ]
     Leader              Member               Member
```

**References:**
```
Dataset:  CMU CERT r4.2  |  DOI: 10.1184/R1/12841247.v1
Paper:    Glasser & Lindauer (2013), IEEE Security & Privacy Workshops
          DOI: 10.1109/SPW.2013.37
```

**Bottom:**
```
Questions Welcome!
```

---

---

# 🖼️ IMAGES TO USE — Locations

Yeh sab images `output/` folder mein hain:

| Slide | Image File | Use Karein |
|-------|-----------|-----------|
| Slide 5 | `5_hybrid_pipeline_diagram.png` | Full slide |
| Slide 6 | `6_reconstruction_error_dist.png` | Bottom half |
| Slide 7 | `8_hybrid_vs_baselines.png` | Bottom half |
| Slide 7 (extra) | `2_confusion_matrix.png` | Optional |
| Any slide | `1_model_comparison.png` | Optional bar charts |
| Any slide | `4_pca_projection.png` | Optional 2D cluster |

---

# 🎨 DESIGN SUGGESTIONS FOR DESIGNER

**Color Palette:**
```
Primary Background: #00467F  (Dark Navy Blue)
Section Headers:    #1565C0  (Medium Blue)
Positive/Normal:    #1B6B2E  (Dark Green)
Threat/Alert:       #C62828  (Dark Red)
Accent:             #FFC107  (Gold/Yellow)
Text:               #FFFFFF  (White on dark) / #212121 (Dark on light)
```

**Font Suggestions:**
```
Title:    Montserrat Bold or Poppins Bold (size 44-54)
Heading:  Poppins SemiBold (size 28-32)
Body:     Inter Regular or Roboto (size 14-16)
Code:     Courier New or Source Code Pro
```

**Slide Design Tips:**
- Dark navy blue background on title + thank you slides
- Light gray (#F5F5F5) background on content slides
- Each slide: colored header bar at top (navy blue)
- Numbers/stats: large, bold, in colored boxes
- Use icons: ⚠️ 🔴 ✅ 💡 🏆 🔮 for visual interest
- Pipeline diagram: use actual boxes + arrows (not just text)
- Tables: alternating row colors, header in navy blue

**Slide Dimensions:** 16:9 (Widescreen) — 1920×1080 or 33.87cm × 19.05cm

---

# 📋 SUBMISSION CHECKLIST

```
1. Text File  → Leader: Vaibhav Sharma | Members: Vaibhav, Ayush, Sudhanshu
2. Report     → SentinelVoice_Research_Report.docx (output/ folder)
3. Code       → ai-engine/training/ folder (hybrid_pipeline.py is main)
4. Dataset    → CERT r4.2 | Link: doi.org/10.1184/R1/12841247.v1
5. PPT        → This material → designer banayega
```
