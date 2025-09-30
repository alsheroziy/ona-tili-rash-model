from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.db_api.database import Database
from data.config import DB_NAME, ADMINS
from states import RegistrationStates
from keyboards.default import get_main_menu, get_phone_keyboard, get_admin_menu

router = Router()
db = Database(DB_NAME)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    
    if user:
        # Foydalanuvchi ro'yxatdan o'tgan
        if str(message.from_user.id) in ADMINS:
            await message.answer(
                f"Assalomu alaykum, {user[1]}!\n"
                f"Admin paneliga xush kelibsiz.",
                reply_markup=get_admin_menu()
            )
        else:
            await message.answer(
                f"Xush kelibsiz, {user[1]}!\n"
                f"Asosiy menyudan test boshlashingiz mumkin.",
                reply_markup=get_main_menu()
            )
    else:
        # Ro'yxatdan o'tish
        await message.answer(
            "Assalomu alaykum! Botdan foydalanish uchun ro'yxatdan o'ting.\n\n"
            "Ism va familiyangizni kiriting:"
        )
        await state.set_state(RegistrationStates.full_name)


@router.message(RegistrationStates.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(RegistrationStates.phone)


@router.message(RegistrationStates.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = message.contact.phone_number
    
    db.add_user(message.from_user.id, data['full_name'], phone)
    
    await state.clear()
    
    if str(message.from_user.id) in ADMINS:
        await message.answer(
            "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n"
            "Admin paneliga xush kelibsiz.",
            reply_markup=get_admin_menu()
        )
    else:
        await message.answer(
            "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n"
            "Endi testlarni boshlashingiz mumkin.",
            reply_markup=get_main_menu()
        )


@router.message(RegistrationStates.phone)
async def process_phone_text(message: Message):
    await message.answer(
        "Iltimos, telefon raqamingizni tugma orqali yuboring!",
        reply_markup=get_phone_keyboard()
    )
