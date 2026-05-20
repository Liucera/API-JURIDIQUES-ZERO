import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import PromptForm from './components/PromptForm'
import PdfUpload from './components/PdfUpload'
import ResultCard from './components/ResultCard'
import Metrics from './components/Metrics'

const API_URL = 'http://localhost:8000'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [health, setHealth] = useState(null)
  const [activeTab, setActiveTab] = useState('prompt')
  const [useGemini, setUseGemini] = useState(false)

  useEffect(() => {
    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkHealth = async () => {
    try {
      const res = await axios.get(`${API_URL}/health`)
      setHealth(res.data)
    } catch (err) {
      setHealth(null)
    }
  }

  const handlePromptSubmit = async (texto) => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const res = await axios.post(`${API_URL}/simplificar`, {
        texto,
        tipo: 'prompt',
        usar_gemini: useGemini
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao processar')
    } finally {
      setLoading(false)
    }
  }

  const handlePdfUpload = async (file) => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const res = await axios.post(`${API_URL}/upload?usar_gemini=${useGemini}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao processar PDF')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <Header health={health} />
      
      <main className="main">
        <div className="container">
          <div className="gemini-toggle">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={useGemini}
                onChange={(e) => setUseGemini(e.target.checked)}
                disabled={!health?.ia?.gemini_configurado}
              />
              <span className="toggle-text">
                Usar Gemini (mais rapido)
                {!health?.ia?.gemini_configurado && ' - API key nao configurada'}
              </span>
            </label>
          </div>

          <div className="tabs">
            <button
              className={`tab ${activeTab === 'prompt' ? 'active' : ''}`}
              onClick={() => setActiveTab('prompt')}
            >
              Prompt Direto
            </button>
            <button
              className={`tab ${activeTab === 'pdf' ? 'active' : ''}`}
              onClick={() => setActiveTab('pdf')}
            >
              Upload PDF
            </button>
            <button
              className={`tab ${activeTab === 'metrics' ? 'active' : ''}`}
              onClick={() => setActiveTab('metrics')}
            >
              Metricas
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'prompt' && (
              <PromptForm onSubmit={handlePromptSubmit} loading={loading} />
            )}
            {activeTab === 'pdf' && (
              <PdfUpload onUpload={handlePdfUpload} loading={loading} />
            )}
            {activeTab === 'metrics' && (
              <Metrics />
            )}
          </div>

          {error && (
            <div className="error-card">
              {error}
            </div>
          )}

          {result && !loading && (
            <ResultCard result={result} />
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Juridiques Zero v2.1 | IA Hibrida | Custo IA: {useGemini ? 'Variavel' : 'R$ 0,00'}</p>
      </footer>
    </div>
  )
}

export default App
