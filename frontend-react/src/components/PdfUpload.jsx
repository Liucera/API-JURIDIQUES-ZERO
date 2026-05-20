import React, { useState, useCallback } from 'react'

function PdfUpload({ onUpload, loading }) {
  const [dragActive, setDragActive] = useState(false)
  const [file, setFile] = useState(null)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }, [])

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = () => {
    if (file) {
      onUpload(file)
    }
  }

  return (
    <div className="pdf-upload">
      <div
        className={`drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="file-input"
          id="pdf-input"
        />
        <label htmlFor="pdf-input" className="drop-label">
          {file ? (
            <>
              <span className="file-name">{file.name}</span>
              <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
            </>
          ) : (
            <>
              <p>Arraste um PDF aqui ou clique para selecionar</p>
              <span className="hint">Tamanho maximo recomendado: 50 paginas</span>
            </>
          )}
        </label>
      </div>
      
      {file && (
        <button
          className="btn-primary"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? 'Processando...' : 'Processar PDF'}
        </button>
      )}
    </div>
  )
}

export default PdfUpload
