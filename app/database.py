import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


if 'DATABASE_URL' in os.environ:
    print "POSTGRES FOUND"
    engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
else:
    engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.model

    # drop all to make a fresh database for testing
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)