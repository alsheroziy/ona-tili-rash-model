from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "🏠 Asosiy menyu")
async def back_to_menu(message: Message):
    from keyboards.default import get_main_menu
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())
