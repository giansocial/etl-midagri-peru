from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.settings import DB_CONFIG

_engine = None


def get_connection_url() -> str:
    return (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_connection_url(),
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
    return _engine


def get_session() -> Session:
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    return session_factory()


def test_connection() -> bool:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False
