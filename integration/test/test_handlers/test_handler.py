import logging
from datetime import datetime, timedelta

import pytest
import requests

from integration.config import settings
from integration.handlers.start_event_handler import start_event_handler

logger = logging.getLogger(__name__)


@pytest.fixture()
def fixture_get_events_service():
    start_time = datetime.now() - timedelta(seconds=10)
    parameters = {"start_at": start_time}
    response = requests.get(f"{settings.BIG_CHAT_API}/events", params=parameters)
    print("response   ", response.json().get("events"))
    return response.json().get("events")


@pytest.fixture()
def fixture_event_finder(fixture_get_events_service: dict):
    print("fixture_get_events_service   ", fixture_get_events_service)
    if not fixture_get_events_service:
        logger.warning("No events found")
        return
    logger.info("Starting to process events")

    for event in fixture_get_events_service:
        event_name = event.get("event_name")

        if event_name == "START":
            return True, event
        else:
            pass
    return False, {}


def test_get_events_service():
    start_time = datetime.now() - timedelta(seconds=10)
    parameters = {"start_at": start_time}
    response = requests.get(f"{settings.BIG_CHAT_API}/events", params=parameters)
    assert response.status_code == 200


def test_start_event_handler(fixture_event_finder):
    flag, event = fixture_event_finder
    print(flag, event)
    if flag:
        res = start_event_handler(event)
        assert res == True
