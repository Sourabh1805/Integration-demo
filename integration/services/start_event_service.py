import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def start_event_service(agent_id: str, started_at: str, external_id: str) -> dict:
    """
    Starts an event by sending a POST request to the external service.

    Args:
        agent_id (str): The ID of the agent starting the event.
        started_at (str): The timestamp when the event started (ISO 8601 format).
        external_id (str): The external identifier for the event (e.g., conversation ID).

    Returns:
        dict: A dictionary containing the response JSON if the request is successful.
              Returns an empty dictionary if the request fails or an error occurs.
    """
    # Initialize HTTPStatusHandler
    status_handler = HTTPStatusHandler(logger)
    # Payload for the POST request
    payload = {
        "agent_id": agent_id,
        "started_at": started_at,
        "external_id": str(external_id),
    }

    # Headers for the request
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        logger.debug(f"Starting event with payload: {payload}")

        # Send POST request to start the event
        response = requests.post(
            f"{settings.OUR_API}/chats", json=payload, headers=headers
        )
        # response.raise_for_status()

        # Parse the response JSON
        try:
            response_body = response.json()
        except ValueError:
            logger.warning(
                "Failed to parse JSON response, returning an empty dictionary."
            )
            response_body = {}
        # Handle the HTTP status code using the handler
        if status_handler.handle_status(response.status_code):
            logger.info(f"Event started successfully: {response_body}")
            return response.status_code, response_body

        return response.status_code, {}

    except requests.exceptions.HTTPError as http_err:
        logger.error(
            f"HTTP error occurred while starting the event: {http_err}", exc_info=True
        )
        return None, {"error": "HTTP error occurred.", "details": str(http_err)}

    except requests.RequestException as req_err:
        logger.error(
            f"Request exception occurred while starting the event: {req_err}",
            exc_info=True,
        )
        return None, {"error": "Request exception occurred.", "details": str(req_err)}

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return None, {"error": "Unexpected error occurred.", "details": str(e)}
