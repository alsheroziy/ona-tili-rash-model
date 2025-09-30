from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
