import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

import asgi_correlation_id
from fastapi import FastAPI

from integration.handlers import all_events_handler, get_events_handler
from integration.logging_config import configure_logging

logger = logging.getLogger(__name__)


async def periodic_event_processor():
    """

    Background task that periodically processes events without blocking future fetches.

    """
    tasks = []
    while True:
        try:
            start_time = datetime.now() - timedelta(seconds=10)
            logger.info(f"Start time --> {start_time}")
            events = get_events_handler(start_time)
            task = asyncio.create_task(all_events_handler(events, start_time))
            tasks.append(task)
            print(
                "--------------------------------------------------------------------------"
            )
            print("taks created ", tasks)
            print(
                "--------------------------------------------------------------------------"
            )
            print(
                "--------------------------------------------------------------------------"
            )

            tasks = [t for t in tasks if not t.done()]
        except Exception as e:
            logger.error(f"Error at start: {e}")
        await asyncio.sleep(10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Hello World")
    task = asyncio.create_task(periodic_event_processor())

    yield
    # Code here runs at shutdown
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.add_middleware(asgi_correlation_id.CorrelationIdMiddleware)

"""
@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)


"""
