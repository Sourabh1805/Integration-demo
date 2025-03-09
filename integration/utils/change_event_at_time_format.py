from datetime import datetime, timezone

def change_event_at_time_format(event_at: int) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 formatted string with microseconds.

    Args:
        event_at (int): The Unix timestamp to convert.

    Returns:
        str: The formatted timestamp as a string in ISO 8601 format.
    """
    
    started_at= datetime.fromtimestamp(event_at, tz=timezone.utc)
    formatted_started_at = started_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return str(formatted_started_at)