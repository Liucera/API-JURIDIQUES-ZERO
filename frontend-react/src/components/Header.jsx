import React from 'react'

function Header({ health }) {
  const getStatus = () => {
    if (!health) return { text: 'Offline', class: 'offline' }
    if (health.status === 'ok') return { text: 'Online', class: 'online' }
    return { text: 'Degradado', class: 'warning' }
  }

  const status = getStatus()

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">JZ</span>
          <div>
            <h1>Juridiques Zero</h1>
            <p className="subtitle">Simplificacao de documentos juridicos com IA</p>
          </div>
        </div>
        <div className="status">
          <span className={`status-badge ${status.class}`}>
            {status.text}
          </span>
          {health?.ia?.gemini_configurado && (
            <span className="gemini-badge">Gemini</span>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
