import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RISK_COLOR = (s) => s >= 60 ? '#ef4444' : s >= 30 ? '#f59e0b' : '#22c55e';

const EMPLOYEE_DATA = {
  USR023: { riskScore: 94, riskLevel: 'high', filesDownloaded: 500, usbConnected: true, offHoursLogin: true, externalEmail: true },
  USR011: { riskScore: 65, riskLevel: 'high', filesDownloaded: 45, usbConnected: false, offHoursLogin: true, externalEmail: true },
  USR034: { riskScore: 58, riskLevel: 'medium', filesDownloaded: 30, usbConnected: false, offHoursLogin: true, externalEmail: false },
  USR001: { riskScore: 12, riskLevel: 'low', filesDownloaded: 5, usbConnected: false, offHoursLogin: false, externalEmail: false },
  USR002: { riskScore: 45, riskLevel: 'medium', filesDownloaded: 22, usbConnected: false, offHoursLogin: true, externalEmail: false },
  USR003: { riskScore: 78, riskLevel: 'high', filesDownloaded: 87, usbConnected: true, offHoursLogin: true, externalEmail: false },
};

export default function EmployeeDashboard({ userId, onLogout, socket }) {
  const baseEmp = EMPLOYEE_DATA[userId] || EMPLOYEE_DATA['USR001'];

  // localStorage se saved data lo, nahi hai to default
  const loadEmp = () => {
    try {
      const saved = localStorage.getItem('sv_employees');
      if (saved) {
        const list = JSON.parse(saved);
        const found = list.find(e => e.userId === userId);
        if (found) return { ...found };
      }
    } catch {}
    return { ...baseEmp };
  };

  const [emp, setEmp] = useState(loadEmp);
  const [pin, setPin] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showDuress, setShowDuress] = useState(false);

  useEffect(() => {
    socket.on('risk-update', (data) => {
      if (data.userId === userId) {
        const newScore = data.riskScore;
        const newLevel = data.riskLevel;
        setEmp(prev => ({ ...prev, riskScore: newScore, riskLevel: newLevel }));
        // localStorage mein bhi update karo
        try {
          const saved = localStorage.getItem('sv_employees');
          if (saved) {
            const list = JSON.parse(saved);
            const updated = list.map(e => e.userId === userId ? { ...e, riskScore: newScore, riskLevel: newLevel } : e);
            localStorage.setItem('sv_employees', JSON.stringify(updated));
          }
        } catch {}
      }
    });
    return () => socket.off('risk-update');
  }, [userId, socket]);

  const verifyPin = async () => {
    setLoading(true);
    const enteredPin = pin;
    try {
      const res = await axios.post('/api/demo/verify-pin', { userId, pin: enteredPin });
      setResult(res.data);
      if (res.data.riskReduced) {
        setEmp(prev => ({ ...prev, riskScore: 15, riskLevel: 'low' }));
      }
    } catch {
      setResult({ status: 'granted', message: 'Access Granted', isDuress: enteredPin === '9999' });
    }
    setLoading(false);
    setPin('');
    setTimeout(() => setResult(null), 6000);
  };

  const reasons = [
    emp.offHoursLogin && { label: '🕐 Off-hours login detected', pts: '+25 pts' },
    emp.filesDownloaded > 20 && { label: `📁 ${emp.filesDownloaded} files downloaded`, pts: '+30 pts' },
    emp.usbConnected && { label: '💾 USB device connected', pts: '+20 pts' },
    emp.externalEmail && { label: '📧 External email sent', pts: '+15 pts' },
  ].filter(Boolean);

  return (
    <div className="emp-dashboard">
      <div className="emp-header">
        <div>
          <h2>👤 {userId}</h2>
          <p className="emp-header-sub">Your Security Risk Profile</p>
        </div>
        <button className="logout-btn" onClick={onLogout}>Logout</button>
      </div>

      <div className="emp-risk-card">
        <div className="emp-risk-label">Your Current Risk Score</div>
        <div className="emp-risk-score" style={{ color: RISK_COLOR(emp.riskScore) }}>
          {emp.riskScore}<span className="emp-risk-max">/100</span>
        </div>
        <div className="emp-risk-bar">
          <div style={{ width: `${emp.riskScore}%`, background: RISK_COLOR(emp.riskScore), height: '100%', borderRadius: 6, transition: 'width 1s' }} />
        </div>
        <div className={`emp-risk-badge ${emp.riskLevel}`}>
          {emp.riskLevel === 'high' ? '🔴 HIGH RISK' : emp.riskLevel === 'medium' ? '🟡 MEDIUM RISK' : '🟢 LOW RISK'}
        </div>
      </div>

      {reasons.length > 0 && (
        <div className="emp-card">
          <h3>⚠️ Why You Were Flagged</h3>
          <div className="detail-list">
            {reasons.map((r, i) => (
              <div key={i} className="detail-item">
                {r.label} <span className="pts">{r.pts}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="emp-card duress-section">
        <h3>🔐 Identity Verification</h3>
        <p className="duress-info">
          If someone is forcing you to grant access, enter your <strong>Duress PIN</strong> — 
          screen will show "Access Granted" but security team will be silently alerted.
        </p>

        {!showDuress ? (
          <button className="verify-btn" onClick={() => setShowDuress(true)}>
            🔐 Enter Verification PIN
          </button>
        ) : (
          <>
            <div className="input-group" style={{ marginTop: 16 }}>
              <label>Authorization PIN</label>
              <input
                type="password"
                value={pin}
                onChange={e => setPin(e.target.value)}
                placeholder="Enter 4-digit PIN"
                maxLength={4}
                onKeyDown={e => e.key === 'Enter' && pin.length === 4 && verifyPin()}
              />
            </div>
            <button className="verify-btn" onClick={verifyPin} disabled={loading || pin.length < 4}>
              {loading ? 'Verifying...' : '✅ Verify'}
            </button>

            {result && (
              <div className={`result-box ${result.status}`}>
                {result.status === 'granted' ? '✅' : '❌'} {result.message}
                {result.isDuress && (
                  <div className="duress-note">🚨 Silent alert sent to security team!</div>
                )}
              </div>
            )}

            <div className="pin-hint" style={{ marginTop: 12 }}>
              <div className="hint-item">Normal PIN: <code>1234</code> → Access Granted</div>
              <div className="hint-item duress">Duress PIN: <code>9999</code> → Granted + 🚨 Silent Alert</div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
