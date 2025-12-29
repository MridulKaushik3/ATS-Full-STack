// frontend/src/components/ResumeEvaluator.jsx

import { useState } from 'react';
import axios from 'axios';
import './ResumeEvaluator.css';

const ResumeEvaluator = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
    } else {
      setError('Please upload a PDF file');
      setResumeFile(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!resumeFile || !jobDescription) {
      setError('Please provide both resume and job description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/evaluate/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to evaluate resume. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setResumeFile(null);
    setJobDescription('');
    setResult(null);
    setError('');
  };

  return (
    <div className="resume-evaluator">
      <div className="container">
        <h1>🎯 ATS Resume Evaluator</h1>
        <p className="subtitle">Check how well your resume matches the job description</p>

        {!result ? (
          <form onSubmit={handleSubmit} className="upload-form">
            <div className="form-group">
              <label htmlFor="resume">Upload Resume (PDF)</label>
              <input
                type="file"
                id="resume"
                accept=".pdf"
                onChange={handleFileChange}
                disabled={loading}
              />
              {resumeFile && (
                <p className="file-name">Selected: {resumeFile.name}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="jobDescription">Job Description</label>
              <textarea
                id="jobDescription"
                rows="10"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                disabled={loading}
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <button 
              type="submit" 
              className="submit-btn"
              disabled={loading || !resumeFile || !jobDescription}
            >
              {loading ? 'Analyzing...' : 'Evaluate Resume'}
            </button>
          </form>
        ) : (
          <div className="results">
            <div className="score-card">
              <h2>ATS Score</h2>
              <div className="score-circle">
                <span className="score-number">{result.score}%</span>
              </div>
              <p className="score-label">
                {result.score >= 80 ? 'Excellent Match! 🎉' : 
                 result.score >= 60 ? 'Good Match 👍' : 
                 result.score >= 40 ? 'Needs Improvement 📝' : 
                 'Poor Match ⚠️'}
              </p>
            </div>

            {result.keywords_missing && (
              <div className="keywords-section">
                <h3>Missing Keywords</h3>
                <div className="keywords-list">
                  {result.keywords_missing.split('\n').filter(k => k.trim()).map((keyword, index) => (
                    <span key={index} className="keyword-tag">
                      {keyword.replace(/^-\s*/, '')}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {result.final_thoughts && (
              <div className="thoughts-section">
                <h3>Final Thoughts</h3>
                <p>{result.final_thoughts}</p>
              </div>
            )}

            <button onClick={resetForm} className="reset-btn">
              Evaluate Another Resume
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeEvaluator;