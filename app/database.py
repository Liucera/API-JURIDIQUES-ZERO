import os
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Busca a URL do banco que você colocou no .env
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição da Tabela (O seu arquivo digital)
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String)
    categoria = Column(String)  # Jurídico, Logística, etc.
    conteudo_extraido = Column(Text)
    data_processamento = Column(DateTime, default=datetime.utcnow)

# Função para criar as tabelas no banco
def init_db():
    Base.metadata.create_all(bind=engine)
