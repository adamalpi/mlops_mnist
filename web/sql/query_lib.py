import pandas as pd
from sqlalchemy.orm import Session

from sql.df_management import DBManager
from sql.models import Experiment


def get_all_experiments(db: DBManager) -> pd.DataFrame:
    """Retrieves full table "experiments".

    Args:
        db: manager object that supports connection session creation.

    Returns:
        pd.DataFrame: table's content.
    """
    with db.session() as s:
        s: Session

        experiments_query = s.query(Experiment)

        df = pd.read_sql_query(experiments_query.statement, s.bind)

        return df
