import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import DuressPanel from './components/DuressPanel';
import ModelStats from './components/ModelStats';
import EmployeeDashboard from './components/EmployeeDashboard';
import './App.css';

const socket = io('http://localhost:5000');

export default function App() {
  const [user, setUser] = useState(null); 
  const [page, setPage] = useState('dashboard');
  const [alerts, setAlerts] = useState([]);
  const [duressAlert, setDuressAlert] = useState(null);
  const [liveRisk, setLiveRisk] = useState({});

  useEffect(() => {
    socket.on('new-alert', (alert) => {
      setAlerts(prev => [alert, ...prev].slice(0, 20));
    });
    socket.on('duress-alert', (alert) => {
      setDuressAlert(alert);
      setTimeout(() => setDuressAlert(null), 8000);
    });
    socket.on('risk-update', (data) => {
      setLiveRisk(prev => ({ ...prev, [data.userId]: data.riskScore }));
    });
    return () => socket.off();
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setPage('dashboard');
    if (userData.role === 'employee') {
      const saved = localStorage.getItem('sv_employees');
      const list = saved ? JSON.parse(saved) : [];
      const existing = list.find(e => e.userId === userData.userId);
      const empData = existing || { userId: userData.userId, riskScore: 10, riskLevel: 'low', filesDownloaded: 0, usbConnected: false, offHoursLogin: false };
      if (!existing) {
        list.push(empData);
        localStorage.setItem('sv_employees', JSON.stringify(list));
      }
      socket.emit('employee-login', { userId: userData.userId, ...empData, timestamp: new Date() });
    }
  };

  const addEmployeeToAdmin = (empData) => {
    setAlerts(prev => [{ userId: empData.userId, riskScore: empData.riskScore, riskLevel: 'low', reasons: ['Employee logged in'], timestamp: new Date() }, ...prev].slice(0, 20));
  };

  const handleLogout = () => {
    setUser(null);
    setPage('dashboard');
    setAlerts([]);
    setDuressAlert(null);
  };

  if (!user) return <LoginPage onLogin={handleLogin} />;


  if (user.role === 'employee') {
    return (
      <div className="app">
        <EmployeeDashboard userId={user.userId} onLogout={handleLogout} socket={socket} />
      </div>
    );
  }

  return (
    <div className="app">
      {duressAlert && (
        <div className="duress-banner">
          🚨 DURESS ALERT: {duressAlert.userId} NEEDS IMMEDIATE HELP! 🚨
        </div>
      )}
      <nav className="navbar">
        <div className="logo">🛡️ SentinelVoice</div>
        <div className="nav-links">
          <button className={page === 'dashboard' ? 'active' : ''} onClick={() => setPage('dashboard')}>Dashboard</button>
          <button className={page === 'duress' ? 'active' : ''} onClick={() => setPage('duress')}>Verify / Duress</button>
          <button className={page === 'stats' ? 'active' : ''} onClick={() => setPage('stats')}>Model Stats</button>
        </div>
        <div className="nav-right">
          <span className="nav-user">👨💼 Admin</span>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </nav>
      <main>
        {page === 'dashboard' && <Dashboard alerts={alerts} liveRisk={liveRisk} socket={socket} />}
        {page === 'duress' && <DuressPanel socket={socket} />}
        {page === 'stats' && <ModelStats />}
      </main>
    </div>
  );
}
