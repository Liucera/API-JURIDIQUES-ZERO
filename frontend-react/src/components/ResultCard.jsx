import React from 'react'

function ResultCard({ result }) {
  return (
    <div className="result-card">
      <div className="result-header">
        <h3>Processado em {Math.round(result.tempo_ms / 1000)}s</h3>
        <div className="result-meta">
          <span className="model-badge">{result.modelo}</span>
          {result.cache && <span className="cache-badge">Cache</span>}
          <span className="cost-badge">R$ 0,00</span>
        </div>
      </div>

      <div className="result-section resumo">
        <h4>Resumo</h4>
        <p>{result.resumo}</p>
      </div>

      {result.prazos && result.prazos.length > 0 && (
        <div className="result-section prazos">
          <h4>Prazos Identificados</h4>
          <ul>
            {result.prazos.map((prazo, i) => (
              <li key={i}>{prazo}</li>
            ))}
          </ul>
        </div>
      )}

      {result.acoes && result.acoes.length > 0 && (
        <div className="result-section acoes">
          <h4>Acoes Necessarias</h4>
          <ul>
            {result.acoes.map((acao, i) => (
              <li key={i}>{acao}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="result-footer">
        <span>Documento ID: #{result.id}</span>
      </div>
    </div>
  )
}

export default ResultCard
