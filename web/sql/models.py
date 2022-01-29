from sqlalchemy import JSON, Column, Float, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Experiment(Base):
    """Defines schema of "experiments" table."""
    __tablename__ = "experiments"
    experiment_name = Column("Experiment Name", String(128), primary_key=True)
    learning_rate = Column("Loss", JSON)
    momentum = Column("Momentum", Float)
    loss = Column("Learning Rate", Float)
