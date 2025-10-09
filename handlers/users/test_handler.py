from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.db_api.database import Database
from data.config import DB_NAME
from states import TestStates
from keyboards.inline import get_tests_keyboard, get_abcd_inline_keyboard, get_abcdef_inline_keyboard
from keyboards.default import get_ab_keyboard, get_main_menu
from utils.rasch_model import calculate_rasch_score, get_score_level

router = Router()
db = Database(DB_NAME)


def update_user_score(user_id: int, test_id: int):
    """User javoblaridan natijani hisoblash va yangilash"""
    try:
        # User javoblarini olish
        user_answers = db.get_user_answers(user_id, test_id)

        # To'g'ri javoblarni olish
        correct_answers = db.get_test_answers(test_id)

        if not correct_answers or not user_answers:
            return

        # Ball hisoblash
        score = 0.0
        max_score = 0.0

        # 1-32 savollar (har biri 1 ball)
        for i in range(1, 33):
            max_score += 1.0
            user_key = str(i)
            if user_key in user_answers and user_key in correct_answers:
                if user_answers[user_key].upper() == correct_answers[user_key].upper():
                    score += 1.0

        # 33-35 savollar (har biri 1 ball)
        for i in range(33, 36):
            max_score += 1.0
            user_key = str(i)
            if user_key in user_answers and user_key in correct_answers:
                if user_answers[user_key].upper() == correct_answers[user_key].upper():
                    score += 1.0

        # 36-39 savollar (har biri 2 ball)
        for i in range(36, 40):
            max_score += 2.0
            user_key = str(i)
            if user_key in user_answers and user_key in correct_answers:
                if user_answers[user_key].strip().lower() == correct_answers[user_key].strip().lower():
                    score += 2.0

        # 40-44 savollar (har biri 3 ball: A=1.5, B=1.5)
        for i in range(40, 45):
            max_score += 3.0
            a_key = f"{i}_a"
            b_key = f"{i}_b"

            if a_key in user_answers and a_key in correct_answers:
                if user_answers[a_key].strip().lower() == correct_answers[a_key].strip().lower():
                    score += 1.5

            if b_key in user_answers and b_key in correct_answers:
                if user_answers[b_key].strip().lower() == correct_answers[b_key].strip().lower():
                    score += 1.5

        # Calculate Rasch model score
        rasch_score = calculate_rasch_score(score, max_score)

        # Natijani saqlash
        db.save_result(user_id, test_id, rasch_score)

    except Exception as e:
        print(f"❌ Natijani yangilashda xato (User {user_id}, Test {test_id}): {e}")


@router.message(F.text == "📝 Test boshlash")
async def start_test(message: Message, state: FSMContext):
    tests = db.get_active_tests()

    if not tests:
        await message.answer("Hozircha mavjud testlar yo'q yoki barcha testlar tugagan.")
        return

    await message.answer(
        "Quyidagi testlardan birini tanlang:",
        reply_markup=get_tests_keyboard(tests)
    )
    await state.set_state(TestStates.choosing_test)


@router.callback_query(TestStates.choosing_test, F.data.startswith("test_"))
async def choose_test(callback: CallbackQuery, state: FSMContext):
    test_id = int(callback.data.split("_")[1])

    # Eski javoblarni o'chirish (agar qayta boshlagan bo'lsa)
    db.clear_user_answers(callback.from_user.id, test_id)

    # Test boshlanganda darhol 0 ball bilan natija yaratish
    # Bu user test boshlagani haqida ma'lumot beradi
    db.save_result(callback.from_user.id, test_id, 0.0)

    await state.update_data(
        test_id=test_id,
        current_question=1,
        answers={}
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "Test boshlandi!\n\n"
        "1-32 savollar: A, B, C, D variantlari\n\n"
        "1-savol uchun javobni tanlang:",
        reply_markup=get_abcd_inline_keyboard()
    )
    await state.set_state(TestStates.answering_1_32)

    try:
        await callback.answer()
    except:
        pass


@router.callback_query(TestStates.answering_1_32, F.data.startswith("answer_"))
async def answer_1_32(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]  # "answer_A" -> "A"

    data = await state.get_data()
    test_id = data.get('test_id')

    # Check if test is still active
    test = db.get_test(test_id)
    if not test or test[3] == 0:  # is_active = 0
        await callback.message.answer(
            "⚠️ Bu test admin tomonidan tugatildi. Javoblaringiz saqlanmadi.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        try:
            await callback.answer("Test tugagan!", show_alert=True)
        except:
            pass
        return

    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = answer

    # Javobni darhol bazaga saqlash
    db.add_user_answer(callback.from_user.id, test_id, str(current), answer)

    # Natijani yangilash
    update_user_score(callback.from_user.id, test_id)

    if current < 32:
        current += 1
        await state.update_data(current_question=current, answers=answers)
        try:
            await callback.message.edit_text(
                f"{current}-savol uchun javobni tanlang:",
                reply_markup=get_abcd_inline_keyboard()
            )
        except:
            await callback.message.delete()
            await callback.message.answer(
                f"{current}-savol uchun javobni tanlang:",
                reply_markup=get_abcd_inline_keyboard()
            )
    else:
        # 33-savolga o'tish
        await state.update_data(current_question=33, answers=answers)
        try:
            await callback.message.edit_text(
                "33-35 savollar: A, B, C, D, E, F variantlari\n\n"
                "33-savol uchun javobni tanlang:",
                reply_markup=get_abcdef_inline_keyboard()
            )
        except:
            await callback.message.delete()
            await callback.message.answer(
                "33-35 savollar: A, B, C, D, E, F variantlari\n\n"
                "33-savol uchun javobni tanlang:",
                reply_markup=get_abcdef_inline_keyboard()
            )
        await state.set_state(TestStates.answering_33_35)

    try:
        await callback.answer()
    except:
        pass


@router.callback_query(TestStates.answering_33_35, F.data.startswith("answer_"))
async def answer_33_35(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]  # "answer_A" -> "A"

    data = await state.get_data()
    test_id = data.get('test_id')

    # Check if test is still active
    test = db.get_test(test_id)
    if not test or test[3] == 0:  # is_active = 0
        await callback.message.answer(
            "⚠️ Bu test admin tomonidan tugatildi. Javoblaringiz saqlanmadi.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        try:
            await callback.answer("Test tugagan!", show_alert=True)
        except:
            pass
        return

    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = answer

    # Javobni darhol bazaga saqlash
    db.add_user_answer(callback.from_user.id, test_id, str(current), answer)

    # Natijani yangilash
    update_user_score(callback.from_user.id, test_id)

    if current < 35:
        current += 1
        await state.update_data(current_question=current, answers=answers)
        try:
            await callback.message.edit_text(
                f"{current}-savol uchun javobni tanlang:",
                reply_markup=get_abcdef_inline_keyboard()
            )
        except:
            await callback.message.delete()
            await callback.message.answer(
                f"{current}-savol uchun javobni tanlang:",
                reply_markup=get_abcdef_inline_keyboard()
            )
    else:
        # 36-savolga o'tish
        await state.update_data(current_question=36, answers=answers)
        try:
            await callback.message.edit_text(
                "36-39 savollar: Yozma javob\n\n"
                "36-savol uchun javobingizni yozing:"
            )
        except:
            await callback.message.delete()
            await callback.message.answer(
                "36-39 savollar: Yozma javob\n\n"
                "36-savol uchun javobingizni yozing:"
            )
        await state.set_state(TestStates.answering_36_39)

    try:
        await callback.answer()
    except:
        pass


@router.message(TestStates.answering_36_39, F.text == "🏠 Asosiy menyu")
@router.message(TestStates.answering_40_44_a, F.text == "🏠 Asosiy menyu")
@router.message(TestStates.answering_40_44_b, F.text == "🏠 Asosiy menyu")
async def cancel_test(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Test bekor qilindi. Javoblaringiz saqlanmadi.",
        reply_markup=get_main_menu()
    )


@router.message(TestStates.answering_36_39)
async def answer_36_39(message: Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get('test_id')

    # Check if test is still active
    test = db.get_test(test_id)
    if not test or test[3] == 0:  # is_active = 0
        await message.answer(
            "⚠️ Bu test admin tomonidan tugatildi. Javoblaringiz saqlanmadi.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return

    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = message.text

    # Javobni darhol bazaga saqlash
    db.add_user_answer(message.from_user.id, test_id, str(current), message.text)

    # Natijani yangilash
    update_user_score(message.from_user.id, test_id)

    if current < 39:
        current += 1
        await state.update_data(current_question=current, answers=answers)
        await message.answer(
            f"{current}-savol uchun javobingizni yozing:"
        )
    else:
        # 40-savolga o'tish
        await state.update_data(current_question=40, answers=answers)
        await message.answer(
            "40-44 savollar: A va B qismlari\n\n"
            "40-savol, A qismini yozing:"
        )
        await state.set_state(TestStates.answering_40_44_a)


@router.message(TestStates.answering_40_44_a)
async def answer_40_44_a(message: Message, state: FSMContext):
    data = await state.get_data()
    test_id = data.get('test_id')

    # Check if test is still active
    test = db.get_test(test_id)
    if not test or test[3] == 0:  # is_active = 0
        await message.answer(
            "⚠️ Bu test admin tomonidan tugatildi. Javoblaringiz saqlanmadi.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return

    current = data['current_question']
    answers = data.get('answers', {})

    answers[f"{current}_a"] = message.text

    # Javobni darhol bazaga saqlash
    db.add_user_answer(message.from_user.id, test_id, f"{current}_a", message.text)

    # Natijani yangilash
    update_user_score(message.from_user.id, test_id)

    await state.update_data(answers=answers)
    await message.answer(
        f"{current}-savol, B qismini yozing:"
    )
    await state.set_state(TestStates.answering_40_44_b)


@router.message(TestStates.answering_40_44_b)
async def answer_40_44_b(message: Message, state: FSMContext):
    data = await state.get_data()
    test_id = data['test_id']

    # Check if test is still active
    test = db.get_test(test_id)
    if not test or test[3] == 0:  # is_active = 0
        await message.answer(
            "⚠️ Bu test admin tomonidan tugatildi. Javoblaringiz saqlanmadi.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return

    current = data['current_question']
    answers = data.get('answers', {})

    answers[f"{current}_b"] = message.text

    # Javobni darhol bazaga saqlash
    db.add_user_answer(message.from_user.id, test_id, f"{current}_b", message.text)

    # Natijani yangilash
    update_user_score(message.from_user.id, test_id)

    if current < 44:
        current += 1
        await state.update_data(current_question=current, answers=answers)
        await message.answer(
            f"{current}-savol, A qismini yozing:"
        )
        await state.set_state(TestStates.answering_40_44_a)
    else:
        # Test tugadi - natijani hisoblash
        await calculate_and_show_result(message, state, test_id, answers)


async def calculate_and_show_result(message: Message, state: FSMContext, test_id: int, user_answers: dict):
    # Bazadan to'g'ri javoblarni olish
    correct_answers = db.get_test_answers(test_id)

    if not correct_answers:
        await message.answer(
            "❌ Xatolik: Test javoblari topilmadi!",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return

    # Javoblar allaqachon har qadamda saqlanganligini tekshirish
    # Agar biror sabab bilan ba'zi javoblar saqlanmagan bo'lsa, ularni saqlash
    saved_answers = db.get_user_answers(message.from_user.id, test_id)
    for q_num, answer in user_answers.items():
        if str(q_num) not in saved_answers:
            db.add_user_answer(message.from_user.id, test_id, str(q_num), answer)
    
    # Ball hisoblash
    score = 0.0
    max_score = 0.0
    
    # 1-32 savollar (har biri 1 ball)
    for i in range(1, 33):
        max_score += 1.0
        user_key = str(i)
        if user_key in user_answers and user_key in correct_answers:
            if user_answers[user_key].upper() == correct_answers[user_key].upper():
                score += 1.0
    
    # 33-35 savollar (har biri 1 ball)
    for i in range(33, 36):
        max_score += 1.0
        user_key = str(i)
        if user_key in user_answers and user_key in correct_answers:
            if user_answers[user_key].upper() == correct_answers[user_key].upper():
                score += 1.0
    
    # 36-39 savollar (har biri 2 ball)
    for i in range(36, 40):
        max_score += 2.0
        user_key = str(i)
        if user_key in user_answers and user_key in correct_answers:
            if user_answers[user_key].strip().lower() == correct_answers[user_key].strip().lower():
                score += 2.0
    
    # 40-44 savollar (har biri 3 ball: A=1.5, B=1.5)
    for i in range(40, 45):
        max_score += 3.0
        a_key = f"{i}_a"
        b_key = f"{i}_b"
        
        if a_key in user_answers and a_key in correct_answers:
            if user_answers[a_key].strip().lower() == correct_answers[a_key].strip().lower():
                score += 1.5
        
        if b_key in user_answers and b_key in correct_answers:
            if user_answers[b_key].strip().lower() == correct_answers[b_key].strip().lower():
                score += 1.5
    
    # Calculate Rasch model score
    rasch_score = calculate_rasch_score(score, max_score)
    level, level_desc = get_score_level(rasch_score)

    # Natijani saqlash (Rasch score)
    db.save_result(message.from_user.id, test_id, rasch_score)

    percentage = (score / max_score * 100) if max_score > 0 else 0

    # Result message - simplified
    await message.answer(
        "✅ <b>Test yakunlandi!</b>",
        reply_markup=get_main_menu()
    )

    await state.clear()
