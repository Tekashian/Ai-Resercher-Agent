import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Download, ExternalLink, CheckCircle, Loader2, AlertCircle, FileText } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './ResearchPage.css';

const ResearchPage = () => {
  const { id } = useParams();
  const [research, setResearch] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);

  const fetchResearch = async () => {
    try {
      const response = await axios.get(`/research/${id}`);
      setResearch(response.data);
      setIsLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load research');
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchResearch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const generatePdfReport = async () => {
    setIsGeneratingPdf(true);
    try {
      const response = await axios.post('/report', {
        research_id: id,
        include_sources: true
      });

      // Download the PDF
      window.open(response.data.download_url, '_blank');
    } catch (err) {
      alert('Failed to generate PDF report');
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <Loader2 className="spin-icon" size={48} />
        <p>Loading research...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <AlertCircle size={48} />
        <p>{error}</p>
        <Link to="/" className="back-button">
          <ArrowLeft size={20} />
          Back to Home
        </Link>
      </div>
    );
  }

  return (
    <motion.div 
      className="research-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="research-header">
        <Link to="/" className="back-link">
          <ArrowLeft size={20} />
          <span>Back</span>
        </Link>

        <motion.button
          className="pdf-button"
          onClick={generatePdfReport}
          disabled={isGeneratingPdf}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isGeneratingPdf ? (
            <>
              <Loader2 className="spin-icon" size={20} />
              <span>Generating...</span>
            </>
          ) : (
            <>
              <Download size={20} />
              <span>Download PDF</span>
            </>
          )}
        </motion.button>
      </div>

      {/* Topic & Status */}
      <motion.div 
        className="research-title-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="status-badge success">
          <CheckCircle size={16} />
          <span>Completed</span>
        </div>
        <h1 className="research-title">{research.metadata.topic}</h1>
        <p className="research-date">
          Research ID: {research.research_id} • {new Date(research.metadata.created_at).toLocaleString()}
        </p>
      </motion.div>

      {/* Summary */}
      {research.metadata.summary && (
        <motion.div 
          className="research-section glass-effect"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="section-title">
            <FileText size={24} />
            Summary
          </h2>
          <div className="summary-content">
            <ReactMarkdown>{research.metadata.summary}</ReactMarkdown>
          </div>
        </motion.div>
      )}

      {/* Key Findings */}
      {research.metadata.key_findings && research.metadata.key_findings.length > 0 && (
        <motion.div 
          className="research-section glass-effect"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="section-title">
            <CheckCircle size={24} />
            Key Findings
          </h2>
          <div className="key-findings-grid">
            {research.metadata.key_findings.map((finding, index) => (
              <motion.div
                key={index}
                className="finding-card"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
              >
                <div className="finding-number">{index + 1}</div>
                <p className="finding-text">{finding}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Detailed Analysis */}
      {research.metadata.detailed_analysis && (
        <motion.div 
          className="research-section glass-effect"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className="section-title">Detailed Analysis</h2>
          <div className="analysis-content">
            <ReactMarkdown>{research.metadata.detailed_analysis}</ReactMarkdown>
          </div>
        </motion.div>
      )}

      {/* Sources */}
      {research.metadata.sources && research.metadata.sources.length > 0 && (
        <motion.div 
          className="research-section glass-effect"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <h2 className="section-title">
            <ExternalLink size={24} />
            Sources ({research.metadata.sources.length})
          </h2>
          <div className="sources-list">
            {research.metadata.sources.map((source, index) => (
              <motion.a
                key={index}
                href={source}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + index * 0.05 }}
                whileHover={{ x: 5 }}
              >
                <ExternalLink size={16} />
                <span className="source-url">{source}</span>
              </motion.a>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ResearchPage;
