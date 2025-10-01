from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Test boshlash")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_phone_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_admin_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Test yaratish"), KeyboardButton(text="📋 Testlar ro'yxati")],
            [KeyboardButton(text="📊 Natijalar"), KeyboardButton(text="🛑 Testni tugatish")],
            [KeyboardButton(text="🏠 Asosiy menyu")],
        ],
        resize_keyboard=True
    )
    return keyboard
