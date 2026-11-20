import React, { useState } from 'react';
import axios from 'axios';

export default function DuressPanel({ socket }) {
  const [pin, setPin] = useState('');
  const [userId, setUserId] = useState('USR023');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verifyPin = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/demo/verify-pin', { userId, pin });
      setResult(res.data);
    } catch {
      setResult({ status: 'denied', message: 'Server error' });
    }
    setLoading(false);
    setPin('');
    setTimeout(() => setResult(null), 5000);
  };

  return (
    <div className="duress-page">
      <div className="duress-card">
        <div className="duress-header">
          <h2>🔐 Action Verification Required</h2>
          <p>High Risk Activity Detected — Employee must verify identity</p>
        </div>

        <div className="duress-body">
          <div className="warning-box">
            ⚠️ Risk Score: <strong>94/100</strong> — Verification Required
          </div>

          <div className="input-group">
            <label>Employee ID</label>
            <input value={userId} onChange={e => setUserId(e.target.value)} placeholder="USR023" />
          </div>

          <div className="input-group">
            <label>Authorization PIN</label>
            <input type="password" value={pin} onChange={e => setPin(e.target.value)} placeholder="Enter PIN" maxLength={4} />
          </div>

          <button className="verify-btn" onClick={verifyPin} disabled={loading || pin.length < 4}>
            {loading ? 'Verifying...' : '✅ Authorize'}
          </button>

          {result && (
            <div className={`result-box ${result.status}`}>
              {result.status === 'granted' ? '✅' : '❌'} {result.message}
              {result.isDuress && (
                <div className="duress-note">🚨 Silent alert sent to security team!</div>
              )}
            </div>
          )}

          <div className="pin-hint">
            <div className="hint-item">Normal PIN: <code>1234</code> → Access Granted</div>
            <div className="hint-item duress">Duress PIN: <code>9999</code> → Screen shows Granted, Security Alerted 🚨</div>
          </div>
        </div>
      </div>
    </div>
  );
}
