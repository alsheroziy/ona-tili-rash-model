#!/usr/bin/env python3
'''
Test 1 ni avtomatik tugatish skripti
'''
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from utils.db_api.database import Database
from utils.rasch_model import calculate_rasch_score

DB_NAME = 'data/main.db'

async def finish_test():
    db = Database(DB_NAME)
    test_id = 1

    print(f"\n{'='*50}")
    print(f"🛑 Test tugatish boshlandi: Test ID {test_id}")

    # Active userlarni olish
    active_users = db.get_active_test_users(test_id)
    print(f"📊 Jami userlar: {len(active_users)}")
    print(f"{'='*50}\n")

    # To'g'ri javoblar
    correct_answers = db.get_test_answers(test_id)
    print(f"✅ To'g'ri javoblar: {len(correct_answers)} ta savol\n")

    saved_count = 0

    for idx, user_id in enumerate(active_users, 1):
        try:
            # User javoblarini olish
            user_answers = db.get_user_answers(user_id, test_id)

            if user_answers:
                # Ball hisoblash
                score = 0.0
                max_score = 0.0

                # 1-32 savollar
                for i in range(1, 33):
                    max_score += 1.0
                    user_key = str(i)
                    if user_key in user_answers and user_key in correct_answers:
                        if user_answers[user_key].upper() == correct_answers[user_key].upper():
                            score += 1.0

                # 33-35 savollar
                for i in range(33, 36):
                    max_score += 1.0
                    user_key = str(i)
                    if user_key in user_answers and user_key in correct_answers:
                        if user_answers[user_key].upper() == correct_answers[user_key].upper():
                            score += 1.0

                # 36-39 savollar
                for i in range(36, 40):
                    max_score += 2.0
                    user_key = str(i)
                    if user_key in user_answers and user_key in correct_answers:
                        if user_answers[user_key].strip().lower() == correct_answers[user_key].strip().lower():
                            score += 2.0

                # 40-44 savollar
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

                # Rasch score
                rasch_score = calculate_rasch_score(score, max_score)

                # Natijani saqlash
                db.save_result(user_id, test_id, rasch_score)
                saved_count += 1

            if idx % 100 == 0:
                print(f"  ✓ {idx}/{len(active_users)} user qayta ishlandi...")

        except Exception as e:
            print(f"❌ User {user_id} uchun xato: {e}")

    # Testni tugatish
    db.finish_test(test_id)

    print(f"\n{'='*50}")
    print(f"✅ TEST TUGATISH YAKUNLANDI!")
    print(f"📊 Natijalar saqlandi: {saved_count}/{len(active_users)}")
    print(f"{'='*50}\n")

    # Natijalarni tekshirish
    results = db.get_test_results_summary(test_id)
    print(f"📋 Natijalar jadvalidagi userlar: {len(results)} ta")

    if len(results) > 0:
        print(f"\n🔝 Top 5 natija:")
        for i, (user_id, full_name, score, completed_at) in enumerate(results[:5], 1):
            print(f"  {i}. {full_name}: {score:.2f} ball")

if __name__ == "__main__":
    asyncio.run(finish_test())
