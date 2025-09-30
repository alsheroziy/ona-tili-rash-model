from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def get_tests_keyboard(tests: List[tuple]) -> InlineKeyboardMarkup:
    """
    tests: [(test_id, test_name), ...]
    """
    buttons = []
    for test_id, test_name in tests:
        buttons.append([
            InlineKeyboardButton(
                text=test_name,
                callback_data=f"test_{test_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_finish_tests_keyboard(tests: List[tuple]) -> InlineKeyboardMarkup:
    """
    tests: [(test_id, test_name), ...]
    Testlarni tugatish uchun keyboard
    """
    buttons = []
    for test_id, test_name in tests:
        buttons.append([
            InlineKeyboardButton(
                text=f"🛑 {test_name}",
                callback_data=f"finish_test_{test_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_delete_tests_keyboard(tests: List[tuple]) -> InlineKeyboardMarkup:
    """
    tests: [(test_id, test_name), ...]
    Testlarni o'chirish uchun keyboard
    """
    buttons = []
    for test_id, test_name in tests:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {test_name}",
                callback_data=f"delete_test_{test_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_tests_list_keyboard(tests: List[tuple]) -> InlineKeyboardMarkup:
    """
    tests: [(test_id, test_name), ...]
    Testlar ro'yxati uchun keyboard (har bir test yonida o'chirish tugmasi)
    """
    buttons = []
    for test_id, test_name in tests:
        buttons.append([
            InlineKeyboardButton(
                text=test_name,
                callback_data=f"view_test_{test_id}"
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=f"delete_test_{test_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_abcd_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for A, B, C, D variants"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data="answer_A"),
            InlineKeyboardButton(text="B", callback_data="answer_B"),
        ],
        [
            InlineKeyboardButton(text="C", callback_data="answer_C"),
            InlineKeyboardButton(text="D", callback_data="answer_D"),
        ]
    ])
    return keyboard


def get_abcdef_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for A, B, C, D, E, F variants"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data="answer_A"),
            InlineKeyboardButton(text="B", callback_data="answer_B"),
            InlineKeyboardButton(text="C", callback_data="answer_C"),
        ],
        [
            InlineKeyboardButton(text="D", callback_data="answer_D"),
            InlineKeyboardButton(text="E", callback_data="answer_E"),
            InlineKeyboardButton(text="F", callback_data="answer_F"),
        ]
    ])
    return keyboard
