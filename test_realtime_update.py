#!/usr/bin/env python3
"""
Real-time natija yangilanishini test qilish
"""
import sqlite3

DB_NAME = 'data/main.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Yangi test yaratish
cursor.execute("INSERT INTO tests (test_name, created_by) VALUES (?, ?)",
              ("Real-time Update Test", 12345678))
conn.commit()
test_id = cursor.lastrowid

print(f"✅ Test yaratildi: ID={test_id}")

# To'g'ri javoblarni qo'shish (faqat 10ta savol)
for i in range(1, 11):
    cursor.execute("INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
                  (test_id, str(i), 'A'))
conn.commit()

print(f"✅ 10ta to'g'ri javob qo'shildi")

# Test user
user_id = 999999
cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, phone) VALUES (?, ?, ?)",
              (user_id, "Test Realtime User", "+998901234567"))
conn.commit()

print(f"\n📝 Test boshlandi...")
print(f"User ID: {user_id}")
print(f"Test ID: {test_id}\n")

# Test boshlanganda 0 ball
cursor.execute("INSERT INTO test_results (user_id, test_id, score) VALUES (?, ?, ?)",
              (user_id, test_id, 0.0))
conn.commit()

cursor.execute("SELECT score FROM test_results WHERE user_id = ? AND test_id = ?",
              (user_id, test_id))
score = cursor.fetchone()[0]
print(f"0️⃣ Test boshlandi: {score:.2f} ball")

# Har bir javobdan keyin natija yangilanishi kerak
for i in range(1, 6):  # 5ta savol
    # Javobni saqlash
    answer = 'A'  # To'g'ri javob
    cursor.execute("INSERT INTO user_answers (user_id, test_id, question_num, answer) VALUES (?, ?, ?, ?)",
                  (user_id, test_id, str(i), answer))
    conn.commit()

    # Natijani hisoblash (soddalashtirilgan)
    # Har bir to'g'ri javob uchun 1 ball
    raw_score = i * 1.0
    max_score = 10.0

    # Rasch model (sodda versiya)
    import math
    proportion = raw_score / max_score
    if proportion >= 0.9999:
        proportion = 0.9999
    elif proportion <= 0.0001:
        proportion = 0.0001

    logit = math.log(proportion / (1 - proportion))
    rasch_score = 50 + (logit * 10)
    rasch_score = max(0, min(100, rasch_score))

    # Natijani yangilash
    cursor.execute("UPDATE test_results SET score = ? WHERE user_id = ? AND test_id = ?",
                  (rasch_score, user_id, test_id))
    conn.commit()

    # Tekshirish
    cursor.execute("SELECT score FROM test_results WHERE user_id = ? AND test_id = ?",
                  (user_id, test_id))
    updated_score = cursor.fetchone()[0]

    print(f"{i}️⃣ {i}-savol javobi saqlandi: {updated_score:.2f} ball")

print(f"\n✅ Test yakunlandi!")

# Oxirgi natijani ko'rish
cursor.execute("""
    SELECT u.full_name, tr.score, tr.completed_at
    FROM test_results tr
    JOIN users u ON tr.user_id = u.user_id
    WHERE tr.user_id = ? AND tr.test_id = ?
""", (user_id, test_id))

result = cursor.fetchone()
if result:
    name, score, completed = result
    print(f"\n📊 Natija:")
    print(f"   User: {name}")
    print(f"   Ball: {score:.2f}")
    print(f"   Vaqt: {completed}")

# Javoblarni tekshirish
cursor.execute("SELECT COUNT(*) FROM user_answers WHERE user_id = ? AND test_id = ?",
              (user_id, test_id))
answer_count = cursor.fetchone()[0]
print(f"\n📝 Saqlangan javoblar: {answer_count} ta")

conn.close()

print(f"\n{'='*50}")
print(f"✅ Test muvaffaqiyatli yakunlandi!")
print(f"{'='*50}\n")
print(f"Endi botda test qiling:")
print(f"1. Test boshlang (ID: {test_id})")
print(f"2. 3-4ta savol javobi bering")
print(f"3. Home tugmasini bosing")
print(f"4. Admin panelda natijalarni tekshiring")
print(f"\nNatija darhol ko'rinishi kerak!\n")
