import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def create_agent_service(agent: dict) -> dict:
    """
    Creates an agent in the external system by sending a POST request.

    Args:
        agent (dict): A dictionary containing agent details. Expected keys:
            - 'email_address' (str): The agent's email address.
            - 'name' (str): The agent's name.

    Returns:
        dict: A dictionary containing the details of the created agent if successful.
              Returns an empty dictionary if the creation fails or encounters an error.
    """
    status_handler = HTTPStatusHandler(logger)

    payload = {
        "email": agent.get("email_address"),
        "name": agent.get("name"),
    }
    if not payload["email"] or not payload["name"]:
        logger.error("Invalid payload: 'email_address' and 'name' are required.")
        return None, {
            "error": "Invalid payload. 'email_address' and 'name' are required."
        }

    try:
        logger.info(f"Creating agent with payload: {payload}")

        # Send POST request to create agent
        response = requests.post(f"{settings.OUR_API}/agents", json=payload)
        # response.raise_for_status()

        status_code = response.status_code
        try:
            agent_response = response.json()  # Parse response as JSON
        except ValueError:
            logger.warning("Failed to parse JSON response, falling back to raw text.")
            agent_response = response.text  # Fallback to plain text

        if status_handler.handle_status(status_code):
            logger.info(f"Agent created successfully: {agent_response}")
            return status_code, agent_response

        return status_code, {}

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while creating agent: {e}", exc_info=True)
        return None, {"error": str(e)}

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return None, {"error": str(e)}
