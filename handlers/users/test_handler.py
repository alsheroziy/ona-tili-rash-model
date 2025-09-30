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

    await state.update_data(
        test_id=test_id,
        current_question=1,
        answers={}
    )

    await callback.message.delete()
    await callback.message.answer(
        "Test boshlandi!\n\n"
        "1-32 savollar: A, B, C, D variantlari\n\n"
        "1-savol uchun javobni tanlang:",
        reply_markup=get_abcd_inline_keyboard()
    )
    await state.set_state(TestStates.answering_1_32)
    await callback.answer()


@router.callback_query(TestStates.answering_1_32, F.data.startswith("answer_"))
async def answer_1_32(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]  # "answer_A" -> "A"

    data = await state.get_data()
    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = answer

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

    await callback.answer()


@router.callback_query(TestStates.answering_33_35, F.data.startswith("answer_"))
async def answer_33_35(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]  # "answer_A" -> "A"

    data = await state.get_data()
    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = answer

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

    await callback.answer()


@router.message(TestStates.answering_36_39)
async def answer_36_39(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data['current_question']
    answers = data.get('answers', {})

    answers[str(current)] = message.text

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
    current = data['current_question']
    answers = data.get('answers', {})

    answers[f"{current}_a"] = message.text

    await state.update_data(answers=answers)
    await message.answer(
        f"{current}-savol, B qismini yozing:"
    )
    await state.set_state(TestStates.answering_40_44_b)


@router.message(TestStates.answering_40_44_b)
async def answer_40_44_b(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data['current_question']
    answers = data.get('answers', {})
    test_id = data['test_id']

    answers[f"{current}_b"] = message.text

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
    
    # Bazaga foydalanuvchi javoblarini saqlash
    db.clear_user_answers(message.from_user.id, test_id)
    for q_num, answer in user_answers.items():
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

    # Result message with Rasch score
    result_text = (
        f"✅ <b>Test yakunlandi!</b>\n\n"
        f"📊 <b>Natija:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 Xom ball: {score:.1f} / {max_score:.0f}\n"
        f"📈 Foiz: {percentage:.1f}%\n\n"
        f"🎯 <b>Rasch Model (Xalqaro metodika):</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🏆 Reyting: {rasch_score:.2f} / 78\n"
        f"📊 Daraja: <b>{level}</b> - {level_desc}\n\n"
    )

    # Add interpretation based on level
    if level == "A+" or level == "A":
        result_text += "🌟 A'lo natija! Siz ajoyib bilim ko'rsatdingiz!"
    elif level == "B+" or level == "B":
        result_text += "👍 Yaxshi natija! Davom eting!"
    elif level == "C+" or level == "C":
        result_text += "💪 Qoniqarli natija. Ko'proq mashq qiling!"
    else:
        result_text += "📚 O'tmadingiz. Qayta urinib ko'ring!"

    await message.answer(
        result_text,
        reply_markup=get_main_menu()
    )

    await state.clear()
