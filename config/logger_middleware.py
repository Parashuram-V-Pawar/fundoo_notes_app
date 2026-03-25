from fastapi import Request
from config.logger import logger
import time

async def log_requests(request: Request, call_next):
    '''
    Middleware to log incoming HTTP requests and responses.

    This middleware captures request details such as method and path,
    logs the response status and execution time, and handles exceptions
    by logging error details.

    Args:
        request (Request): Incoming HTTP request object.
        call_next (Callable): Function to process the request and return a response.

    Returns:
        Response: The HTTP response returned by the next middleware or route handler.

    Raises:
        Exception: Re-raises any exception encountered during request processing
                   after logging the error details.
    '''
    start_time = time.perf_counter()

    logger.bind(
        method=request.method,
        path=request.url.path
    ).info("Incoming request")

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.bind(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=round(duration, 4)
        ).info("Request completed")

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.bind(
            method=request.method,
            path=request.url.path,
            duration=round(duration, 4)
        ).exception("Request failed")

        raise