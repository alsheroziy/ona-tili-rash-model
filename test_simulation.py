"""
Bot test simulyatsiyasi: 1000 ta user, har biri 30ta savolgacha
"""
import sqlite3
import random

# Test user ID range
START_USER_ID = 100000
USER_COUNT = 1000

# Database connection
DB_NAME = 'data/main.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Jadvallarni yaratish
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        question_num TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (test_id) REFERENCES tests(test_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        question_num TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (test_id) REFERENCES tests(test_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        score REAL NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (test_id) REFERENCES tests(test_id)
    )
""")

conn.commit()

print(f"🚀 Test simulyatsiya boshlandi...")
print(f"📊 User soni: {USER_COUNT}")
print(f"📝 Har bir user 30ta savolgacha javob beradi\n")

# Test yaratish
test_name = "1000 Userlik Stress Test"
admin_id = 12345678  # .env dagi birinchi admin ID

print(f"📋 Test yaratilmoqda: {test_name}...")
cursor.execute("INSERT INTO tests (test_name, created_by) VALUES (?, ?)", (test_name, admin_id))
conn.commit()
test_id = cursor.lastrowid
print(f"✅ Test yaratildi: ID={test_id}\n")

# To'g'ri javoblarni qo'shish
print("📝 To'g'ri javoblar qo'shilmoqda...")

# 1-32 savollar (A, B, C, D)
for i in range(1, 33):
    answer = random.choice(['A', 'B', 'C', 'D'])
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, str(i), answer))

# 33-35 savollar (A, B, C, D, E, F)
for i in range(33, 36):
    answer = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, str(i), answer))

# 36-39 savollar (yozma)
for i in range(36, 40):
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, str(i), f"javob_{i}"))

# 40-44 savollar (A va B qismlari)
for i in range(40, 45):
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, f"{i}_a", f"javob_{i}_a"))
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, f"{i}_b", f"javob_{i}_b"))

conn.commit()

print(f"✅ To'g'ri javoblar qo'shildi (49ta savol)\n")

# Userlarni ro'yxatdan o'tkazish va javoblarini qo'shish
print(f"👥 {USER_COUNT} ta user yaratilmoqda va javoblar qo'shilmoqda...")

for i in range(USER_COUNT):
    user_id = START_USER_ID + i
    full_name = f"Test User {i+1}"
    phone = f"+998901234{i:04d}"

    # Usermi ro'yxatdan o'tkazish
    cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, phone) VALUES (?, ?, ?)",
                  (user_id, full_name, phone))

    # 30ta savolga javob berish (1-30)
    for q_num in range(1, 31):
        if q_num <= 32:
            answer = random.choice(['A', 'B', 'C', 'D'])
        elif q_num <= 35:
            answer = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        else:
            answer = f"javob_{q_num}"

        cursor.execute("INSERT INTO user_answers (user_id, test_id, question_num, answer) VALUES (?, ?, ?, ?)",
                      (user_id, test_id, str(q_num), answer))

    if (i + 1) % 100 == 0:
        conn.commit()
        print(f"  ✓ {i + 1}/{USER_COUNT} user bajarildi...")

conn.commit()

print(f"\n✅ Barcha userlar va javoblar yaratildi!")

# Statistika
print(f"\n{'='*60}")
print(f"📊 TEST STATISTIKASI")
print(f"{'='*60}")
print(f"Test ID: {test_id}")
print(f"Test nomi: {test_name}")
print(f"User soni: {USER_COUNT}")
print(f"Har bir userning javoblari: 30ta")
print(f"Jami javoblar soni: {USER_COUNT * 30}")
print(f"{'='*60}\n")

# Bazadan tekshirish
cursor.execute("SELECT DISTINCT user_id FROM user_answers WHERE test_id = ?", (test_id,))
active_users = [row[0] for row in cursor.fetchall()]
print(f"📋 Bazadan topilgan userlar: {len(active_users)} ta")

# Birinchi 5 userning javoblarini tekshirish
print(f"\n🔍 Birinchi 5 userning javoblari:")
for i in range(5):
    user_id = START_USER_ID + i
    cursor.execute("SELECT COUNT(*) FROM user_answers WHERE user_id = ? AND test_id = ?", (user_id, test_id))
    count = cursor.fetchone()[0]
    print(f"  User {user_id}: {count} javob")

conn.close()

print(f"\n{'='*60}")
print(f"✅ SIMULYATSIYA TAYYOR!")
print(f"{'='*60}")
print(f"\nEndi botda admin sifatida:")
print(f"1. /admin buyrug'ini yuboring")
print(f"2. '🛑 Testni tugatish' tugmasini bosing")
print(f"3. Test ID: {test_id} ni tanlang")
print(f"4. Konsolda barcha loglarni kuzating")
print(f"\nYoki quyidagi skriptni ishga tushiring:")
print(f"  python test_finish.py {test_id}")
print(f"{'='*60}\n")

# Test finish skriptini yaratish
finish_script = f"""#!/usr/bin/env python3
'''
Test {test_id} ni avtomatik tugatish skripti
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
    test_id = {test_id}

    print(f"\\n{{'='*50}}")
    print(f"🛑 Test tugatish boshlandi: Test ID {{test_id}}")

    # Active userlarni olish
    active_users = db.get_active_test_users(test_id)
    print(f"📊 Jami userlar: {{len(active_users)}}")
    print(f"{{'='*50}}\\n")

    # To'g'ri javoblar
    correct_answers = db.get_test_answers(test_id)
    print(f"✅ To'g'ri javoblar: {{len(correct_answers)}} ta savol\\n")

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
                    a_key = f"{{i}}_a"
                    b_key = f"{{i}}_b"

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
                print(f"  ✓ {{idx}}/{{len(active_users)}} user qayta ishlandi...")

        except Exception as e:
            print(f"❌ User {{user_id}} uchun xato: {{e}}")

    # Testni tugatish
    db.finish_test(test_id)

    print(f"\\n{{'='*50}}")
    print(f"✅ TEST TUGATISH YAKUNLANDI!")
    print(f"📊 Natijalar saqlandi: {{saved_count}}/{{len(active_users)}}")
    print(f"{{'='*50}}\\n")

    # Natijalarni tekshirish
    results = db.get_test_results_summary(test_id)
    print(f"📋 Natijalar jadvalidagi userlar: {{len(results)}} ta")

    if len(results) > 0:
        print(f"\\n🔝 Top 5 natija:")
        for i, (user_id, full_name, score, completed_at) in enumerate(results[:5], 1):
            print(f"  {{i}}. {{full_name}}: {{score:.2f}} ball")

if __name__ == "__main__":
    asyncio.run(finish_test())
"""

with open('/Users/shehrozraxmatov/Desktop/ona-tili-rash-model/test_finish.py', 'w', encoding='utf-8') as f:
    f.write(finish_script)

print(f"📝 test_finish.py skripti yaratildi")
