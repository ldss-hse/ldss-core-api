from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core_api.constants import ROOT_PATH

Base = None


def get_database_session_for_flask() -> SQLAlchemy:
    return get_database_session_for_flask.db_session


def init_db(app: Flask):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import yourapplication.models



    # engine = create_engine('sqlite:////tmp/app.db')
    # engine = create_engine('sqlite:////Users/demidovs/Documents/projects/1_hse/ldss-core-api/db/main.db')
    engine = create_engine(app.config.SQLALCHEMY_DATABASE_URI)
    # db_file_path = Path(app.config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))
    # print(db_file_path.stat().st_mode)
    # db_file_path.chmod(0o777)
    # print(db_file_path.stat().st_mode)

    import sqlalchemy.engine.url as url
    a = url.make_url(app.config.SQLALCHEMY_DATABASE_URI)
    print(a)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    get_database_session_for_flask.db_session = db_session

    global Base
    Base = declarative_base()
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
