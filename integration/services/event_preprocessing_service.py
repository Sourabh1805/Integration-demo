import logging

from integration.services.create_agent_service import create_agent_service
from integration.services.end_event_service import end_event_service
from integration.services.get_advisor_service import get_advisor_service
from integration.services.get_conversation_details_service import (
    get_conversation_details_service,
)
from integration.services.is_agent_exist_service import is_agent_exist_service
from integration.services.start_event_service import start_event_service
from integration.utils import change_event_at_time_format

logger = logging.getLogger(__name__)


def event_preprocessing_service(event, end_time=None):
    logger.info("Starting event preprocessing")
    logger.debug(f"event --> {event}")
    # Retrieve conversation details
    status_code_conversation_details, conversation_details = (
        get_conversation_details_service(event["conversation_id"])
    )
    if status_code_conversation_details != 200:
        logger.error("Failed to fetch conversation details")
        return (False, {}, {}, "")

    # Retrieve advisor details
    status_code_advisor, advisor = get_advisor_service(
        conversation_details["advisor_id"]
    )
    if status_code_advisor != 200:
        logger.error("Failed to fetch advisor details")
        return (False, {}, {}, "")

    # Check if the agent exists
    agent_status_code, agent = is_agent_exist_service(advisor["email_address"])
    if agent_status_code != 200:
        logger.error("Failed to check agent existence")
        return (False, {}, {}, "")

    if len(agent) == 0:
        logger.info("No agent found, creating a new one")
        new_agent_status_code, new_agent = create_agent_service(advisor)
        if new_agent_status_code != 201:
            logger.error("Failed to create a new agent")
            return (False, {}, {}, "")
        logger.info("New agent created successfully")
    elif len(agent) == 1:
        new_agent = agent[0]
    else:
        logger.warning("Multiple agents found for the given email")

    # Convert event_at to datetime string
    start_time = str(
        change_event_at_time_format(int(conversation_details["events"][0]["event_at"]))
    )

    # Start or end the event
    if end_time is not None:
        status_code, start_chat = end_event_service(
            new_agent["agent_id"],
            start_time,
            str(event["conversation_id"]),
            str(end_time),
        )
    else:
        status_code, start_chat = start_event_service(
            new_agent["agent_id"], start_time, event["conversation_id"]
        )

    if status_code != 201:
        logger.error("Failed to process the event")
        return (False, {}, {}, "")

    logger.info("Event processed successfully")
    return (True, start_chat, conversation_details, start_time)
