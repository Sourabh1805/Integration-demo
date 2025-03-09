from sqlalchemy.ext.declarative import declarative_base

from integration.config import settings

# Database configuration
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI


# Declarative base for models
Base = declarative_base()
