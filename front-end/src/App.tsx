import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import ApplicantPage from './pages/ApplicantPage';
import AdminPage from './pages/AdminPage';

// Landing Page Component
const LandingPage = () => {
  const navigate = useNavigate();

  const buttonStyle: React.CSSProperties = {
    display: 'block',
    width: '200px',
    padding: '20px',
    margin: '20px auto',
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    transition: 'background-color 0.3s ease',
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f0f0',
  };

  const handleApplicantClick = () => {
    navigate('/applicant');
  };

  const handleAdminClick = () => {
    navigate('/admin');
  };

  return (
    <div style={containerStyle}>
      <button style={buttonStyle} onClick={handleApplicantClick}>
        Applicant
      </button>
      <button style={{ ...buttonStyle, backgroundColor: '#28a745' }} onClick={handleAdminClick}>
        Admin
      </button>
    </div>
  );
};


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/applicant" element={<ApplicantPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </Router>
  );
};

export default App;