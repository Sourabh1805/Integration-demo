import logging


def log_message(level: str, message: str):
    """
    Logs a message at the specified logging level.

    Args:
        level (str): The logging level (e.g., "INFO", "DEBUG", "ERROR").
        message (str): The message to log.

    log_message("INFO", "This is an INFO message.")
    log_message("DEBUG", "This is a DEBUG message.")
    log_message("ERROR", "This is an ERROR message.")
    log_message("WARNING", "This is a WARNING message.")
    log_message("CRITICAL", "This is a CRITICAL message.")
    """
    # Configure logging only once
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-5s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Log based on the level
    if level.upper() == "DEBUG":
        logging.debug(message)
    elif level.upper() == "INFO":
        logging.info(message)
    elif level.upper() == "WARNING":
        logging.warning(message)
    elif level.upper() == "ERROR":
        logging.error(message)
    elif level.upper() == "CRITICAL":
        logging.critical(message)
    else:
        logging.info(f"Unknown level '{level}', logging as INFO: {message}")
