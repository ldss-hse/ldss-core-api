"""
A module for configuring DB connection
"""
import platform
from pathlib import Path

from dynaconf import FlaskDynaconf
from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from core_api.constants import CORE_PATH

BASE = None


def get_database_session_for_flask() -> Session:
    """get session instance for a Flask application"""
    return get_database_session_for_flask.db_session


def get_db_for_asynchronous_task() -> scoped_session:
    """
    Get session instance for any other application,
    for example for asynchronous tasks executor
    """

    class FakeFlaskApp:
        """
        Fake class to instantiate FlaskDynaconf in the same way as
        for standard Flask applications
        """

        def __init__(self):
            self.root_path = str(Path(__file__).parent.parent.parent)
            self.config = {}

    fake_app = FakeFlaskApp()
    FlaskDynaconf(app=fake_app, settings_files=["settings.toml", ".secrets.toml"])

    root_path = Path(__file__).parent.parent
    uri = fake_app.config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', f'sqlite:///{str(root_path)}/')
    # pylint: disable=no-member
    db_engine = create_engine(url=uri, poolclass=NullPool)

    return scoped_session(sessionmaker(autocommit=False, bind=db_engine))


def init_db(app: Flask):
    """
    initializing database for a running Flask application
    :param app: Flask instance
    """
    db_dir = CORE_PATH.parent / app.config.DATABASE_DIR
    db_dir.mkdir(parents=True, mode=0o777, exist_ok=True)

    db_uri = app.config.SQLALCHEMY_DATABASE_URI.replace('<PATH>', f'{CORE_PATH.parent}')
    if platform.system() == 'Windows':
        db_uri = 'sqlite:///' + db_uri[10:].replace('\\', f'\\\\')
        db_uri = 'sqlite:///' + db_uri[10:].replace('/', f'\\\\')
    print(f'Creating DB in {db_uri}')

    engine = create_engine(db_uri)

    db_session: scoped_session = scoped_session(sessionmaker(autocommit=False,
                                                             autoflush=False,
                                                             bind=engine))
    get_database_session_for_flask.db_session = db_session

    # pylint: disable=global-statement
    global BASE
    BASE = declarative_base()
    BASE.query = db_session.query_property()

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # noinspection PyUnresolvedReferences

    # pylint: disable=import-outside-toplevel,unused-import
    import core_api.main.models

    BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)
