import React, { useState } from 'react';
import './App.css';

function App() {
  const [cvText, setCvText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [userResponse, setUserResponse] = useState('');
  const [interviewMessage, setInterviewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleCvUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload-cv', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setCvText(data.cv_text);
    } catch (error) {
      console.error('Error uploading CV:', error);
    }
  };

  const handleJdUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload-jd', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setJobDescription(data.job_description);
    } catch (error) {
      console.error('Error uploading job description:', error);
    }
  };

  const startInterview = async () => {
    if (!cvText || !jobDescription) {
      alert('Please upload both CV and job description first');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/start-interview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cv_text: cvText,
          job_description: jobDescription,
          user_response: userResponse,
        }),
      });
      const data = await response.json();
      setInterviewMessage(data.message);
      setUserResponse('');
    } catch (error) {
      console.error('Error starting interview:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>AI Interview Coach</h1>
      
      <div className="upload-section">
        <div>
          <h3>Upload CV</h3>
          <input type="file" onChange={handleCvUpload} accept=".txt,.pdf,.doc,.docx" />
        </div>
        
        <div>
          <h3>Upload Job Description</h3>
          <input type="file" onChange={handleJdUpload} accept=".txt,.pdf,.doc,.docx" />
        </div>
      </div>

      <div className="interview-section">
        {interviewMessage && (
          <div className="interview-message">
            <h3>Interviewer:</h3>
            <p>{interviewMessage}</p>
          </div>
        )}

        <div className="response-section">
          <textarea
            value={userResponse}
            onChange={(e) => setUserResponse(e.target.value)}
            placeholder="Type your response here..."
            rows="4"
          />
          <button 
            onClick={startInterview}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Send Response'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
