# from  utils import log_message
from typing import Optional

from integration.database import IntegrationChats
from integration.utils import db

# Get the singleton session
session = db.SessionFactory.get_session()


def create_chat_service(
    event_name: str,
    chat_id: str,
    agent_id: str,
    advisor_id: int,
    started_at: str,
    conversation_id: int,
    ended_at: Optional[str] = None,
    data: Optional[dict] = None,
) -> IntegrationChats:
    """
    Creates a new chat record in the database.

    Args:
        db (Session): The database session.
        event_name (str): Name of the event.
        chat_id (str): Unique chat ID.
        agent_id (str): Agent ID responsible for the chat.
        advisor_id (str): Advisor ID for the conversation.
        started_at (str): Chat start timestamp in ISO 8601 format.
        conversation_id (str): Unique conversation ID.
        ended_at (Optional[str], optional): Chat end timestamp in ISO 8601 format. Defaults to None.
        data (Optional[dict], optional): Additional JSON data for the chat. Defaults to None.

    Returns:
        IntegrationChats: The created `IntegrationChats` object.


    """
    # insert a chat
    try:
        new_chat = IntegrationChats(
            event_name=event_name,
            chat_id=chat_id,
            agent_id=agent_id,
            advisor_id=advisor_id,
            started_at=started_at,
            ended_at=ended_at,
            conversation_id=conversation_id,
            data=data,
        )

        session.add(new_chat)
        session.commit()
        return new_chat
    except Exception:
        # Rollback the transaction in case of an error
        session.rollback()
        # log_message("Info",f"Error creating chat: {e}")
        return None
