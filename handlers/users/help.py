from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["help"]))
async def bot_help(message: Message):
        text = (
                "Buyruqlar:",
                "/start - Botni ishga tushirish",
                "/help - Yordam",
        )
        await message.answer("\n".join(text))