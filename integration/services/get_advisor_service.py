import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def get_advisor_service(advisor_id: int) -> dict:
    """
    Fetches advisor details from the external service.

    Args:
        advisor_id (int): The ID of the advisor to fetch.

    Returns:
        dict: A dictionary containing the advisor details if the request is successful.
              Returns an empty dictionary if the advisor is not found or an error occurs.
    """
    # Initialize the HTTP status handler
    status_handler = HTTPStatusHandler(logger)

    try:
        logger.info(f"Fetching advisor details for advisor_id: {advisor_id}")

        # Fetch advisor details from the external service
        response = requests.get(f"{settings.BIG_CHAT_API}/advisors/{advisor_id}")
        # response.raise_for_status()

        status_code = response.status_code
        try:
            advisor = response.json()  # Parse response as JSON
        except ValueError:
            logger.warning("Failed to parse JSON response, falling back to raw text.")
            advisor = response.text  # Fallback to plain text

        if status_handler.handle_status(status_code):
            if not advisor:
                logger.warning(f"No advisor found for ID {advisor_id}.")
                return (status_code, {})

            logger.info("Advisor details fetched successfully.")
            return (status_code, advisor)

        else:
            return (status_code, {})

    except requests.exceptions.RequestException as e:
        logger.error(
            f"Request error while fetching advisor details: {e}", exc_info=True
        )
        return None, {"error": str(e)}

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return None, {"error": str(e)}
