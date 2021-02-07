from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine('sqlite:///diedb.db', echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@staticmethod
def close_connection():
    engine.dispose()