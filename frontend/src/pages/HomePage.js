import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Search, Sparkles, Zap, Brain, FileText, TrendingUp, Loader2 } from 'lucide-react';
import axios from 'axios';
import './HomePage.css';

const HomePage = () => {
  const [topic, setTopic] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/research', {
        topic: topic.trim(),
        max_results: maxResults
      });

      // Navigate to research detail page
      navigate(`/research/${response.data.research_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start research. Please try again.');
      setIsLoading(false);
    }
  };

  const exampleTopics = [
    'Latest advances in quantum computing',
    'Impact of AI on healthcare',
    'Sustainable energy solutions 2025',
    'Future of space exploration',
    'Blockchain technology applications'
  ];

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Google Gemini 2.5 Flash for deep insights'
    },
    {
      icon: Search,
      title: 'Web Research',
      description: 'Real-time data from trusted sources'
    },
    {
      icon: FileText,
      title: 'PDF Reports',
      description: 'Professional formatted documents'
    },
    {
      icon: TrendingUp,
      title: 'Key Findings',
      description: 'Extracted insights and trends'
    }
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <motion.div 
        className="hero-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <motion.div 
          className="hero-badge"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <Sparkles size={16} />
          <span>Powered by Google Gemini 2.5 Flash</span>
        </motion.div>

        <motion.h1 
          className="hero-title"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Unlock Knowledge with
          <br />
          <span className="gradient-text">AI Research Agent</span>
        </motion.h1>

        <motion.p 
          className="hero-subtitle"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          Conduct deep research on any topic in seconds. Get AI-powered insights,
          <br />
          key findings, and professional PDF reports instantly.
        </motion.p>

        {/* Search Form */}
        <motion.form 
          className="search-form"
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className="search-input-wrapper glow-border">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              className="search-input"
              placeholder="What would you like to research?"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={isLoading}
            />
            <div className="search-controls">
              <select
                className="max-results-select"
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
                disabled={isLoading}
              >
                <option value={5}>5 sources</option>
                <option value={10}>10 sources</option>
                <option value={15}>15 sources</option>
                <option value={20}>20 sources</option>
              </select>
            </div>
          </div>

          <motion.button
            type="submit"
            className="search-button"
            disabled={isLoading || !topic.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isLoading ? (
              <>
                <Loader2 className="spin-icon" size={20} />
                <span>Researching...</span>
              </>
            ) : (
              <>
                <Zap size={20} />
                <span>Start Research</span>
              </>
            )}
          </motion.button>
        </motion.form>

        {error && (
          <motion.div 
            className="error-message"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {error}
          </motion.div>
        )}

        {/* Example Topics */}
        <motion.div 
          className="example-topics"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <span className="example-label">Try these examples:</span>
          <div className="example-tags">
            {exampleTopics.map((example, index) => (
              <motion.button
                key={index}
                className="example-tag"
                onClick={() => setTopic(example)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
              >
                {example}
              </motion.button>
            ))}
          </div>
        </motion.div>
      </motion.div>

      {/* Features Section */}
      <motion.div 
        className="features-section"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <h2 className="features-title">Why Choose AI Research Agent?</h2>
        <div className="features-grid">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                className="feature-card glass-effect glow-border"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 + index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="feature-icon">
                  <Icon size={24} />
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </div>
  );
};

export default HomePage;
