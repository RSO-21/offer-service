from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

DATABASE_URL = (
    f"postgresql://{settings.pg_user}:{settings.pg_password}"
    f"@{settings.pg_host}:{settings.pg_port}/{settings.pg_database}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session(schema: str = None):
    session = SessionLocal()
    try:
        # Set search_path for this session
        session.execute(text(f"SET search_path TO {schema}"))
        yield session
    finally:
        session.close()