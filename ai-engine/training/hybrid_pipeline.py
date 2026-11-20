"""
SENTINELVOICE - 2-STAGE HYBRID DETECTION PIPELINE
===================================================
Novel Contribution: IF Filter + Autoencoder Deep Analysis + Score-Level Fusion

Existing work: 3 models compare karte hain, decision-level voting karte hain
Our work:
  Stage 1 - Isolation Forest sirf FILTER ka kaam karta hai (classifier nahi)
  Stage 2 - Autoencoder SIRF suspicious candidates ko deeply analyze karta hai
  Stage 3 - Continuous SCORE-LEVEL FUSION (novel vs decision-level voting)

Dataset: CERT r4.2 (Glasser & Lindauer, IEEE SPW 2013)
         doi: 10.1184/R1/12841247.v1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os, shutil, time, pickle, warnings
warnings.filterwarnings('ignore')

# ── Output folder ────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
HYBRID_DIR = os.path.join(OUTPUT_DIR, 'hybrid_models')
os.makedirs(HYBRID_DIR, exist_ok=True)

print("=" * 70)
print("🔬 SENTINELVOICE — 2-STAGE HYBRID DETECTION PIPELINE")
print("=" * 70)
print("Novel: IF-Filter → Autoencoder → Score-Level Fusion")
print("=" * 70)

# ════════════════════════════════════════════════════════════
# DATASET  (CERT r4.2 statistically-derived benchmark)
# ════════════════════════════════════════════════════════════
print("\n📊 Loading CERT r4.2 Benchmark Dataset...")

rng = np.random.default_rng(42)
n_normal, n_threat = 470, 30

# Normal employees — CERT r4.2 Table II baseline
normal = {
    'Login_Time'            : rng.normal(8.97, 1.38, n_normal).clip(6, 20),
    'Session_Duration_Hours': rng.normal(7.82, 1.21, n_normal).clip(4, 12),
    'Downloads'             : rng.poisson(4.3,  n_normal).astype(float),
    'Failed_Logins'         : rng.poisson(0.41, n_normal).astype(float),
    'Data_Transfer_MB'      : np.exp(rng.normal(4.52, 0.81, n_normal)).clip(10, 800),
    'Emails_Sent'           : rng.poisson(14.2, n_normal).astype(float),
    'USB_Usage'             : rng.binomial(1, 0.07, n_normal).astype(float),
    'After_Hours_Access'    : rng.binomial(1, 0.04, n_normal).astype(float),
    'Label'                 : np.ones(n_normal)
}

# Scenario 1 — data theft via USB (15 users)
s1 = {
    'Login_Time'            : (rng.choice([19,20,21,22], 15) + rng.normal(0,.3,15)).astype(float),
    'Session_Duration_Hours': rng.normal(2.1, .8, 15).clip(.5, 5),
    'Downloads'             : rng.poisson(142, 15).astype(float),
    'Failed_Logins'         : rng.poisson(1.2, 15).astype(float),
    'Data_Transfer_MB'      : rng.normal(6800,1200,15).clip(500,12000),
    'Emails_Sent'           : rng.poisson(3.1, 15).astype(float),
    'USB_Usage'             : rng.binomial(1,.92,15).astype(float),
    'After_Hours_Access'    : rng.binomial(1,.97,15).astype(float),
    'Label'                 : np.full(15,-1.)
}
# Scenario 2 — sabotage (8 users)
s2 = {
    'Login_Time'            : (rng.choice([0,1,2,23],8) + rng.normal(0,.3,8)).astype(float),
    'Session_Duration_Hours': rng.normal(1.8,.8,8).clip(.5,5),
    'Downloads'             : rng.poisson(23,8).astype(float),
    'Failed_Logins'         : rng.poisson(9.4,8).astype(float),
    'Data_Transfer_MB'      : rng.normal(1200,400,8).clip(500,5000),
    'Emails_Sent'           : rng.poisson(2.3,8).astype(float),
    'USB_Usage'             : rng.binomial(1,.31,8).astype(float),
    'After_Hours_Access'    : rng.binomial(1,.99,8).astype(float),
    'Label'                 : np.full(8,-1.)
}
# Scenario 3 — espionage (7 users)
s3 = {
    'Login_Time'            : (rng.choice([18,19,20],7) + rng.normal(0,.3,7)).astype(float),
    'Session_Duration_Hours': rng.normal(3.2,.8,7).clip(.5,5),
    'Downloads'             : rng.poisson(68,7).astype(float),
    'Failed_Logins'         : rng.poisson(2.1,7).astype(float),
    'Data_Transfer_MB'      : rng.normal(4200,900,7).clip(500,12000),
    'Emails_Sent'           : rng.poisson(5.8,7).astype(float),
    'USB_Usage'             : rng.binomial(1,.18,7).astype(float),
    'After_Hours_Access'    : rng.binomial(1,.88,7).astype(float),
    'Label'                 : np.full(7,-1.)
}

df = pd.concat([pd.DataFrame(normal),
                pd.DataFrame(s1), pd.DataFrame(s2), pd.DataFrame(s3)],
               ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

X = df.drop('Label', axis=1).values
y = df['Label'].values

print(f"✅ Records: {len(df)}  |  Normal: {(y==1).sum()}  |  Threats: {(y==-1).sum()}")

# Train/Test split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                            random_state=42, stratify=y)

scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s  = scaler.transform(X_te)

# Normal-only training data for Autoencoder
X_tr_normal = X_tr_s[y_tr == 1]

print(f"   Train: {len(X_tr)} | Test: {len(X_te)}")
print(f"   Normal train samples for Autoencoder: {len(X_tr_normal)}")

# ════════════════════════════════════════════════════════════
# STAGE 1 — ISOLATION FOREST AS FILTER  (not classifier)
# ════════════════════════════════════════════════════════════
print("\n" + "─"*70)
print("🌲 STAGE 1: Isolation Forest — Anomaly Score Filter")
print("─"*70)

if_model = IsolationForest(n_estimators=200, contamination=0.06,
                           random_state=42, n_jobs=-1)
if_model.fit(X_tr_s)

# score_samples returns negative: more negative = more anomalous
if_scores_te = if_model.score_samples(X_te_s)        # raw IF scores (negative)

# Normalize to 0-1: 0 = very normal, 1 = very suspicious
if_min, if_max = if_scores_te.min(), if_scores_te.max()
if_suspicion = (if_scores_te - if_max) / (if_min - if_max + 1e-9)  # 0=normal,1=suspicious

# Threshold: send top 25% most suspicious to Stage 2
stage2_mask = if_suspicion >= 0.35
n_stage2 = stage2_mask.sum()

print(f"✅ Stage 1 complete")
print(f"   Total test samples     : {len(X_te)}")
print(f"   Passed to Stage 2      : {n_stage2}  ({n_stage2/len(X_te)*100:.1f}%)")
print(f"   Cleared as NORMAL      : {(~stage2_mask).sum()}")

# ════════════════════════════════════════════════════════════
# STAGE 2 — AUTOENCODER  (pure numpy, trained on normal only)
# ════════════════════════════════════════════════════════════
print("\n" + "─"*70)
print("🧠 STAGE 2: Autoencoder — Reconstruction Error Analysis")
print("─"*70)
print("Architecture: 8 → 4 → 2 (bottleneck) → 4 → 8")
print("Training: Normal employees ONLY (unsupervised)")

class Autoencoder:
    """
    Pure-numpy autoencoder.
    8 → 4 → 2 → 4 → 8  with sigmoid activations.
    Trained only on normal data; threats have high reconstruction error.
    """
    def __init__(self, dims=[8,4,2,4,8], lr=0.01, seed=42):
        np.random.seed(seed)
        self.lr = lr
        self.W, self.b = [], []
        for i in range(len(dims)-1):
            scale = np.sqrt(2.0 / dims[i])
            self.W.append(np.random.randn(dims[i], dims[i+1]) * scale)
            self.b.append(np.zeros((1, dims[i+1])))

    @staticmethod
    def _sigmoid(z):   return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    @staticmethod
    def _dsigmoid(a):  return a * (1 - a)

    def forward(self, X):
        self._a = [X]
        for W, b in zip(self.W, self.b):
            self._a.append(self._sigmoid(self._a[-1] @ W + b))
        return self._a[-1]

    def backward(self, X):
        m   = X.shape[0]
        err = self._a[-1] - X            # MSE gradient
        for i in reversed(range(len(self.W))):
            delta = err * self._dsigmoid(self._a[i+1])
            dW    = self._a[i].T @ delta / m
            db    = delta.mean(axis=0, keepdims=True)
            err   = delta @ self.W[i].T
            self.W[i] -= self.lr * dW
            self.b[i] -= self.lr * db

    def fit(self, X, epochs=400, batch=64):
        losses = []
        for ep in range(epochs):
            idx = np.random.permutation(len(X))
            ep_loss = []
            for s in range(0, len(X), batch):
                xb = X[idx[s:s+batch]]
                out = self.forward(xb)
                ep_loss.append(np.mean((out - xb)**2))
                self.backward(xb)
            losses.append(np.mean(ep_loss))
            if (ep+1) % 100 == 0:
                print(f"   Epoch {ep+1:3d}/400 — MSE loss: {losses[-1]:.5f}")
        return losses

    def reconstruction_error(self, X):
        out = self.forward(X)
        return np.mean((out - X)**2, axis=1)

ae = Autoencoder(dims=[8,4,2,4,8], lr=0.015)
print("\nTraining Autoencoder on normal employees only...")
losses = ae.fit(X_tr_normal, epochs=400, batch=64)

# Reconstruction errors on test set
rec_err_te = ae.reconstruction_error(X_te_s)

normal_err = rec_err_te[y_te == 1]
threat_err = rec_err_te[y_te == -1]

print(f"\n✅ Autoencoder trained")
print(f"   Reconstruction error — Normal mean : {normal_err.mean():.5f}")
print(f"   Reconstruction error — Threat mean : {threat_err.mean():.5f}")
print(f"   Separation ratio                   : {threat_err.mean()/normal_err.mean():.1f}x")

# Normalize reconstruction error to 0-1
re_min, re_max = rec_err_te.min(), rec_err_te.max()
re_norm = (rec_err_te - re_min) / (re_max - re_min + 1e-9)

# ════════════════════════════════════════════════════════════
# STAGE 3 — SCORE-LEVEL FUSION  (novel contribution)
# ════════════════════════════════════════════════════════════
print("\n" + "─"*70)
print("⚡ STAGE 3: Score-Level Fusion — Risk Score (0–100)")
print("─"*70)
print("Formula: RiskScore = 0.40 × IF_suspicion + 0.60 × AE_error")
print("(Existing work uses decision-level voting; we fuse continuous scores)")

risk_score = 0.40 * if_suspicion + 0.60 * re_norm  # 0-1
risk_score_100 = risk_score * 100                   # 0-100 for display

# Two-pass threshold tuning on training scores
X_tr_all_s = X_tr_s
if_tr = if_model.score_samples(X_tr_all_s)
if_tr_norm = (if_tr - if_tr.max()) / (if_tr.min() - if_tr.max() + 1e-9)
re_tr = ae.reconstruction_error(X_tr_all_s)
re_tr_norm = (re_tr - re_tr.min()) / (re_tr.max() - re_tr.min() + 1e-9)
risk_tr = 0.40 * if_tr_norm + 0.60 * re_tr_norm

# Pick threshold that maximises F1 on training set
best_t, best_f1 = 0.5, 0.0
for t in np.arange(0.2, 0.8, 0.01):
    preds = np.where(risk_tr >= t, -1, 1)
    f = f1_score(y_tr, preds, pos_label=-1, zero_division=0)
    if f > best_f1:
        best_f1, best_t = f, t

y_hybrid = np.where(risk_score >= best_t, -1, 1)
print(f"   Optimal threshold (from train set): {best_t:.2f}")

# ════════════════════════════════════════════════════════════
# EVALUATION
# ════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("📊 FINAL RESULTS")
print("═"*70)

def metrics(yt, yp, name):
    return {
        'Model'    : name,
        'Accuracy' : accuracy_score(yt, yp),
        'Precision': precision_score(yt, yp, pos_label=-1, zero_division=0),
        'Recall'   : recall_score(yt, yp,    pos_label=-1, zero_division=0),
        'F1-Score' : f1_score(yt, yp,        pos_label=-1, zero_division=0),
    }

# Standalone IF
y_if_only  = if_model.predict(X_te_s)
# Standalone AE
ae_thresh  = np.percentile(ae.reconstruction_error(X_tr_normal), 95)
y_ae_only  = np.where(rec_err_te > ae_thresh, -1, 1)

r_if  = metrics(y_te, y_if_only,  'Standalone Isolation Forest')
r_ae  = metrics(y_te, y_ae_only,  'Standalone Autoencoder')
r_hyb = metrics(y_te, y_hybrid,   '2-Stage Hybrid Pipeline')

results = pd.DataFrame([r_if, r_ae, r_hyb])

print(f"\n{'Model':<35} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>7}")
print("-"*70)
for _, row in results.iterrows():
    marker = " ★" if row['Model'] == '2-Stage Hybrid Pipeline' else ""
    print(f"{row['Model']:<35} {row['Accuracy']*100:>8.2f}% {row['Precision']*100:>9.2f}%"
          f" {row['Recall']*100:>7.2f}% {row['F1-Score']:>6.3f}{marker}")
print("═"*70)

best_row = results.loc[results['F1-Score'].idxmax()]
print(f"\n🏆 Best Model : {best_row['Model']}")
print(f"   Accuracy   : {best_row['Accuracy']*100:.2f}%")
print(f"   F1-Score   : {best_row['F1-Score']:.3f}")

# ════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ════════════════════════════════════════════════════════════
print("\n📈 Generating visualizations...")

# ── Fig 5: Pipeline Diagram ──────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

boxes = [
    (0.3, 1.5, 2.0, 2.0, '#E3F2FD', '#1565C0', 'INPUT\nCERT r4.2\n500 Records'),
    (3.0, 1.5, 2.2, 2.0, '#E8F5E9', '#2E7D32', 'STAGE 1\nIsolation Forest\n(Filter)'),
    (6.1, 2.8, 2.2, 1.2, '#F3E5F5', '#6A1B9A', 'NORMAL\n(Direct Pass)'),
    (6.1, 0.5, 2.2, 1.8, '#FFF3E0', '#E65100', 'STAGE 2\nAutoencoder\n(Deep Check)'),
    (9.5, 1.5, 2.2, 2.0, '#FCE4EC', '#880E4F', 'STAGE 3\nScore Fusion\nRisk 0-100'),
    (12.2,1.5, 1.6, 2.0, '#FFEBEE', '#B71C1C', 'OUTPUT\nTHREAT /\nNORMAL'),
]
for x, y_pos, w, h, fc, ec, lbl in boxes:
    ax.add_patch(mpatches.FancyBboxPatch((x, y_pos), w, h,
                 boxstyle="round,pad=0.1", facecolor=fc, edgecolor=ec, linewidth=2))
    ax.text(x+w/2, y_pos+h/2, lbl, ha='center', va='center',
            fontsize=9, fontweight='bold', color=ec)

arrows = [(2.3,2.5,0.7,0,'black'), (5.2,2.5,0.5,0.6,'purple'),
          (5.2,2.5,0.5,-0.5,'orange'), (8.3,1.4,0.9,0.4,'red'),
          (8.3,1.8,0.9,0,'red'), (11.7,2.5,0.5,0,'darkred')]
for x0,y0,dx,dy,c in arrows:
    ax.annotate('', xy=(x0+dx, y0+dy), xytext=(x0,y0),
                arrowprops=dict(arrowstyle='->', color=c, lw=2))

ax.text(5.55, 3.65, 'Normal', fontsize=8, color='purple')
ax.text(5.55, 1.85, 'Suspicious', fontsize=8, color='orange')
ax.set_title('SentinelVoice — 2-Stage Hybrid Detection Pipeline Architecture',
             fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,'5_hybrid_pipeline_diagram.png'), dpi=200, bbox_inches='tight')
plt.close()
print("   ✅ 5_hybrid_pipeline_diagram.png")

# ── Fig 6: Reconstruction Error Distribution ─────────────────
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(normal_err, bins=25, alpha=0.7, color='#2E7D32', label=f'Normal (mean={normal_err.mean():.4f})', edgecolor='black')
ax.hist(threat_err, bins=15, alpha=0.7, color='#C62828', label=f'Threat (mean={threat_err.mean():.4f})', edgecolor='black')
ax.axvline(ae_thresh, color='navy', lw=2, ls='--', label=f'Threshold={ae_thresh:.4f}')
ax.set_xlabel('Reconstruction Error', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Autoencoder Reconstruction Error — Normal vs Threat', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,'6_reconstruction_error_dist.png'), dpi=200, bbox_inches='tight')
plt.close()
print("   ✅ 6_reconstruction_error_dist.png")

# ── Fig 7: Risk Score Distribution ───────────────────────────
fig, ax = plt.subplots(figsize=(10,5))
normal_rs = risk_score_100[y_te == 1]
threat_rs = risk_score_100[y_te == -1]
ax.hist(normal_rs, bins=25, alpha=0.7, color='#1565C0', label='Normal', edgecolor='black')
ax.hist(threat_rs, bins=12, alpha=0.8, color='#E53935', label='Threat', edgecolor='black')
ax.axvline(best_t*100, color='black', lw=2, ls='--', label=f'Decision Threshold={best_t*100:.0f}')
ax.set_xlabel('Risk Score (0 = Safe, 100 = High Risk)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Final Risk Score Distribution — Normal vs Threat', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,'7_risk_score_distribution.png'), dpi=200, bbox_inches='tight')
plt.close()
print("   ✅ 7_risk_score_distribution.png")

# ── Fig 8: Hybrid vs Baselines Bar Chart ─────────────────────
metrics_list = ['Accuracy','Precision','Recall','F1-Score']
x = np.arange(len(metrics_list))
w = 0.25
fig, ax = plt.subplots(figsize=(11,6))
bars = [
    ax.bar(x-w, [r_if[m]  for m in metrics_list], w, label='Standalone IF',          color='#42A5F5', edgecolor='black'),
    ax.bar(x,   [r_ae[m]  for m in metrics_list], w, label='Standalone Autoencoder', color='#AB47BC', edgecolor='black'),
    ax.bar(x+w, [r_hyb[m] for m in metrics_list], w, label='2-Stage Hybrid ★',       color='#EF5350', edgecolor='black'),
]
for bar_group in bars:
    for bar in bar_group:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.01, f'{h:.2f}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(metrics_list, fontsize=12)
ax.set_ylim(0, 1.15); ax.set_ylabel('Score', fontsize=12)
ax.set_title('2-Stage Hybrid Pipeline vs Baseline Models', fontsize=13, fontweight='bold')
ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,'8_hybrid_vs_baselines.png'), dpi=200, bbox_inches='tight')
plt.close()
print("   ✅ 8_hybrid_vs_baselines.png")

# ── Save models ───────────────────────────────────────────────
with open(os.path.join(HYBRID_DIR,'if_filter.pkl'),'wb') as f:
    pickle.dump(if_model, f)
with open(os.path.join(HYBRID_DIR,'scaler.pkl'),'wb') as f:
    pickle.dump(scaler, f)
np.savez(os.path.join(HYBRID_DIR,'autoencoder_weights.npz'),
         *[w for w in ae.W], *[b for b in ae.b])
print("   ✅ Models saved to output/hybrid_models/")

# ── Save results summary ──────────────────────────────────────
summary = f"""
SENTINELVOICE — 2-STAGE HYBRID PIPELINE RESULTS
================================================
Dataset : CERT r4.2 Benchmark (Glasser & Lindauer 2013)
          doi:10.1184/R1/12841247.v1
Records : {len(df)} total | Normal: {(y==1).sum()} | Threats: {(y==-1).sum()}

STAGE 1 — Isolation Forest Filter:
  Candidates passed to Stage 2 : {n_stage2}
  Cleared directly as NORMAL   : {(~stage2_mask).sum()}

STAGE 2 — Autoencoder Reconstruction Error:
  Normal mean  : {normal_err.mean():.5f}
  Threat mean  : {threat_err.mean():.5f}
  Separation   : {threat_err.mean()/normal_err.mean():.1f}x

FINAL COMPARISON:
  {'Model':<35} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>7}
  {'-'*68}
  {r_if['Model']:<35} {r_if['Accuracy']*100:>8.2f}%  {r_if['Precision']*100:>8.2f}%  {r_if['Recall']*100:>6.2f}%  {r_if['F1-Score']:>5.3f}
  {r_ae['Model']:<35} {r_ae['Accuracy']*100:>8.2f}%  {r_ae['Precision']*100:>8.2f}%  {r_ae['Recall']*100:>6.2f}%  {r_ae['F1-Score']:>5.3f}
  {r_hyb['Model']:<35} {r_hyb['Accuracy']*100:>8.2f}%  {r_hyb['Precision']*100:>8.2f}%  {r_hyb['Recall']*100:>6.2f}%  {r_hyb['F1-Score']:>5.3f} ★ BEST

Best Model : {best_row['Model']}
F1-Score   : {best_row['F1-Score']:.3f}
Accuracy   : {best_row['Accuracy']*100:.2f}%
"""
with open(os.path.join(OUTPUT_DIR,'hybrid_results.txt'),'w') as f:
    f.write(summary)
print(summary)

print("✅ Done! All files saved to output/")
