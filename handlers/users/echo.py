from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def bot_echo(message: Message):
    # Oddiy echo
    if message.text:
        await message.answer(message.text)
