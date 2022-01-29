from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from sql.models import Base


class DBManager:
    """Support class that abstracts access to postgres database."""
    def __init__(self, db_host, db_port, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        
        self.engine = None

    def _connect(self):
        print(f"Connecting to Postgres at {self.db_host}:{self.db_port}...")
        uri = (f'postgresql+psycopg2://{self.db_user}:{self.db_password}@'
               f'{self.db_host}:{self.db_port}/{self.db_name}')

        self.engine = create_engine(
            uri,
            pool_pre_ping=True,  # pings before queries to check if connection alive.
            pool_recycle=300,  # refreshes all connections older than 5 mins.
        )
        self.engine: Engine

        print(f"Connected to Postgres at {self.db_host}:{self.db_port}.")

        self._init_schema()

    def _init_schema(self):
        """Creates registered tables, only creates non-existing tables.

        If table already exists, nothing happens.
        """
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[None]:
        """Sessions that enable transactional operations.

        Details about sessions can be found here:
        https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
        """
        if self.engine is None:
            self._connect()

        db_session = scoped_session(sessionmaker(bind=self.engine)) # a session factory object
  
        try:
            yield db_session
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
