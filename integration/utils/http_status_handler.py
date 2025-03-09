class HTTPStatusHandler:
    """
    Handles HTTP status codes in a reusable and modular way.
    """

    def __init__(self, logger):
        self.logger = logger

    def handle_status(self, status_code, parameters=None):
        """
        Handle HTTP status codes with appropriate actions and logs.

        Args:
            status_code (int): The HTTP status code to handle.
            parameters (dict, optional): Parameters used in the request for context.

        Returns:
            bool: True if the status code indicates success, False otherwise.
        """
        if status_code == 200:
            return True
        elif status_code == 201:
            return True
        elif status_code == 204:
            return True
        elif status_code == 400:
            self.logger.warning(f"Bad request. Parameters: {parameters}")
        elif status_code == 401:
            self.logger.error("Unauthorized access. Check API credentials.")
        elif status_code == 404:
            self.logger.info("Resource not found.")
        else:
            self.logger.error(
                f"Unhandled status code: {status_code}. Parameters: {parameters}"
            )
        return False


"""
from unittest.mock import Mock

# Mock the logger
mock_logger = Mock()

# Initialize the handler
status_handler = HTTPStatusHandler(mock_logger)

# Simulate different scenarios
assert status_handler.handle_status(200) == True
assert status_handler.handle_status(404) == False
mock_logger.info.assert_called_with("Resource not found.")


"""
