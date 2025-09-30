from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from data.config import ADMINS


class AdminMiddleware(BaseMiddleware):
    """Middleware to check if user is admin"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Add is_admin flag to data
        data['is_admin'] = str(event.from_user.id) in ADMINS
        return await handler(event, data)
