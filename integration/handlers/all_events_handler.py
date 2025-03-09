import logging

from .start_event_handler import start_event_handler

logger = logging.getLogger(__name__)


async def all_events_handler(events, start_time):
    """
    Process a list of event dictionaries concurrently by dispatching each event to its corresponding handler.

    This function creates tasks for each event and runs them concurrently, ensuring that independent events
    are processed in parallel for better performance.

    Supported event types and their handlers:
    - "START"    -> start_event_handler
    - "END"      -> end_event_handler
    - "MESSAGE"  -> message_event_handler
    - "TRANSFER" -> transfer_event_handler

    Parameters
    ----------
    events : list
        A list of event dictionaries. Each dictionary should have at least an "event_name" key.
    start_time : any
        The start time reference passed to the end_event_handler.
    """
    if not events:
        logger.warning("No events found")
        return
    logger.info("Starting to process events")
    tasks = []
    for event in events:
        event_name = event.get("event_name")
        try:
            if event_name == "START":
                start_event_handler(event)  # Add async task
            elif event_name == "END":
                pass
                # tasks.append(end_event_handler(event, start_time))
            elif event_name == "MESSAGE":
                pass
                # tasks.append(message_event_handler(event))
            elif event_name == "TRANSFER":
                pass
                # tasks.append(transfer_event_handler(event))
            else:
                logger.warning(f"Unknown event type: {event_name}")
        except Exception as e:
            logger.error(
                f"Error scheduling task for event {event_name}: {e}", exc_info=True
            )


"""
    # Run all tasks concurrently and wait for their completion
    if tasks:
        try:
            await asyncio.gather(*tasks)
            logger.info(f"All {len(tasks)} events processed successfully.")
        except Exception as e:
            logger.error(
                f"Error during concurrent event processing: {e}", exc_info=True
            )
"""
