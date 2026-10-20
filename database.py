from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Banco SQLite local (arquivo radar.db) - nao precisa de Docker nem de Postgres
engine = create_engine('sqlite:///radar.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Concurso(Base):
    __tablename__ = 'concursos'

    # Link do edital como chave primaria (evita duplicados)
    link = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    status = Column(String)

    # Controla se o n8n ja enviou a notificacao (WhatsApp/email/etc)
    notificado_whatsapp = Column(Boolean, default=False)

    # Auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    notificado_em = Column(DateTime, nullable=True)


# Cria as tabelas no banco se nao existirem
Base.metadata.create_all(engine)


def salvar_concursos(lista_concursos):
    """Salva concursos novos no banco e devolve apenas os que realmente foram inseridos."""
    session = Session()
    concursos_novos = []

    for item in lista_concursos:
        existe = session.query(Concurso).filter_by(link=item['link']).first()

        if not existe:
            novo_concurso = Concurso(
                link=item['link'],
                titulo=item['titulo'],
                status=item['status']
            )
            session.add(novo_concurso)
            concursos_novos.append(item)

    session.commit()
    session.close()
    return concursos_novos


def marcar_notificado(link):
    """Marca um concurso como ja notificado (chamado pelo n8n apos enviar a mensagem)."""
    session = Session()
    concurso = session.query(Concurso).filter_by(link=link).first()
    if concurso and not concurso.notificado_whatsapp:
        concurso.notificado_whatsapp = True
        concurso.notificado_em = datetime.utcnow()
        session.commit()
        session.close()
        return True
    session.close()
    return False


def listar_nao_notificados(limit=50):
    """Lista concursos ainda nao notificados (util para o n8n consultar via SQL/diretamente no SQLite)."""
    session = Session()
    rows = (session.query(Concurso)
            .filter_by(notificado_whatsapp=False)
            .order_by(Concurso.criado_em.desc())
            .limit(limit)
            .all())
    resultado = [
        {'link': r.link, 'titulo': r.titulo, 'status': r.status, 'criado_em': r.criado_em.isoformat() if r.criado_em else None}
        for r in rows
    ]
    session.close()
    return resultado
