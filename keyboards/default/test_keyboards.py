from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_abcd_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="A"),
                KeyboardButton(text="B"),
                KeyboardButton(text="C"),
                KeyboardButton(text="D"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_abcdef_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="A"),
                KeyboardButton(text="B"),
                KeyboardButton(text="C"),
            ],
            [
                KeyboardButton(text="D"),
                KeyboardButton(text="E"),
                KeyboardButton(text="F"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_ab_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Keyingisi ➡️")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_skip_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'tkazib yuborish")]
        ],
        resize_keyboard=True
    )
    return keyboard
