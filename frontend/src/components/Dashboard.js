import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';

const RISK_COLOR = (score) => score >= 60 ? '#ef4444' : score >= 30 ? '#f59e0b' : '#22c55e';
const MOCK_EMPLOYEES = [];

const loadEmployees = () => {
  try {
    const saved = localStorage.getItem('sv_employees');
    if (saved) return JSON.parse(saved);
  } catch {}
  return MOCK_EMPLOYEES;
};

const saveEmployees = (list) => {
  try { localStorage.setItem('sv_employees', JSON.stringify(list)); } catch {}
};

export default function Dashboard({ alerts, liveRisk, socket }) {
  const [employees, setEmployees] = useState(loadEmployees);
  const [simulating, setSimulating] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [loginAlerts, setLoginAlerts] = useState([]);
  const [riskTimeline, setRiskTimeline] = useState([
    { time: 'Mon', score: 12 }, { time: 'Tue', score: 18 }, { time: 'Wed', score: 25 },
    { time: 'Thu', score: 30 }, { time: 'Fri', score: 45 }, { time: 'Sat', score: 78 }
  ]);

  // Employees change hone par localStorage mein save karo
  useEffect(() => { saveEmployees(employees); }, [employees]);

  useEffect(() => {
    socket.on('employee-login', (data) => {
      const freshList = (() => { try { return JSON.parse(localStorage.getItem('sv_employees') || '[]'); } catch { return []; } })();
      setEmployees(freshList.map(e => ({ ...e, isNew: e.userId === data.userId ? true : e.isNew })));
      setLoginAlerts(prev => [{ userId: data.userId, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 5));
      setTimeout(() => {
        setEmployees(prev => {
          const updated = prev.map(e => e.userId === data.userId ? { ...e, isNew: false } : e);
          saveEmployees(updated);
          return updated;
        });
      }, 5000);
    });
    return () => socket.off('employee-login');
  }, [socket]);

  useEffect(() => {
    if (Object.keys(liveRisk).length > 0) {
      setEmployees(prev => {
        const updated = prev.map(e =>
          liveRisk[e.userId] !== undefined
            ? { ...e, riskScore: liveRisk[e.userId], riskLevel: liveRisk[e.userId] >= 60 ? 'high' : liveRisk[e.userId] >= 30 ? 'medium' : 'low' }
            : e
        );
        saveEmployees(updated);
        return updated;
      });
    }
  }, [liveRisk]);

  const simulateAttack = async () => {
    setSimulating(true);
    const targetId = 'USR023';
    setEmployees(prev => {
      const exists = prev.find(e => e.userId === targetId);
      if (!exists) {
        const updated = [...prev, { userId: targetId, riskScore: 15, riskLevel: 'low', filesDownloaded: 3, usbConnected: false, offHoursLogin: false }];
        saveEmployees(updated);
        return updated;
      }
      return prev;
    });
    try {
      await axios.post('/api/demo/simulate-attack', { userId: targetId });
      let scores = [15, 30, 50, 70, 85, 94];
      scores.forEach((s, i) => {
        setTimeout(() => {
          setRiskTimeline(prev => [...prev.slice(-5), { time: `T+${i}`, score: s }]);
          setEmployees(prev => {
            const updated = prev.map(e => e.userId === targetId
              ? { ...e, riskScore: s, riskLevel: s >= 60 ? 'high' : s >= 30 ? 'medium' : 'low' }
              : e);
            saveEmployees(updated);
            return updated;
          });
          if (i === scores.length - 1) setSimulating(false);
        }, i * 900);
      });
    } catch {
      setSimulating(false);
    }
  };

  const high = employees.filter(e => e.riskScore >= 60).length;
  const medium = employees.filter(e => e.riskScore >= 30 && e.riskScore < 60).length;
  const low = employees.filter(e => e.riskScore < 30).length;

  return (
    <div className="dashboard">
      <div className="stats-row">
        <div className="stat-card"><div className="stat-num">{employees.length}</div><div className="stat-label">Total Users</div></div>
        <div className="stat-card red"><div className="stat-num">{high}</div><div className="stat-label">🔴 High Risk</div></div>
        <div className="stat-card yellow"><div className="stat-num">{medium}</div><div className="stat-label">🟡 Medium Risk</div></div>
        <div className="stat-card green"><div className="stat-num">{low}</div><div className="stat-label">🟢 Low Risk</div></div>
      </div>

      <div className="main-grid">
        <div className="card">
          <div className="card-header">
            <h3>Risk Score Timeline</h3>
            <button className={`sim-btn ${simulating ? 'loading' : ''}`} onClick={simulateAttack} disabled={simulating}>
              {simulating ? '⚡ Simulating...' : '▶ Simulate Attack'}
            </button>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={riskTimeline}>
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis domain={[0, 100]} stroke="#94a3b8" />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
              <Line type="monotone" dataKey="score" stroke="#ef4444" strokeWidth={2} dot={{ fill: '#ef4444' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>🚨 Live Alerts</h3>
          <div className="alert-list">
            {loginAlerts.map((a, i) => (
              <div key={`login-${i}`} className="alert-item login-alert">
                <span className="alert-user">{a.userId}</span>
                <span className="alert-score">🟢 Just Logged In</span>
                <span className="alert-reason">{a.time}</span>
              </div>
            ))}
            {alerts.length === 0 && loginAlerts.length === 0 ? (
              <div className="no-alerts">No alerts yet — click Simulate Attack</div>
            ) : alerts.map((a, i) => (
              <div key={i} className={`alert-item ${a.riskLevel}`}>
                <span className="alert-user">{a.userId}</span>
                <span className="alert-score">Score: {a.riskScore}</span>
                <span className="alert-reason">{a.reasons?.[0]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h3>👤 Employee Risk Overview</h3>
        <div className="emp-grid">
          {employees.map((emp, i) => (
            <div key={i} className={`emp-card ${emp.riskLevel} ${emp.isNew ? 'emp-new' : ''}`} onClick={() => setSelectedUser(emp)}>
              {emp.isNew && <div className="emp-new-badge">🟢 ONLINE</div>}
              <div className="emp-id">{emp.userId}</div>
              <div className="emp-score" style={{ color: RISK_COLOR(emp.riskScore) }}>{emp.riskScore}</div>
              <div className="emp-bar">
                <div className="emp-bar-fill" style={{ width: `${emp.riskScore}%`, background: RISK_COLOR(emp.riskScore) }} />
              </div>
              <div className="emp-details">
                <span>📁 {emp.filesDownloaded} files</span>
                {emp.usbConnected && <span>💾 USB</span>}
                {emp.offHoursLogin && <span>🌙 Off-hrs</span>}
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedUser && (
        <div className="modal-overlay" onClick={() => setSelectedUser(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>👤 {selectedUser.userId} — Risk Profile</h2>
            <div className="risk-score-big" style={{ color: RISK_COLOR(selectedUser.riskScore) }}>
              {selectedUser.riskScore}/100
            </div>
            <div className="risk-bar-big">
              <div style={{ width: `${selectedUser.riskScore}%`, background: RISK_COLOR(selectedUser.riskScore), height: '100%', borderRadius: 4 }} />
            </div>
            <div className="detail-list">
              {selectedUser.offHoursLogin && <div className="detail-item">🕐 Off-hours login detected <span className="pts">+25 pts</span></div>}
              {selectedUser.filesDownloaded > 20 && <div className="detail-item">📁 {selectedUser.filesDownloaded} files downloaded <span className="pts">+30 pts</span></div>}
              {selectedUser.usbConnected && <div className="detail-item">💾 USB device connected <span className="pts">+20 pts</span></div>}
            </div>
            <button className="close-btn" onClick={() => setSelectedUser(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
