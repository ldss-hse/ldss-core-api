from pathlib import Path

from dynaconf import FlaskDynaconf
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from core_api.constants import ROOT_PATH

Base = None


def get_database_session_for_flask() -> Session:
    return get_database_session_for_flask.db_session


def get_db_for_asynchronous_task() -> scoped_session:
    class FakeFlaskApp:
        def __init__(self):
            self.root_path = str(Path(__file__).parent.parent.parent)
            self.config = {}
    fakeApp = FakeFlaskApp()
    FlaskDynaconf(app=fakeApp, settings_files=["settings.toml", ".secrets.toml"])
    db_engine = create_engine(fakeApp.config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    return scoped_session(sessionmaker(autocommit=False, bind=db_engine))


def init_db(app: Flask):
    db_dir = Path('.') / app.config.DATABASE_DIR
    db_dir.mkdir(parents=True, mode=0o777, exist_ok=True)

    engine = create_engine(app.config.SQLALCHEMY_DATABASE_URI)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    get_database_session_for_flask.db_session = db_session

    global Base
    Base = declarative_base()
    Base.query = db_session.query_property()

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # noinspection PyUnresolvedReferences
    import core_api.main.models

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
