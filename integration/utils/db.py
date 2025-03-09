from integration.database import (  # noqa e402
    Base,
    IntegrationChats,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from integration.config import settings
from integration.utils import log_message

# from schemas import IntegrationChat
# Import the model


DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI


class SessionFactory:
    """
    Provides a session instance.

    Returns:
        Session: A SQLAlchemy session instance.
    """

    _session = None
    _engine = None

    @staticmethod
    def get_session():
        """Get a singleton session."""
        if SessionFactory._session is None:
            # Create engine and session only once

            try:
                engine = create_engine(DATABASE_URL)

                # Base.metadata.drop_all(bind=engine)  # drop tables
                Base.metadata.create_all(bind=engine)  # Ensure tables are created
                # print("All tables recreated!")
            except Exception as e:
                log_message("error", f"Database connection failed: {e}")

            Session = sessionmaker(bind=engine)
            SessionFactory._session = Session()
        return SessionFactory._session
