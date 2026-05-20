CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    nome_arquivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    texto_original TEXT,
    resumo TEXT,
    prazos JSONB DEFAULT '[]',
    acoes JSONB DEFAULT '[]',
    modelo_ia VARCHAR(100),
    tempo_ms INTEGER,
    cache_hit BOOLEAN DEFAULT FALSE,
    sigilo VARCHAR(20) DEFAULT 'interno',
    criado_em TIMESTAMP DEFAULT NOW(),
    processado_em TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_documentos_criado ON documentos(criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_documentos_tipo ON documentos(tipo);
CREATE INDEX IF NOT EXISTS idx_documentos_modelo ON documentos(modelo_ia);

CREATE TABLE IF NOT EXISTS metricas_diarias (
    data DATE PRIMARY KEY,
    total_documentos INTEGER DEFAULT 0,
    tempo_medio_ms INTEGER DEFAULT 0,
    cache_hits INTEGER DEFAULT 0,
    cache_misses INTEGER DEFAULT 0,
    modelos_usados JSONB DEFAULT '{}'
);

CREATE OR REPLACE FUNCTION atualizar_metricas()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO metricas_diarias (data, total_documentos, tempo_medio_ms)
    VALUES (CURRENT_DATE, 1, NEW.tempo_ms)
    ON CONFLICT (data) DO UPDATE SET
        total_documentos = metricas_diarias.total_documentos + 1,
        tempo_medio_ms = (metricas_diarias.tempo_medio_ms * metricas_diarias.total_documentos + NEW.tempo_ms) / (metricas_diarias.total_documentos + 1);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_metricas
AFTER INSERT ON documentos
FOR EACH ROW
EXECUTE FUNCTION atualizar_metricas();
