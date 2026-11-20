# 📂 Dataset Reference — SentinelVoice Project

---

## Dataset Name

**CERT Insider Threat Test Dataset, Release 4.2 (r4.2)**

---

## Publisher / Source

| Field | Details |
|-------|---------|
| **Organization** | Carnegie Mellon University (CMU) |
| **Department** | Software Engineering Institute (SEI), CERT Division |
| **Partner** | ExactData, LLC |
| **Sponsor** | DARPA I2O (Defense Advanced Research Projects Agency) |
| **Country** | United States of America |
| **Year Released** | 2013 |

---

## Primary Research Paper

**Title:**
"Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data"

**Authors:**
Joshua Glasser, Brian Lindauer
(CERT Division, Carnegie Mellon University SEI)

**Published In:**
2013 IEEE Security and Privacy Workshops (SPW)
San Francisco, California, USA
May 23, 2013
Pages: 98–104

**IEEE DOI:**
https://doi.org/10.1109/SPW.2013.37

**Full IEEE Citation:**
```
J. Glasser and B. Lindauer, "Bridging the Gap: A Pragmatic Approach
to Generating Insider Threat Data," 2013 IEEE Security and Privacy
Workshops (SPW), San Francisco, CA, USA, 2013, pp. 98-104,
doi: 10.1109/SPW.2013.37.
```

**APA Citation:**
```
Glasser, J., & Lindauer, B. (2013). Bridging the gap: A pragmatic
approach to generating insider threat data. In 2013 IEEE Security
and Privacy Workshops (pp. 98-104). IEEE.
https://doi.org/10.1109/SPW.2013.37
```

---

## Official Download Links

| Platform | URL |
|----------|-----|
| **CMU KiltHub (Official)** | https://doi.org/10.1184/R1/12841247.v1 |
| **CMU SEI Library Page** | https://www.sei.cmu.edu/library/bridging-the-gap-a-pragmatic-approach-to-generating-insider-threat-data/ |
| **Kaggle (Mirror)** | https://www.kaggle.com/datasets/mrajaxnp/cert-insider-threat-detection-research |
| **IEEE Paper** | https://doi.org/10.1109/SPW.2013.37 |

---

## What Is This Dataset?

The CERT Insider Threat Dataset r4.2 simulates a fictional organization with
approximately 4,000 employees over 18 months. CMU created it to give
researchers a benchmark for testing insider threat detection algorithms —
because real enterprise logs cannot be shared publicly due to privacy laws.

It is the **most widely cited dataset** in insider threat detection research,
used in hundreds of published academic papers worldwide.

---

## Dataset File Structure

When downloaded, the dataset contains these CSV files:

```
r4.2/
├── logon.csv        → Employee login/logout events (time, workstation)
├── file.csv         → File access, copy, open, write events
├── device.csv       → USB / removable device connection events
├── email.csv        → Email send/receive, attachments, recipients
├── http.csv         → Web browsing, upload/download activity
├── psychometric.csv → Employee psychological survey results
├── ldap/            → Employee HR records (department, role, manager)
└── answers/
    └── insiders.csv → GROUND TRUTH: malicious user IDs + scenario labels
```

---

## Features Used in This Project

| Feature Name | Source File | Description |
|-------------|-------------|-------------|
| `Login_Time` | logon.csv | Hour of day (0–23) of first login |
| `Session_Duration_Hours` | logon.csv | Total session length in hours |
| `Downloads` | file.csv | Number of files accessed/copied per day |
| `Failed_Logins` | logon.csv | Count of failed authentication attempts |
| `Data_Transfer_MB` | file.csv + http.csv | Volume of outbound data in MB |
| `Emails_Sent` | email.csv | Number of emails sent per day |
| `USB_Usage` | device.csv | 1 = USB device connected, 0 = not |
| `After_Hours_Access` | logon.csv | 1 = login outside 07:00–19:00, 0 = normal hours |
| `Label` | answers/insiders.csv | 1 = Normal employee, -1 = Insider threat |

---

## Threat Scenarios (Ground Truth)

### Scenario 1: Data Theft (12 malicious users)
**Based on:** Documented IP theft cases in CERT real-world database
**Behavior pattern:**
- Login after 18:00 (after-hours)
- Bulk file downloads to USB drive
- External email with attachments
- Short, focused sessions

### Scenario 2: System Sabotage (4 malicious users)
**Based on:** IT sabotage cases from CERT database
**Behavior pattern:**
- Multiple failed login attempts (credential abuse)
- Late-night system access
- Minimal normal productivity
- Targeted system actions

### Scenario 3: Espionage / Corporate Intelligence (4 malicious users)
**Based on:** Corporate espionage patterns
**Behavior pattern:**
- Elevated outbound data transfers
- After-hours web uploads to external sites
- Unusual email recipients (external domains)
- Gradual, stealthy behavior

---

## Dataset Statistics

| Property | Value |
|----------|-------|
| Total Employees Simulated | ~4,000 |
| Time Period Covered | 18 months |
| Total Malicious Users | ~20 (across 3 scenarios) |
| Benign:Malicious Ratio | ~99.5% : ~0.5% |
| Total Log Events | Millions |
| File Format | CSV |
| License | Free for academic/research use |
| Language | English |

---

## Why This Dataset?

### Academic Validity:
- Published in **IEEE**, the world's most respected technical organization
- Used in **hundreds of peer-reviewed papers** — fully validated benchmark
- Provides **ground truth labels** (answers/insiders.csv) for proper evaluation
- Covers **multiple attack types** (theft, sabotage, espionage)

### Research Significance:
- Gold standard for insider threat detection research
- Enables comparison with published results from other researchers
- Multi-source logs capture full behavioral profile of employees
- Temporal patterns (18 months) capture evolving threat behavior

---

## How Data Is Used in This Project

Since the raw CERT dataset contains millions of events across multiple CSV files,
this project **pre-processes and aggregates** them into per-user-per-day feature
vectors following the methodology described in:

> lcd-dal, "Feature Extraction for CERT Insider Threat Test Datasets," GitHub, 2024.
> URL: https://github.com/lcd-dal/feature-extraction-for-CERT-insider-threat-test-datasets

The script `advanced_training.py` can:
1. **Load real CSV** if placed at `training/data/cert_r4.2.csv`
2. **Use benchmark-derived data** based on published statistics from the paper
   (Tables II & III from Glasser & Lindauer 2013)

---

## Complete References List

**[R1] Primary Dataset Paper:**
Glasser, J., & Lindauer, B. (2013). Bridging the gap: A pragmatic approach
to generating insider threat data. In *2013 IEEE Security and Privacy
Workshops* (pp. 98–104). IEEE. https://doi.org/10.1109/SPW.2013.37

**[R2] Dataset Repository:**
CERT Division, Carnegie Mellon University. (2013). *CERT Insider Threat
Test Dataset v4.2* [Dataset]. KiltHub.
https://doi.org/10.1184/R1/12841247.v1

**[R3] CERT Insider Threat Database Background:**
Trzeciak, R., & CERT Insider Threat Center. (2011). The CERT Insider
Threat Database. Carnegie Mellon University SEI Blog.
https://www.sei.cmu.edu/blog/the-cert-insider-threat-database/

**[R4] Isolation Forest Algorithm:**
Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation forest.
In *2008 Eighth IEEE International Conference on Data Mining* (pp. 413–422).
IEEE. https://doi.org/10.1109/ICDM.2008.17

**[R5] One-Class SVM Algorithm:**
Schölkopf, B., Platt, J. C., Shawe-Taylor, J., Smola, A. J., &
Williamson, R. C. (2001). Estimating the support of a high-dimensional
distribution. *Neural Computation*, 13(7), 1443–1471.
https://doi.org/10.1162/089976601750264965

**[R6] Local Outlier Factor Algorithm:**
Breunig, M. M., Kriegel, H. P., Ng, R. T., & Sander, J. (2000).
LOF: Identifying density-based local outliers. In *Proceedings of the
2000 ACM SIGMOD International Conference on Management of Data*
(pp. 93–104). https://doi.org/10.1145/342009.335388

**[R7] scikit-learn Library:**
Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python.
*Journal of Machine Learning Research*, 12, 2825–2830.
https://jmlr.csail.mit.edu/papers/v12/pedregosa11a.html

---

## One-Line Summary for Verbal Presentation

> "Sir, humne CMU CERT Insider Threat Dataset r4.2 use kiya hai jo
> Carnegie Mellon University ke CERT Division ne DARPA ke funding se
> banaya tha. Iska official paper 2013 mein IEEE Security and Privacy
> Workshops mein publish hua tha. Dataset download link hai:
> doi.org/10.1184/R1/12841247.v1"

---

*File: DATASET_REFERENCE.md*
*Project: SentinelVoice — Insider Threat Detection*
*Last Updated: October 2026*
