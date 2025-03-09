import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def get_conversation_details_service(conversation_id: int) -> dict:
    """
    Fetches conversation details from the external service.

    Args:
        conversation_id (int): The unique identifier of the conversation to fetch.

    Returns:
        dict: A dictionary containing the conversation details if the request is successful.
              Returns an empty dictionary if the conversation is not found or an error occurs.
    """
    # Initialize the HTTP status handler
    status_handler = HTTPStatusHandler(logger)

    try:
        logger.info(
            f"Fetching conversation details for conversation_id: {conversation_id}"
        )

        # Fetch conversation details from the external service
        response = requests.get(
            f"{settings.BIG_CHAT_API}/conversations/{conversation_id}"
        )
        # response.raise_for_status()

        status_code = response.status_code
        try:
            conversation_details = response.json()  # Parse response as JSON
        except ValueError:
            logger.warning("Failed to parse JSON response, falling back to raw text.")
            conversation_details = response.text  # Fallback to plain text

        if status_handler.handle_status(response.status_code, conversation_id):
            if not conversation_details:
                logger.warning(
                    f"No conversation details found for ID {conversation_id}."
                )
                return (status_code, {})

            logger.info("Conversation details fetched successfully.")
            return (status_code, conversation_details)

        else:
            return (status_code, {})

    except requests.exceptions.RequestException as e:
        logger.error(
            f"Request error while fetching conversation details: {e}", exc_info=True
        )
        return None, {"error": str(e)}

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return None, {"error": str(e)}
