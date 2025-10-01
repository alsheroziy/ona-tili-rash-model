from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
import os
from datetime import datetime

from data.config import ADMINS, DB_NAME
from states import AdminTestStates
from utils.db_api.database import Database
from utils.pdf_generator import generate_test_results_pdf
from keyboards.default import (
    get_admin_menu,
    get_abcd_keyboard,
    get_abcdef_keyboard,
    get_ab_keyboard
)
from keyboards.inline import get_finish_tests_keyboard, get_delete_tests_keyboard, get_tests_list_keyboard

router = Router()
db = Database(DB_NAME)


# Admin filter
def is_admin(message: Message) -> bool:
    return str(message.from_user.id) in ADMINS


@router.message(Command("admin"), F.func(is_admin))
async def admin_command(message: Message):
    await message.answer(
        "Admin paneli:",
        reply_markup=get_admin_menu()
    )


@router.message(F.text == "➕ Test yaratish", F.func(is_admin))
async def create_test_start(message: Message, state: FSMContext):
    await message.answer("Test nomini kiriting:")
    await state.set_state(AdminTestStates.waiting_test_name)


@router.message(AdminTestStates.waiting_test_name, F.text == "🏠 Asosiy menyu")
async def cancel_test_creation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Test yaratish bekor qilindi.",
        reply_markup=get_admin_menu()
    )


@router.message(AdminTestStates.waiting_test_name)
async def process_test_name(message: Message, state: FSMContext):
    test_name = message.text
    test_id = db.create_test(test_name, message.from_user.id)

    await state.update_data(
        test_id=test_id,
        test_name=test_name,
        current_question=1
    )

    await message.answer(
        f"✅ Test yaratildi: <b>{test_name}</b>\n\n"
        f"Endi to'g'ri javoblarni kiriting.\n\n"
        f"1-32 savollar: A, B, C, D variantlari\n\n"
        f"1-savol uchun to'g'ri javobni tanlang:",
        reply_markup=get_abcd_keyboard()
    )
    await state.set_state(AdminTestStates.answering_1_32)


@router.message(AdminTestStates.answering_1_32, F.text == "🏠 Asosiy menyu")
@router.message(AdminTestStates.answering_33_35, F.text == "🏠 Asosiy menyu")
@router.message(AdminTestStates.answering_36_39, F.text == "🏠 Asosiy menyu")
@router.message(AdminTestStates.answering_40_44_a, F.text == "🏠 Asosiy menyu")
@router.message(AdminTestStates.answering_40_44_b, F.text == "🏠 Asosiy menyu")
async def cancel_test_answering(message: Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get('test_id')

    # Yarim yaratilgan testni o'chirish
    if test_id:
        db.delete_test(test_id)

    await state.clear()
    await message.answer(
        "Test yaratish bekor qilindi va o'chirildi.",
        reply_markup=get_admin_menu()
    )


@router.message(AdminTestStates.answering_1_32, F.text.in_(["A", "B", "C", "D"]))
async def admin_answer_1_32(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data['current_question']
    test_id = data['test_id']
    
    # Javobni saqlash
    db.add_test_answer(test_id, str(current), message.text.upper())
    
    if current < 32:
        current += 1
        await state.update_data(current_question=current)
        await message.answer(
            f"{current}-savol uchun to'g'ri javobni tanlang:",
            reply_markup=get_abcd_keyboard()
        )
    else:
        # 33-savolga o'tish
        await state.update_data(current_question=33)
        await message.answer(
            "33-35 savollar: A, B, C, D, E, F variantlari\n\n"
            "33-savol uchun to'g'ri javobni tanlang:",
            reply_markup=get_abcdef_keyboard()
        )
        await state.set_state(AdminTestStates.answering_33_35)


@router.message(AdminTestStates.answering_33_35, F.text.in_(["A", "B", "C", "D", "E", "F"]))
async def admin_answer_33_35(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data['current_question']
    test_id = data['test_id']
    
    db.add_test_answer(test_id, str(current), message.text.upper())
    
    if current < 35:
        current += 1
        await state.update_data(current_question=current)
        await message.answer(
            f"{current}-savol uchun to'g'ri javobni tanlang:",
            reply_markup=get_abcdef_keyboard()
        )
    else:
        # 36-savolga o'tish
        await state.update_data(current_question=36)
        await message.answer(
            "36-39 savollar: Yozma javob\n\n"
            "36-savol uchun to'g'ri javobni yozing:",
            reply_markup=get_ab_keyboard()
        )
        await state.set_state(AdminTestStates.answering_36_39)


@router.message(AdminTestStates.answering_36_39)
async def admin_answer_36_39(message: Message, state: FSMContext):
    if message.text == "Keyingisi ➡️":
        await message.answer("Iltimos, avval to'g'ri javobni yozing!")
        return
    
    data = await state.get_data()
    current = data['current_question']
    test_id = data['test_id']
    
    db.add_test_answer(test_id, str(current), message.text)
    
    if current < 39:
        current += 1
        await state.update_data(current_question=current)
        await message.answer(
            f"{current}-savol uchun to'g'ri javobni yozing:",
            reply_markup=get_ab_keyboard()
        )
    else:
        # 40-savolga o'tish
        await state.update_data(current_question=40)
        await message.answer(
            "40-44 savollar: A va B qismlari\n\n"
            "40-savol, A qismi uchun to'g'ri javobni yozing:",
            reply_markup=get_ab_keyboard()
        )
        await state.set_state(AdminTestStates.answering_40_44_a)


@router.message(AdminTestStates.answering_40_44_a)
async def admin_answer_40_44_a(message: Message, state: FSMContext):
    if message.text == "Keyingisi ➡️":
        await message.answer("Iltimos, avval A qismi uchun to'g'ri javobni yozing!")
        return
    
    data = await state.get_data()
    current = data['current_question']
    test_id = data['test_id']
    
    db.add_test_answer(test_id, f"{current}_a", message.text)
    
    await message.answer(
        f"{current}-savol, B qismi uchun to'g'ri javobni yozing:",
        reply_markup=get_ab_keyboard()
    )
    await state.set_state(AdminTestStates.answering_40_44_b)


@router.message(AdminTestStates.answering_40_44_b)
async def admin_answer_40_44_b(message: Message, state: FSMContext):
    if message.text == "Keyingisi ➡️":
        await message.answer("Iltimos, avval B qismi uchun to'g'ri javobni yozing!")
        return
    
    data = await state.get_data()
    current = data['current_question']
    test_id = data['test_id']
    test_name = data['test_name']
    
    db.add_test_answer(test_id, f"{current}_b", message.text)
    
    if current < 44:
        current += 1
        await state.update_data(current_question=current)
        await message.answer(
            f"{current}-savol, A qismi uchun to'g'ri javobni yozing:",
            reply_markup=get_ab_keyboard()
        )
        await state.set_state(AdminTestStates.answering_40_44_a)
    else:
        # Test yaratish yakunlandi
        await message.answer(
            f"✅ <b>Test muvaffaqiyatli yaratildi!</b>\n\n"
            f"Test nomi: {test_name}\n"
            f"Savollar soni: 44\n\n"
            f"Foydalanuvchilar endi bu testni topshirishlari mumkin.",
            reply_markup=get_admin_menu()
        )
        await state.clear()


@router.message(F.text == "📋 Testlar ro'yxati", F.func(is_admin))
async def list_tests(message: Message):
    tests = db.get_all_tests()

    if not tests:
        await message.answer("Hozircha testlar yo'q.")
        return

    await message.answer(
        "📋 <b>Testlar ro'yxati:</b>\n\n"
        "Testni ko'rish uchun bosing yoki 🗑 tugmasi bilan o'chiring:",
        reply_markup=get_tests_list_keyboard(tests)
    )


@router.callback_query(F.data.startswith("view_test_"))
async def view_test_info(callback: CallbackQuery):
    test_id = int(callback.data.split("_")[2])
    test = db.get_test(test_id)

    if not test:
        await callback.answer("Test topilmadi!", show_alert=True)
        return

    test_name = test[1]
    is_active = test[3]
    created_at = test[4]

    status = "✅ Aktiv" if is_active == 1 else "🛑 Tugagan"

    # Test ishtirokchilar sonini hisoblash
    results = db.get_test_results_summary(test_id)
    participants = len(results)

    info_text = (
        f"📋 <b>Test ma'lumotlari:</b>\n\n"
        f"Nomi: <b>{test_name}</b>\n"
        f"ID: {test_id}\n"
        f"Holat: {status}\n"
        f"Yaratilgan: {created_at}\n"
        f"Ishtirokchilar: {participants} ta"
    )

    await callback.message.answer(info_text)
    await callback.answer()


@router.message(F.text == "📊 Natijalar", F.func(is_admin))
async def show_results_menu(message: Message):
    tests = db.get_all_tests()

    if not tests:
        await message.answer("Hozircha testlar yo'q.")
        return

    text = "📊 <b>Natijalarni ko'rish</b>\n\n"
    text += "Natijalarini ko'rmoqchi bo'lgan testning ID raqamini kiriting:\n\n"

    for idx, (test_id, test_name) in enumerate(tests, 1):
        text += f"{test_id}. {test_name}\n"

    await message.answer(text)


@router.message(F.func(lambda m: m.text and m.text.isdigit() and is_admin(m)))
async def show_test_results(message: Message):
    test_id = int(message.text)
    test = db.get_test(test_id)

    if not test:
        await message.answer("Test topilmadi!")
        return

    test_name = test[1]
    results = db.get_test_results_summary(test_id)

    if not results:
        await message.answer(f"Test '{test_name}' uchun hali natijalar yo'q.")
        return

    # PDF yaratish
    await message.answer("PDF hisobot tayyorlanmoqda...")

    # Papkani yaratish
    os.makedirs("pdf_reports", exist_ok=True)

    # PDF fayl nomi
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"pdf_reports/test_{test_id}_{timestamp}.pdf"

    # To'g'ri javoblar sonini hisoblash va natijalarni tayyorlash
    results_with_correct = []
    for user_id, full_name, score, completed_at in results:
        correct_count = db.count_correct_answers(user_id, test_id)
        results_with_correct.append((correct_count, full_name, score, completed_at))

    # PDF yaratish
    generate_test_results_pdf(test_name, results_with_correct, pdf_filename)

    # PDF yuborish
    pdf_file = FSInputFile(pdf_filename)
    await message.answer_document(
        pdf_file,
        caption=f"📊 <b>{test_name}</b> test natijalari\n\n"
                f"Jami ishtirokchilar: {len(results)} ta"
    )

    # Faylni o'chirish
    try:
        os.remove(pdf_filename)
    except:
        pass


@router.message(F.text == "🛑 Testni tugatish", F.func(is_admin))
async def finish_test_menu(message: Message):
    tests = db.get_active_tests()

    if not tests:
        await message.answer("Tugatiladigan aktiv testlar yo'q.")
        return

    await message.answer(
        "🛑 <b>Testni tugatish</b>\n\n"
        "Tugatmoqchi bo'lgan testni tanlang:",
        reply_markup=get_finish_tests_keyboard(tests)
    )


@router.callback_query(F.data.startswith("finish_test_"))
async def confirm_finish_test(callback: CallbackQuery):
    test_id = int(callback.data.split("_")[2])
    test = db.get_test(test_id)

    if not test:
        await callback.answer("Test topilmadi!", show_alert=True)
        return

    test_name = test[1]
    is_active = test[3]

    if is_active == 0:
        await callback.answer(f"Test allaqachon tugatilgan!", show_alert=True)
        return

    # Testni tugatish
    db.finish_test(test_id)

    # Test topshirayotgan userlarni olish
    from loader import bot
    active_users = db.get_active_test_users(test_id)

    # Userlarga xabar yuborish
    notified_count = 0
    for user_id in active_users:
        try:
            await bot.send_message(
                user_id,
                f"⚠️ <b>Test tugadi!</b>\n\n"
                f"<b>{test_name}</b> testi admin tomonidan tugatildi.\n\n"
                f"Siz belgilagan javoblar saqlandi.\n"
                f"Natijani ko'rish uchun 📊 Natijalarim bo'limiga kiring."
            )
            notified_count += 1
        except:
            pass

    await callback.message.edit_text(
        f"✅ Test <b>{test_name}</b> tugatildi!\n\n"
        f"Xabar yuborildi: {notified_count} ta foydalanuvchiga"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_test_"))
async def confirm_delete_test(callback: CallbackQuery):
    test_id = int(callback.data.split("_")[2])
    test = db.get_test(test_id)

    if not test:
        await callback.answer("Test topilmadi!", show_alert=True)
        return

    test_name = test[1]

    # Testni o'chirish
    db.delete_test(test_id)

    await callback.message.edit_text(
        f"🗑 Test <b>{test_name}</b> o'chirildi!\n\n"
        f"Barcha ma'lumotlar (javoblar, natijalar) butunlay o'chirildi."
    )
    await callback.answer("Test o'chirildi!", show_alert=True)
