import logging
from aiogram import Router
from aiogram.types import ErrorEvent

# Aiogram v3 da exceptionlar aiogram.exceptions modulida
from aiogram.exceptions import (
    TelegramUnauthorizedError,
    TelegramBadRequest,
    TelegramNotFound,
    TelegramForbiddenError,
    TelegramAPIError
)

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):
    """
    Global error handler for aiogram v3.
    Catches all exceptions within update processing.
    """
    update = event.update
    exception = event.exception

    # V3 da exception turlarini tekshirish
    if isinstance(exception, TelegramUnauthorizedError):
        logging.exception(f'Unauthorized bot token: {exception}')
        return True

    if isinstance(exception, TelegramBadRequest):
        logging.exception(f'Bad request: {exception}')
        return True

    if isinstance(exception, TelegramNotFound):
        logging.exception(f'Not found: {exception}')
        return True

    if isinstance(exception, TelegramForbiddenError):
        logging.exception(f'Forbidden: {exception}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception}')
        return True
    
    # Boshqa har qanday xato
    logging.exception(f'Unhandled error: {exception}\nUpdate: {update}')
    return True
