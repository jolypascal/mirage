import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/generate', { text: prompt });
      setImage(response.data.image);
    } catch (error) {
      console.error('Error generating image:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Text-to-Image Generator</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt (e.g., A futuristic city)"
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Image'}
      </button>
      {image && <img src={image} alt="Generated" style={{ maxWidth: '100%', marginTop: '20px' }} />}
    </div>
  );
}

export default App;
