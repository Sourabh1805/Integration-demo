from sqlalchemy import JSON, Column, Integer, Text

from .base import Base


class IntegrationChats(Base):
    """
    SQLAlchemy model representing the 'integration_chats' table.
    Stores chat event details with support for optional data and timestamps.
    """

    __tablename__ = "integration_chats"

    integration_chat_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(Text, nullable=False)
    chat_id = Column(Text, nullable=False)
    agent_id = Column(Text, nullable=False)
    advisor_id = Column(Integer, nullable=False)
    started_at = Column(Text, nullable=False)
    ended_at = Column(Text, nullable=True)
    conversation_id = Column(Integer, nullable=False)
    data = Column(JSON, nullable=True)
