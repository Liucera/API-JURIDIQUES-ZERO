import os
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

"""
Módulo de configuração do Banco de Dados.
Este arquivo gerencia a conexão com o PostgreSQL e define a estrutura das tabelas usando SQLAlchemy.
"""

# Busca a URL de conexão com o banco de dados a partir das variáveis de ambiente (.env)
DATABASE_URL = os.getenv("DATABASE_URL")

# Criação do motor de conexão do SQLAlchemy
# O 'engine' é o ponto de partida para qualquer comunicação com o banco de dados
engine = create_engine(DATABASE_URL)

# Configuração da sessão local do banco de dados
# SessionLocal será instanciada para cada requisição para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para a criação dos modelos (tabelas) do SQLAlchemy
Base = declarative_base()

class Documento(Base):
    """
    Modelo representativo da tabela 'documentos'.
    Armazena os dados extraídos dos PDFs e as informações de processamento.
    """
    __tablename__ = "documentos"

    # Identificador único (Chave Primária)
    id = Column(Integer, primary_key=True, index=True)

    # Nome original do arquivo PDF carregado
    nome_arquivo = Column(String)

    # Classificação do documento (ex: Jurídico, Logística, Administrativo)
    categoria = Column(String)

    # Conteúdo textual bruto extraído do PDF via PyPDF2
    conteudo_extraido = Column(Text)

    # Data e hora em que o processamento foi realizado (UTC)
    data_processamento = Column(DateTime, default=datetime.utcnow)

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas no código.
    Deve ser chamada na inicialização da aplicação (app/main.py).
    """
    Base.metadata.create_all(bind=engine)
