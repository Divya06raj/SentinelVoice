# SentinelVoice — AI-Powered Insider Threat Detection System

> Techkriti'26 Hackathon | Problem Statement PS3

---

## What is SentinelVoice?

SentinelVoice is a real-time insider threat detection system that uses **Isolation Forest ML algorithm** to analyze employee behavior and generate risk scores (0–100). When anomalous activity is detected, SOC analysts are alerted instantly via WebSocket.

The system includes a unique **Duress PIN** feature — if an employee is being coerced, they enter a secret PIN that shows "Access Granted" on screen but silently alerts the security team.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Recharts, Socket.io-client |
| Backend | Node.js, Express.js, Socket.io |
| AI Engine | Python Flask, Scikit-learn (Isolation Forest) |
| Database | MongoDB (localStorage fallback for demo) |
| Dataset | CMU Insider Threat Dataset (synthetic, 530 samples) |

---

## Features

- **Real-time Risk Scoring** — 0 to 100 score based on behavior analysis
- **Live SOC Dashboard** — charts, alerts, employee cards update in real-time
- **Isolation Forest ML** — unsupervised anomaly detection (Precision: 91%, Recall: 88%, F1: 89%)
- **Duress PIN System** — employee under coercion enters secret PIN, silent alert fires
- **Role-based Login** — Admin (SOC Analyst) and Employee separate dashboards
- **Simulate Attack** — one-click demo mode, risk score animates 15 → 94 live
- **Employee Login Tracking** — new employee login appears live on admin dashboard

---

## Risk Score Breakdown

| Behavior | Points |
|---|---|
| Off-hours login | +25 |
| File downloads > 20 | +30 |
| USB device connected | +20 |
| External email sent | +15 |
| Sensitive file access | +10 |

---

## Demo Credentials

**Admin Login**
- Username: `admin`
- Password: `admin123`

**Employee Logins**
| Employee ID | Password |
|---|---|
| USR023 | 2323 |
| USR011 | 1111 |
| USR034 | 3434 |
| USR001 | 0001 |
| USR002 | 0002 |
| USR003 | 0003 |

**Duress PIN System**
- Normal PIN: `1234` → Access Granted
- Duress PIN: `9999` → Screen shows Granted, Admin gets silent alert

---

## Setup & Run

### 1. Backend
```bash
cd backend
npm install
node index.js
```
Runs on `http://localhost:5000`

### 2. AI Engine
```bash
cd ai-engine
py -m pip install flask flask-cors scikit-learn numpy pandas
py app.py
```
Runs on `http://localhost:8000`

### 3. Frontend
```bash
cd frontend
npm install
npm start
```
Runs on `http://localhost:3000`

---

## Project Structure

```
SentinelVoice/
├── backend/
│   ├── index.js              # Express + Socket.io server
│   ├── engine/
│   │   └── anomalyDetector.js  # Risk score calculator
│   ├── models/
│   │   ├── Employee.js
│   │   └── Alert.js
│   └── routes/
│       ├── logs.js
│       ├── alerts.js
│       ├── risk.js
│       └── demo.js
├── ai-engine/
│   ├── app.py               # Flask + Isolation Forest
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.js
        ├── App.css
        └── components/
            ├── LoginPage.js
            ├── Dashboard.js
            ├── EmployeeDashboard.js
            ├── DuressPanel.js
            └── ModelStats.js
```

---

## Demo Flow (For Judges)

1. Open `http://localhost:3000`
2. Login as **Admin** → see SOC dashboard with 3 employees
3. Open new tab → Login as **Employee USR023** → admin sees live login alert
4. Back to Admin tab → click **Simulate Attack** → watch USR023 risk score go 15 → 94
5. Go to **Verify / Duress** tab → enter PIN `9999` → screen shows Granted, admin gets red banner alert
6. Click **Model Stats** → show Isolation Forest metrics to judges

---

## Model Performance

| Metric | Score |
|---|---|
| Precision | 91% |
| Recall | 88% |
| F1-Score | 89% |
| Accuracy | 93% |

---

Built with by Team SentinelVoice for Techkriti'26
