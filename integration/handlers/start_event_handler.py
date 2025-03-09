import logging

from integration.services import create_chat_service, event_preprocessing_service

logger = logging.getLogger(__name__)


def start_event_handler(event: dict):
    logger.info("Starting to handle start event")

    # Preprocess the event
    flag, start_chat, conversation_details, start_time = event_preprocessing_service(
        event
    )
    if not flag:
        logger.error("Start event preprocessing failed")
        return False

    logger.info("Event preprocessing completed successfully")

    # Create a new event service
    try:
        res = create_chat_service(
            event_name=event["event_name"],
            chat_id=str(start_chat["chat_id"]),
            agent_id=str(start_chat["agent_id"]),
            advisor_id=conversation_details["advisor_id"],
            started_at=start_time,
            conversation_id=event["conversation_id"],
        )

        if res:
            logger.info("Start event handled successfully, event saved in database")
            return True
        else:
            logger.error("Failed to save the start event in the database")
            return False

    except Exception:
        logger.exception("Unexpected error occurred while handling start event")
        return False
