import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { History as HistoryIcon, FileText, Calendar, ArrowRight, Loader2, AlertCircle } from 'lucide-react';
import axios from 'axios';
import './HistoryPage.css';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/history?limit=50');
      setHistory(response.data.research);
      setIsLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load history');
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <Loader2 className="spin-icon" size={48} />
        <p>Loading history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <AlertCircle size={48} />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <motion.div 
      className="history-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <motion.div 
        className="history-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="history-title-section">
          <div className="history-icon">
            <HistoryIcon size={32} />
          </div>
          <div>
            <h1 className="history-title">Research History</h1>
            <p className="history-subtitle">
              {history.length} {history.length === 1 ? 'research' : 'researches'} found
            </p>
          </div>
        </div>
      </motion.div>

      {/* History List */}
      {history.length === 0 ? (
        <motion.div 
          className="empty-state glass-effect"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <FileText size={64} />
          <h2>No research history yet</h2>
          <p>Start your first research to see it here</p>
          <Link to="/" className="cta-button">
            Start Research
          </Link>
        </motion.div>
      ) : (
        <div className="history-grid">
          {history.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Link
                to={`/research/${item.id}`}
                className="history-card glass-effect glow-border"
              >
                <div className="history-card-header">
                  <div className="history-card-icon">
                    <FileText size={20} />
                  </div>
                  <div className="history-card-date">
                    <Calendar size={14} />
                    <span>{new Date(item.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                <h3 className="history-card-title">{item.topic}</h3>

                {item.summary && (
                  <p className="history-card-summary">
                    {item.summary.slice(0, 150)}
                    {item.summary.length > 150 ? '...' : ''}
                  </p>
                )}

                <div className="history-card-footer">
                  <div className="history-card-stats">
                    <span className="stat">
                      {item.key_findings?.length || 0} findings
                    </span>
                    <span className="stat-separator">•</span>
                    <span className="stat">
                      {item.sources?.length || 0} sources
                    </span>
                  </div>
                  <div className="history-card-arrow">
                    <ArrowRight size={20} />
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default HistoryPage;
