import React, { useState } from 'react'

function PromptForm({ onSubmit, loading }) {
  const [texto, setTexto] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (texto.trim().length >= 50) {
      onSubmit(texto)
    }
  }

  return (
    <form className="prompt-form" onSubmit={handleSubmit}>
      <label className="form-label">
        Digite um texto juridico para simplificar
      </label>
      <textarea
        className="form-textarea"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Cole o texto aqui..."
        rows={8}
      />
      <div className="form-meta">
        <span className={`char-count ${texto.length >= 50 ? 'ok' : ''}`}>
          {texto.length} caracteres {texto.length < 50 && '(minimo 50)'}
        </span>
      </div>
      <button
        type="submit"
        className="btn-primary"
        disabled={loading || texto.length < 50}
      >
        {loading ? 'Processando...' : 'Simplificar'}
      </button>
    </form>
  )
}

export default PromptForm
