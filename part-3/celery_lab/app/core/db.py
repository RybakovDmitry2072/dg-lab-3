from sqlmodel import create_engine, SQLModel

from app.utils import build_engine_url

engine = create_engine(build_engine_url(), echo=True)


def create_db_and_tables():
    """
    Create the database tables.

    This function creates the database tables based on the models defined in
    :py:mod:`app.models`.

    It uses the :py:func:`sqlmodel.metadata.create_all` function to create the
    tables in the database.

    :param engine: The database engine to use for creating the tables.
    :type engine: :py:class:`sqlalchemy.engine.Engine`
    """
    SQLModel.metadata.create_all(engine)
