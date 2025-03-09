import logging

import requests

from integration.config import settings
from integration.utils import HTTPStatusHandler

logger = logging.getLogger(__name__)


def get_events_service(start_time: str) -> tuple:
    """
    Fetches events starting from the specified time from the external service.

    Args:
        start_time (str): The starting timestamp for fetching events in ISO 8601 format.

    Returns:
        tuple: A tuple containing the response status code and a list of events.
               Returns (None, []) if no events are found or an error occurs.
    """
    # Initialize the HTTP status handler
    status_handler = HTTPStatusHandler(logger)

    parameters = {"start_at": start_time}
    logger.debug(f"Fetching events with parameters: {parameters}")

    try:
        response = requests.get(f"{settings.BIG_CHAT_API}/events", params=parameters)
        logger.debug(
            f"Response received: Status code {response.status_code}, Headers: {response.headers}"
        )

        # #response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        if status_handler.handle_status(response.status_code, parameters):
            events = response.json().get("events", [])
            if not events:
                logger.info(f"No events found starting at {start_time}.")
            else:
                logger.info(
                    f"Events fetched successfully: {len(events)} events found starting at {start_time}."
                )
            return response.status_code, events
        return None, []

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed with error: {e}. Parameters sent: {parameters}")
        return None, []

    except ValueError as e:
        logger.error(
            f"JSON decoding failed with error: {e}. Raw response text: {response.text if response else 'None'}"
        )
        return None, []

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        return None, []
