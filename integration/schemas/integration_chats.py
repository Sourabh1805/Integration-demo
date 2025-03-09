from typing import Optional
from pydantic import Field, BaseModel
from typing import Optional



class IntegrationChatBase(BaseModel):
    """
    Base model for Integration Chat, defining the structure
    and validation for chat data.
    """

    event_name: str = Field(description="Name of the event")
    chat_id: str = Field(description="Chat ID from our API")
    agent_id: str = Field(description="Agent ID from our API")
    advisor_id: int = Field(description="Advisor ID from Big Chat")
    started_at: str = Field(description="When the chat started.")
    ended_at: Optional[str] = Field(
        description="When the chat ended (will be undefined if the chat is ongoing).",
        default=None,
    )
    conversation_id: int = Field(description="Conversation ID from Big Chat")
    data: Optional[dict] = Field(description="Additional data based on events")


class IntegrationChatCreate(IntegrationChatBase):
    """
    Model for creating a new Integration Chat record.
    Inherits from IntegrationChatBase.
    """
    pass


class IntegrationChatUpdate(BaseModel):
    """
    Model for updating an existing Integration Chat record.
    Allows for partial updates.
    """
    pass


class IntegrationChat(IntegrationChatBase):
    """
    Model representing an Integration Chat retrieved from the database.
    Adds the integration_chat_id field.
    """

    integration_chat_id: int

    class Config:
        from_attributes = True




  
