"""
SentinelVoice - Professional PPT Generator
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

DARK_BLUE  = RGBColor(0,   70,  127)
MID_BLUE   = RGBColor(21,  101, 192)
GREEN      = RGBColor(27,  107,  46)
RED        = RGBColor(198,  40,  40)
WHITE      = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(245, 245, 245)
DARK_GRAY  = RGBColor(50,   50,  50)
ORANGE     = RGBColor(230, 100,   0)
GOLD       = RGBColor(255, 193,   7)

BLANK = prs.slide_layouts[6]   # completely blank

# ── helpers ──────────────────────────────────────────────────────────────────
def bg(slide, color):
    from pptx.oxml.ns import qn
    from lxml import etree
    bg_elem = slide.background
    fill    = bg_elem.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, l, t, w, h, text='', fg=WHITE, bk=DARK_BLUE,
        bold=False, size=18, align=PP_ALIGN.CENTER,
        border_color=None, border_w=Pt(0), radius=False):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf    = txBox.text_frame
    tf.word_wrap = True
    # fill
    from pptx.oxml.ns import qn
    from lxml import etree
    spPr = txBox._element.spPr
    solidFill = etree.SubElement(spPr, qn('a:solidFill'))
    srgb = etree.SubElement(solidFill, qn('a:srgbClr'))
    srgb.set('val', str(bk))
    if border_color:
        ln = etree.SubElement(spPr, qn('a:ln'))
        ln.set('w', str(int(border_w.pt * 12700)))
        bf = etree.SubElement(ln, qn('a:solidFill'))
        bs = etree.SubElement(bf, qn('a:srgbClr'))
        bs.set('val', str(border_color))
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.bold  = bold
    run.font.size  = Pt(size)
    run.font.color.rgb = fg
    return txBox

def heading(slide, text, t, size=32, color=WHITE, bold=True, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(t), Inches(12.3), Inches(0.7))
    tf = tb.text_frame
    p  = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text           = text
    r.font.bold      = bold
    r.font.size      = Pt(size)
    r.font.color.rgb = color
    return tb

def para(slide, text, l, t, w, h, size=16, color=DARK_GRAY,
         bold=False, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text           = text
    r.font.size      = Pt(size)
    r.font.color.rgb = color
    r.font.bold      = bold
    return tb

def multi_para(slide, lines, l, t, w, size=15, color=DARK_GRAY,
               bold=False, spacing=0.42, bullet=True):
    for i, line in enumerate(lines):
        prefix = "  •  " if bullet else "  "
        para(slide, prefix + line, l, t + i*spacing, w, 0.4,
             size=size, color=color, bold=bold)

def img(slide, fname, l, t, w):
    path = os.path.join(OUTPUT_DIR, fname)
    if os.path.exists(path):
        slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w))

def divider(slide, t, color=MID_BLUE):
    from pptx.oxml.ns import qn
    from lxml import etree
    sp = slide.shapes.add_shape(1, Inches(0.5), Inches(t), Inches(12.3), Inches(0.04))
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    sp.line.fill.background()

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, DARK_BLUE)

# Top accent bar
box(s, 0, 0, 13.33, 0.18, bk=MID_BLUE)

# Main title
tb = s.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.4))
tf = tb.text_frame
p  = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r  = p.add_run(); r.text = "SENTINELVOICE"
r.font.bold = True; r.font.size = Pt(54); r.font.color.rgb = WHITE

tb2 = s.shapes.add_textbox(Inches(0.8), Inches(2.75), Inches(11.7), Inches(0.8))
tf2 = tb2.text_frame
p2  = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
r2  = p2.add_run()
r2.text = "AI-Powered Insider Threat Detection System"
r2.font.size = Pt(22); r2.font.color.rgb = RGBColor(173, 216, 230)

# Divider line
box(s, 2.5, 3.65, 8.3, 0.06, bk=GOLD)

# Subtitle cards
cards = [
    (1.0,  4.1, 3.5, "2-Stage Hybrid Pipeline",   MID_BLUE),
    (4.9,  4.1, 3.5, "CERT r4.2 Dataset",          GREEN),
    (8.8,  4.1, 3.5, "100% Accuracy",              RED),
]
for lc, tc, wc, txt, clr in cards:
    box(s, lc, tc, wc, 0.75, txt, WHITE, clr, bold=True, size=14)

# Team info
box(s, 0, 6.3, 13.33, 1.2, bk=RGBColor(0, 40, 80))
para(s, "Vaibhav Sharma  |  Ayush Pandey  |  Sudhanshu Pandey",
     0, 6.42, 13.33, 0.5, size=15, color=RGBColor(173,216,230),
     align=PP_ALIGN.CENTER)
para(s, "Department of Computer Science  •  October 2026",
     0, 6.85, 13.33, 0.4, size=12, color=RGBColor(140,180,210),
     align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "The Problem — Insider Threats", 0.2, size=28)

# Left — problem
box(s, 0.4, 1.3, 5.8, 0.5, "⚠️  What Is an Insider Threat?",
    WHITE, MID_BLUE, bold=True, size=16)
points_l = [
    "Employees who misuse their authorized access",
    "Data theft — copying files to USB or email",
    "System sabotage — deleting or corrupting data",
    "Espionage — sharing secrets with competitors",
    "Hard to detect — they look 'normal' on surface",
]
multi_para(s, points_l, 0.5, 1.95, 5.6, size=14, color=DARK_GRAY)

# Right — why hard
box(s, 6.6, 1.3, 6.3, 0.5, "🔍  Why Traditional Systems Fail?",
    WHITE, RED, bold=True, size=16)
points_r = [
    "Rule-based systems: easy to bypass",
    "Need labeled data — insider data is rare",
    "High false positive rate → alert fatigue",
    "Single-model approaches miss subtle patterns",
    "No real-time continuous monitoring",
]
multi_para(s, points_r, 6.7, 1.95, 6.1, size=14, color=DARK_GRAY)

divider(s, 5.1)
box(s, 1.5, 5.25, 10.3, 0.75,
    "💡  Our Solution: SentinelVoice — AI learns what NORMAL looks like, then flags DEVIATIONS",
    WHITE, GREEN, bold=True, size=16)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — DATASET
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Dataset — CMU CERT Insider Threat r4.2", 0.2, size=28)

box(s, 0.4, 1.25, 12.5, 0.5,
    "Source: Carnegie Mellon University, Software Engineering Institute (CERT Division) | DARPA Funded",
    DARK_GRAY, RGBColor(220,235,255), bold=False, size=13,
    border_color=MID_BLUE, border_w=Pt(1.5))

# Stats boxes
stats = [
    ("500",    "Records\n(User-Day)",   MID_BLUE),
    ("470",    "Normal\nEmployees",     GREEN),
    ("30",     "Insider\nThreats",      RED),
    ("3",      "Real Threat\nScenarios",ORANGE),
    ("8",      "Behavioral\nFeatures",  RGBColor(106,27,154)),
]
for i, (num, lbl, clr) in enumerate(stats):
    x = 0.4 + i * 2.5
    box(s, x, 1.95, 2.2, 0.65, num,  WHITE, clr, bold=True, size=28, align=PP_ALIGN.CENTER)
    box(s, x, 2.62, 2.2, 0.55, lbl,  clr, RGBColor(240,240,240), bold=False, size=12, align=PP_ALIGN.CENTER)

# 3 scenarios
box(s, 0.4, 3.35, 12.5, 0.4, "3 Real Insider Threat Scenarios (Based on Actual Documented Cases):",
    DARK_BLUE, RGBColor(220,235,255), bold=True, size=14)
sc = [
    (0.4,  3.9,  4.0, "Scenario 1\nData Theft via USB",         "15 users — bulk downloads,\nafter-hours access, USB usage", MID_BLUE),
    (4.6,  3.9,  4.0, "Scenario 2\nSystem Sabotage",            "8 users — multiple failed logins,\nlate night access",        RED),
    (8.8,  3.9,  4.0, "Scenario 3\nCorporate Espionage",        "7 users — elevated transfers,\nexternal email destinations",  ORANGE),
]
for lc, tc, wc, title, desc, clr in sc:
    box(s, lc, tc, wc, 0.55, title, WHITE, clr, bold=True, size=13)
    box(s, lc, 4.47, wc, 0.75, desc, DARK_GRAY, WHITE, size=12,
        border_color=clr, border_w=Pt(1))

# Paper reference
box(s, 0.4, 5.4, 12.5, 0.65,
    "📄  Reference: Glasser J. & Lindauer B. (2013). Bridging the Gap: A Pragmatic Approach to Generating "
    "Insider Threat Data. IEEE Security & Privacy Workshops, pp.98-104. DOI: 10.1109/SPW.2013.37\n"
    "🔗  Dataset DOI: https://doi.org/10.1184/R1/12841247.v1",
    DARK_GRAY, RGBColor(255,250,220), size=11,
    border_color=GOLD, border_w=Pt(1.5))

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — NOVEL APPROACH OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Our Novel Approach — 2-Stage Hybrid Pipeline", 0.2, size=27)

box(s, 0.4, 1.25, 12.5, 0.45,
    "Existing work: compare 3 algorithms, majority vote (decision-level)   |   Our work: IF Filter → Autoencoder → Score-Level Fusion",
    WHITE, MID_BLUE, size=13)

# Pipeline boxes
pipe = [
    (0.3,  2.0, 2.4, 1.6, "INPUT\n\n500 Employee\nRecords\n(CERT r4.2)", RGBColor(21,101,192)),
    (3.1,  2.0, 2.6, 1.6, "STAGE 1\n\nIsolation Forest\nFilter\n(Suspicion Score)", GREEN),
    (6.2,  1.4, 2.6, 1.1, "123 NORMAL\n→ Direct Pass ✅", RGBColor(0,100,0)),
    (6.2,  2.7, 2.6, 1.1, "27 Suspicious\n→ Stage 2 🔍", ORANGE),
    (9.3,  2.0, 2.6, 1.6, "STAGE 2\n\nAutoencoder\nNeural Network\n(8→4→2→4→8)", RGBColor(106,27,154)),
]
for lc,tc,wc,hc,txt,clr in pipe:
    box(s, lc, tc, wc, hc, txt, WHITE, clr, bold=False, size=12)

# Arrows
for arr_txt, lc, tc in [("→", 2.75, 2.65), ("→", 5.78, 2.65), ("→", 8.87, 2.65)]:
    para(s, arr_txt, lc, tc, 0.4, 0.4, size=24, color=DARK_BLUE, bold=True, align=PP_ALIGN.CENTER)

# Stage 3 fusion
box(s, 3.5, 4.0, 6.3, 0.9,
    "STAGE 3 — Score-Level Fusion\nRisk Score = 0.40 × IF_suspicion + 0.60 × AE_error → 0–100",
    WHITE, RED, bold=True, size=14)

# Novel callouts
novel = [
    "Novel 1: IF used as FILTER (not classifier) — continuous score, not -1/+1",
    "Novel 2: Autoencoder trained on NORMAL data only — threats have 24.5× higher error",
    "Novel 3: Score-Level Fusion — combines continuous numbers, not binary votes",
]
multi_para(s, novel, 0.5, 5.1, 12.3, size=13, color=DARK_GRAY, bullet=True, spacing=0.38)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — PIPELINE DIAGRAM (image)
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Pipeline Architecture Diagram", 0.2, size=28)
img(s, '5_hybrid_pipeline_diagram.png', 0.5, 1.2, 12.3)
para(s, "Figure 5: SentinelVoice 2-Stage Hybrid Detection Pipeline",
     0, 6.9, 13.33, 0.4, size=12, color=MID_BLUE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — AUTOENCODER EXPLANATION
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Stage 2 — Autoencoder Neural Network", 0.2, size=28)

# Architecture visual
layers = [
    (0.5,  "INPUT\n8 features",     MID_BLUE,  1.4),
    (3.0,  "ENCODER\n8 → 4 → 2",   GREEN,     1.4),
    (5.5,  "BOTTLENECK\n2 neurons", RED,       1.4),
    (8.0,  "DECODER\n2 → 4 → 8",   GREEN,     1.4),
    (10.5, "OUTPUT\n8 features",    MID_BLUE,  1.4),
]
for lc, txt, clr, wc in layers:
    box(s, lc, 1.3, 2.3, 1.3, txt, WHITE, clr, bold=True, size=13)
for arr_x in [2.85, 5.35, 7.85, 10.35]:
    para(s, "→", arr_x, 1.75, 0.3, 0.4, size=20, color=DARK_BLUE, bold=True, align=PP_ALIGN.CENTER)

# Key stats
box(s, 0.4, 2.85, 12.5, 0.4,
    "Trained ONLY on Normal Employees (329 samples)  •  400 Epochs  •  MSE Loss  •  Pure NumPy (no TensorFlow)",
    DARK_GRAY, RGBColor(240,255,240), size=13, border_color=GREEN, border_w=Pt(1.5))

# Error comparison
box(s, 0.4, 3.45, 5.8, 0.45, "Normal Employees", WHITE, GREEN, bold=True, size=15)
box(s, 0.4, 3.92, 5.8, 1.1,
    "Reconstruction Error: 0.362\n\n"
    "Model perfectly reconstructs normal\nbehavior → LOW error ✅",
    DARK_GRAY, RGBColor(240,255,240), size=14, border_color=GREEN, border_w=Pt(1.5))

box(s, 7.1, 3.45, 5.8, 0.45, "Insider Threats", WHITE, RED, bold=True, size=15)
box(s, 7.1, 3.92, 5.8, 1.1,
    "Reconstruction Error: 8.874\n\n"
    "Model CANNOT reconstruct threat\npatterns → HIGH error 🔴",
    DARK_GRAY, RGBColor(255,240,240), size=14, border_color=RED, border_w=Pt(1.5))

box(s, 4.5, 3.45, 2.3, 0.45, "⚡", WHITE, ORANGE, bold=True, size=24)
box(s, 4.5, 3.92, 2.3, 1.1,
    "24.5×\nSeparation\nRatio", WHITE, ORANGE, bold=True, size=16)

# Reconstruction error graph
img(s, '6_reconstruction_error_dist.png', 0.5, 5.1, 12.3)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Experimental Results", 0.2, size=28)

# Table header
box(s, 0.4, 1.2, 4.5, 0.5, "Model", WHITE, DARK_BLUE, bold=True, size=14)
for i, m in enumerate(["Accuracy", "Precision", "Recall", "F1-Score"]):
    box(s, 5.1 + i*2.0, 1.2, 1.9, 0.5, m, WHITE, DARK_BLUE, bold=True, size=14)

# Data rows
rows = [
    ("Standalone Isolation Forest",   "100.00%","100.00%","100.00%","1.000", False),
    ("Standalone Autoencoder",         "94.00%", "50.00%","100.00%","0.667", False),
    ("3-Algorithm Ensemble (old)",     "88.41%", "54.55%", "66.67%","0.600", False),
    ("2-Stage Hybrid Pipeline ★",     "100.00%","100.00%","100.00%","1.000", True),
]
for i, (name, acc, prec, rec, f1, highlight) in enumerate(rows):
    bkg = RGBColor(212,237,218) if highlight else (RGBColor(255,255,255) if i%2==0 else RGBColor(245,245,245))
    fc  = DARK_BLUE if highlight else DARK_GRAY
    box(s, 0.4,  1.75+i*0.65, 4.5, 0.6, name, fc, bkg, bold=highlight, size=13, align=PP_ALIGN.LEFT)
    for j, val in enumerate([acc, prec, rec, f1]):
        box(s, 5.1+j*2.0, 1.75+i*0.65, 1.9, 0.6, val, fc, bkg, bold=highlight, size=13)

# Key finding
box(s, 0.4, 4.45, 12.5, 0.65,
    "🏆  Key Finding: 2-Stage Hybrid matches perfect IF performance (100%) while improving "
    "Autoencoder baseline from 94% to 100%. Score-level fusion outperforms decision-level voting.",
    DARK_GRAY, RGBColor(255,250,220), size=13, border_color=GOLD, border_w=Pt(2))

img(s, '8_hybrid_vs_baselines.png', 0.5, 5.2, 12.3)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Feature Importance & Threat Patterns", 0.2, size=28)

feats = [
    ("1 ★  After_Hours_Access", "Normal: Always 0",   "Threat: Always 1",    RED,     0.95),
    ("2    Data_Transfer_MB",   "Normal: 50–300 MB",  "Threat: 2000–10000 MB", ORANGE, 0.80),
    ("3    Downloads",          "Normal: 1–10 files", "Threat: 100–200 files", ORANGE, 0.70),
    ("4    Failed_Logins",      "Normal: 0–1",        "Threat: 5–20",          MID_BLUE,0.55),
    ("5    USB_Usage",          "Normal: 7%",         "Threat: 80–92%",        MID_BLUE,0.45),
    ("6    Login_Time",         "Normal: 7AM–6PM",    "Threat: 2AM / 11PM",    GREEN,  0.38),
    ("7    Session_Duration",   "Normal: 6–10 hrs",   "Threat: 1–5 hrs",       GREEN,  0.28),
    ("8    Emails_Sent",        "Normal: 10–25",      "Threat: 1–5",           DARK_GRAY,0.18),
]
for i, (fname, norm, threat, clr, importance) in enumerate(feats):
    y = 1.25 + i * 0.65
    box(s, 0.4,  y, 3.5, 0.55, fname,  WHITE, clr, bold=False, size=12, align=PP_ALIGN.LEFT)
    box(s, 4.0,  y, 2.8, 0.55, norm,   DARK_GRAY, WHITE, size=12, border_color=GREEN, border_w=Pt(1))
    box(s, 6.9,  y, 2.8, 0.55, threat, DARK_GRAY, WHITE, size=12, border_color=RED,   border_w=Pt(1))
    # importance bar
    bar_w = importance * 3.0
    box(s, 9.8, y+0.1, bar_w, 0.35, '', bk=clr)
    para(s, f"{int(importance*100)}%", 9.8+bar_w+0.05, y+0.1, 0.5, 0.35,
         size=11, color=DARK_GRAY, bold=True)

para(s, "Feature", 0.4, 1.0, 3.5, 0.3, size=12, color=MID_BLUE, bold=True)
para(s, "Normal Range", 4.0, 1.0, 2.8, 0.3, size=12, color=GREEN, bold=True)
para(s, "Threat Range", 6.9, 1.0, 2.8, 0.3, size=12, color=RED, bold=True)
para(s, "Importance", 9.8, 1.0, 2.5, 0.3, size=12, color=DARK_GRAY, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — CONCLUSION & FUTURE WORK
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, LIGHT_GRAY)
box(s, 0, 0, 13.33, 1.1, bk=DARK_BLUE)
heading(s, "Conclusion & Future Work", 0.2, size=28)

# Left — conclusions
box(s, 0.4, 1.25, 6.0, 0.5, "✅  Key Conclusions", WHITE, GREEN, bold=True, size=15)
concs = [
    "2-Stage Hybrid Pipeline: 100% Accuracy, F1 = 1.0",
    "Autoencoder: 24.5× separation between normal and threat",
    "Score-level fusion > decision-level voting",
    "CERT r4.2 dataset — 3 real threat scenarios validated",
    "Pure NumPy implementation — no external DL dependencies",
]
multi_para(s, concs, 0.5, 1.9, 5.8, size=13, color=DARK_GRAY, spacing=0.45)

# Right — future work
box(s, 7.0, 1.25, 5.9, 0.5, "🔮  Future Work", WHITE, MID_BLUE, bold=True, size=15)
future = [
    "LSTM Autoencoder — temporal sequence modeling",
    "Real-time Apache Kafka stream processing",
    "Voice biometrics integration",
    "Federated learning — privacy preserving",
    "SHAP explainability for security analysts",
]
multi_para(s, future, 7.1, 1.9, 5.7, size=13, color=DARK_GRAY, spacing=0.45)

divider(s, 5.1)

# Novel summary
box(s, 0.4, 5.3, 12.5, 1.0,
    "💡  Novel Contributions Summary:\n"
    "1. IF as Filter (continuous score)   "
    "2. Pure-NumPy Autoencoder on normal-only data   "
    "3. Score-Level Fusion (0–100 risk score)",
    WHITE, DARK_BLUE, bold=False, size=14)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — THANK YOU
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, DARK_BLUE)
box(s, 0, 0, 13.33, 0.18, bk=GOLD)
box(s, 0, 7.32, 13.33, 0.18, bk=GOLD)

tb = s.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(12.3), Inches(1.2))
tf = tb.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Thank You"
r.font.bold = True; r.font.size = Pt(52); r.font.color.rgb = WHITE

box(s, 1.5, 3.1, 10.3, 0.55,
    "SentinelVoice — AI-Powered Insider Threat Detection",
    RGBColor(173,216,230), DARK_BLUE, size=18, align=PP_ALIGN.CENTER)

box(s, 0, 3.8, 13.33, 0.06, bk=MID_BLUE)

team_info = [
    ("Vaibhav Sharma",    "Leader",   3.5),
    ("Ayush Pandey",      "Member",   5.5),
    ("Sudhanshu Pandey",  "Member",   7.5),
]
for name, role, lc in team_info:
    box(s, lc, 4.1, 2.8, 0.9,
        f"{name}\n{role}", WHITE, MID_BLUE, size=13, bold=False)

box(s, 1.5, 5.3, 10.3, 0.55,
    "Dataset: CMU CERT r4.2  •  DOI: 10.1184/R1/12841247.v1",
    RGBColor(173,216,230), DARK_BLUE, size=13, align=PP_ALIGN.CENTER)
box(s, 1.5, 5.95, 10.3, 0.55,
    "Paper: Glasser & Lindauer (2013), IEEE Security & Privacy Workshops",
    RGBColor(173,216,230), DARK_BLUE, size=13, align=PP_ALIGN.CENTER)

para(s, "Questions Welcome!",
     0, 6.6, 13.33, 0.5, size=16, color=GOLD, bold=True, align=PP_ALIGN.CENTER)

# ── Save ──────────────────────────────────────────────────────
out = os.path.join(OUTPUT_DIR, 'SentinelVoice_Presentation.pptx')
prs.save(out)
print(f"✅  PPT saved: {out}")
print(f"📦  Size: {os.path.getsize(out)//1024} KB")
print(f"📊  Slides: 10")
