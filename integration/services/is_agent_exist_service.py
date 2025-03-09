import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def is_agent_exist_service(email_address: str) -> list:
    """
    Checks if an agent exists for the given email address by querying the external service.

    Args:
        email_address (str): The email address to check for existing agents.

    Returns:
        list: A list of agents matching the given email address if found.
              Returns an empty list if no agents are found or an error occurs.
    """
    # Query parameters for the request
    parameters = {"email": email_address}
    status_handler = HTTPStatusHandler(logger)

    try:
        logger.info(f"Checking if agent exists for email: {email_address}")

        # Send GET request to fetch agent details
        response = requests.get(f"{settings.OUR_API}/agents", params=parameters)
        # response.raise_for_status()

        status_code = response.status_code
        try:
            agent = response.json()  # Parse response as JSON
        except ValueError:
            logger.warning("Failed to parse JSON response, falling back to raw text.")
            agent = response.text  # Fallback to plain text

        if status_handler.handle_status(status_code):
            if not agent:
                logger.info(f"No agents found for email: {email_address}.")
                return (status_code, [])

            logger.info(f"Agent fetch successful: {len(agent)} agents found.")
            return (status_code, agent)

        return (status_code, [])

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching agent details: {e}", exc_info=True)
        return []

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return []
