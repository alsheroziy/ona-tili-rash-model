from aiogram import Router, F
from aiogram.types import Message

from utils.db_api.database import Database
from data.config import DB_NAME

router = Router()
db = Database(DB_NAME)


@router.message(F.text == "📊 Natijalarim")
async def show_results(message: Message):
    results = db.get_user_results(message.from_user.id)
    
    if not results:
        await message.answer("Siz hali hech qanday test topshirmadingiz.")
        return
    
    text = "📊 <b>Sizning natijalaringiz:</b>\n\n"
    for idx, (score, test_name, completed_at) in enumerate(results, 1):
        text += f"{idx}. <b>{test_name}</b>\n"
        text += f"   Ball: {score:.1f}\n"
        text += f"   Sana: {completed_at}\n\n"
    
    await message.answer(text)


@router.message(F.text == "🏠 Asosiy menyu")
async def back_to_menu(message: Message):
    from keyboards.default import get_main_menu
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())
