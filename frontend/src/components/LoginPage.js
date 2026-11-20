import React, { useState } from 'react';

const ADMIN_CREDS = { username: 'admin', password: 'admin123' };

const getRegisteredUsers = () => {
  try { return JSON.parse(localStorage.getItem('sv_users') || '{}'); } catch { return {}; }
};

const saveUser = (userId, password) => {
  const users = getRegisteredUsers();
  users[userId] = password;
  localStorage.setItem('sv_users', JSON.stringify(users));
};

export default function LoginPage({ onLogin }) {
  const [role, setRole] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegister, setIsRegister] = useState(false);

  const handleSubmit = () => {
    setError('');
    if (role === 'admin') {
      if (username === ADMIN_CREDS.username && password === ADMIN_CREDS.password) {
        onLogin({ role: 'admin', userId: 'admin' });
      } else {
        setError('Invalid credentials');
      }
      return;
    }

    const empId = username.toUpperCase().trim();
    if (!empId || password.length < 3) {
      setError('Employee ID aur minimum 3 digit password chahiye');
      return;
    }

    const users = getRegisteredUsers();

    if (isRegister) {
      if (users[empId]) {
        setError('Ye Employee ID already registered hai');
        return;
      }
      saveUser(empId, password);
      onLogin({ role: 'employee', userId: empId });
    } else {
      if (!users[empId]) {
        setError('Employee ID registered nahi hai — pehle Register karo');
        return;
      }
      if (users[empId] !== password) {
        setError('Galat password');
        return;
      }
      onLogin({ role: 'employee', userId: empId });
    }
  };

  const reset = () => { setRole(null); setError(''); setUsername(''); setPassword(''); setIsRegister(false); };

  return (
    <div className="login-page">
      <div className="login-box">
        <div className="login-logo">🛡️</div>
        <h1 className="login-title">SentinelVoice</h1>
        <p className="login-sub">AI-Powered Insider Threat Detection</p>

        {!role ? (
          <div className="role-select">
            <p className="role-label">Select your role to continue</p>
            <button className="role-btn admin-btn" onClick={() => setRole('admin')}>
              <span className="role-icon">👨‍💼</span>
              <span className="role-text">
                <strong>Admin / SOC Analyst</strong>
                <small>Monitor all employees, view alerts</small>
              </span>
            </button>
            <button className="role-btn emp-btn" onClick={() => setRole('employee')}>
              <span className="role-icon">👤</span>
              <span className="role-text">
                <strong>Employee</strong>
                <small>View your risk profile, verify identity</small>
              </span>
            </button>
          </div>
        ) : (
          <div className="login-form">
            <div className="login-role-badge">
              {role === 'admin' ? '👨‍💼 Admin Login' : isRegister ? '📝 Employee Register' : '👤 Employee Login'}
            </div>

            <div className="input-group">
              <label>{role === 'admin' ? 'Username' : 'Employee ID'}</label>
              <input
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder={role === 'admin' ? 'admin' : 'e.g. USR045'}
                onKeyDown={e => e.key === 'Enter' && handleSubmit()}
              />
            </div>

            <div className="input-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder={role === 'admin' ? 'admin123' : 'Min 3 characters'}
                onKeyDown={e => e.key === 'Enter' && handleSubmit()}
              />
            </div>

            {error && <div className="login-error">⚠️ {error}</div>}

            <button className="login-btn" onClick={handleSubmit}>
              {role === 'admin' ? '🔐 Login' : isRegister ? '📝 Register & Login' : '🔐 Login'}
            </button>

            {role === 'employee' && (
              <button className="toggle-btn" onClick={() => { setIsRegister(!isRegister); setError(''); }}>
                {isRegister ? 'Already registered? Login' : 'New employee? Register here'}
              </button>
            )}

            <button className="back-btn" onClick={reset}>← Back</button>

            {role === 'admin' && (
              <div className="demo-hint">Demo: <strong>admin</strong> / <strong>admin123</strong></div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
