#!/usr/bin/env python3
"""
Test 1 ni avtomatik tugatish skripti (simple version)
"""
import sqlite3
import math

DB_NAME = 'data/main.db'
test_id = 1

def calculate_rasch_score(raw_score: float, max_score: float) -> float:
    """Rasch model yordamida ballni hisoblash"""
    if max_score == 0:
        return 0.0

    proportion = raw_score / max_score

    # Extreme qiymatlarni to'g'rilash
    if proportion >= 0.9999:
        proportion = 0.9999
    elif proportion <= 0.0001:
        proportion = 0.0001

    # Logit transformatsiyasi
    logit = math.log(proportion / (1 - proportion))

    # 0-100 oralig'iga o'zgartirish
    rasch_score = 50 + (logit * 10)

    # Minimal va maksimal qiymatlarni cheklash
    rasch_score = max(0, min(100, rasch_score))

    return round(rasch_score, 2)

print(f"\n{'='*50}")
print(f"🛑 Test tugatish boshlandi: Test ID {test_id}")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Active userlarni olish
cursor.execute("SELECT DISTINCT user_id FROM user_answers WHERE test_id = ?", (test_id,))
active_users = [row[0] for row in cursor.fetchall()]
print(f"📊 Jami userlar: {len(active_users)}")
print(f"{'='*50}\n")

# To'g'ri javoblarni olish
cursor.execute("SELECT question_num, answer FROM test_answers WHERE test_id = ?", (test_id,))
correct_answers = {row[0]: row[1] for row in cursor.fetchall()}
print(f"✅ To'g'ri javoblar: {len(correct_answers)} ta savol\n")

saved_count = 0

for idx, user_id in enumerate(active_users, 1):
    try:
        # User javoblarini olish
        cursor.execute("SELECT question_num, answer FROM user_answers WHERE user_id = ? AND test_id = ?",
                      (user_id, test_id))
        user_answers = {row[0]: row[1] for row in cursor.fetchall()}

        if user_answers:
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

            # Rasch score hisoblash
            rasch_score = calculate_rasch_score(score, max_score)

            # Natijani saqlash
            cursor.execute("SELECT id FROM test_results WHERE user_id = ? AND test_id = ?",
                          (user_id, test_id))
            existing = cursor.fetchone()

            if existing:
                cursor.execute(
                    "UPDATE test_results SET score = ?, completed_at = CURRENT_TIMESTAMP WHERE user_id = ? AND test_id = ?",
                    (rasch_score, user_id, test_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO test_results (user_id, test_id, score) VALUES (?, ?, ?)",
                    (user_id, test_id, rasch_score)
                )

            conn.commit()
            saved_count += 1

        if idx % 100 == 0:
            print(f"  ✓ {idx}/{len(active_users)} user qayta ishlandi...")

    except Exception as e:
        print(f"❌ User {user_id} uchun xato: {e}")

# Testni tugatish
cursor.execute("UPDATE tests SET is_active = 0 WHERE test_id = ?", (test_id,))
conn.commit()

print(f"\n{'='*50}")
print(f"✅ TEST TUGATISH YAKUNLANDI!")
print(f"📊 Natijalar saqlandi: {saved_count}/{len(active_users)}")
print(f"{'='*50}\n")

# Natijalarni tekshirish
cursor.execute("""
    SELECT
        u.user_id,
        u.full_name,
        tr.score,
        tr.completed_at
    FROM test_results tr
    JOIN users u ON tr.user_id = u.user_id
    WHERE tr.test_id = ?
    ORDER BY tr.score DESC
    LIMIT 10
""", (test_id,))
results = cursor.fetchall()

print(f"📋 Natijalar jadvalidagi userlar: {saved_count} ta\n")

if len(results) > 0:
    print(f"🔝 Top 10 natija:")
    for i, (user_id, full_name, score, completed_at) in enumerate(results, 1):
        print(f"  {i}. {full_name}: {score:.2f} ball")

conn.close()
print()
