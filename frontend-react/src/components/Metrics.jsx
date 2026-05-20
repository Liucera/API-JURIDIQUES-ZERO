import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function Metrics() {
  const [metrics, setMetrics] = useState(null)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 10000)
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const res = await axios.get(`${API_URL}/metricas`)
      setMetrics(res.data)
    } catch (err) {
      console.error('Erro ao buscar metricas:', err)
    }
  }

  if (!metrics) return <div className="loading">Carregando metricas...</div>

  return (
    <div className="metrics">
      <h3>Metricas do Sistema</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <span className="metric-value">{metrics.total_documentos}</span>
          <span className="metric-label">Total Documentos</span>
        </div>
        <div className="metric-card">
          <span className="metric-value">{Math.round(metrics.tempo_medio / 1000)}s</span>
          <span className="metric-label">Tempo Medio</span>
        </div>
        <div className="metric-card">
          <span className="metric-value">{Math.round(metrics.taxa_cache * 100)}%</span>
          <span className="metric-label">Taxa Cache</span>
        </div>
        <div className="metric-card">
          <span className="metric-value">{metrics.custo_ia_mes}</span>
          <span className="metric-label">Custo IA/Mes</span>
        </div>
      </div>
      
      {metrics.gemini_disponivel && (
        <div className="gemini-status">
          Gemini configurado e disponivel
        </div>
      )}
    </div>
  )
}

export default Metrics
