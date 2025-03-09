import logging

from integration.services import get_events_service

logger = logging.getLogger(__name__)


def get_events_handler(start_time):
    """
    Handles the retrieval of events, ensuring the provided start_time is valid.

    Args:
        start_time (str): The start time to validate and use for retrieving events.

    Returns:
        Any: The result of the service call if the time format is valid, otherwise None.
    """
    # Simulate async I/O operation for fetching events

    logger.info(f"getting events starting from {start_time}")
    status_code, events = get_events_service(start_time)
    if status_code == 200:
        return events
    else:
        return []
