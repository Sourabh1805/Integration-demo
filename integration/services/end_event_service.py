import requests

from integration.config import settings
from integration.utils import log_message


def end_event_service(
    agent_id: str, event_at: str, external_id: str, ended_at: str
) -> dict:
    """
    Ends an event by sending a POST request to the external service.

    Args:
        agent_id (str): The ID of the agent handling the event.
        event_at (str): The timestamp when the event started.
        external_id (str): The external identifier for the event (e.g., conversation ID).
        ended_at (str): The timestamp when the event ended.

    Returns:
        dict: A dictionary containing the response JSON if the request is successful.
              Returns an empty dictionary if the request fails or an error occurs.

    Process:
        1. Constructs the payload with event details (agent ID, start time, end time, external ID).
        2. Sends a POST request to the external API to record the end of the event.
        3. Logs the result:
            - Logs success if the response status code is 200.
            - Handles common error codes (400, 401, 404) with appropriate log messages.
        4. Handles HTTP errors and unexpected exceptions, logging them and returning an empty dictionary.
    """

    payload = {
        "agent_id": agent_id,
        "started_at": event_at,
        "external_id": external_id,
        "ended_at": ended_at,
    }

    # Headers for the request
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        # Send POST request to start the event
        response = requests.post(
            f"{settings.OUR_API}/chats", json=payload, headers=headers
        )
        # response.raise_for_status()

        status_code = response.status_code
        try:
            response_body = response.json()  # Parse response as JSON
        except ValueError:
            response_body = response.text  # Fallback to plain text

        if status_code == 201:
            # Return the response JSON
            log_message("INFO", f"Event Ended successfully: {status_code}")
        elif status_code == 400:
            log_message("ERROR", "Bad request.")
        elif status_code == 401:
            log_message("ERROR", "Unauthorized.")
        elif status_code == 404:
            log_message("ERROR", "Not Found.")
        else:
            log_message("ERROR", f"Unhandled response code: {status_code}")

        return status_code, response_body

    except requests.exceptions.HTTPError as e:
        log_message("ERROR", f"HTTP error occurred: {e}")
        return None, {"error": str(e)}

    except Exception as e:
        log_message("ERROR", f"Unexpected error: {e}")
        return None, {"error": str(e)}
