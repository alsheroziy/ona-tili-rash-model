import sqlite3
import math

def calculate_rasch_score(raw_score: float, max_score: float) -> float:
    if max_score == 0:
        return 0.0
    proportion = raw_score / max_score
    if proportion <= 0.001:
        return 0.0
    elif proportion >= 0.999:
        proportion = 0.999
    logit = math.log(proportion / (1 - proportion))
    offset = 52.0
    scale = 12.5
    rasch_score = offset + scale * logit
    rasch_score = max(0, min(85, rasch_score))
    return round(rasch_score, 2)

# Database'ni ochish
conn = sqlite3.connect('test_bot.db')
cursor = conn.cursor()

# Barcha natijalarni olish
cursor.execute("""
    SELECT tr.id, tr.user_id, tr.test_id
    FROM test_results tr
""")

results = cursor.fetchall()

print(f"Jami {len(results)} ta natija topildi. Qayta hisoblanmoqda...")

updated = 0
for result_id, user_id, test_id in results:
    # User javoblarini olish
    cursor.execute("""
        SELECT question_num, answer 
        FROM user_answers 
        WHERE user_id = ? AND test_id = ?
    """, (user_id, test_id))
    user_answers = {row[0]: row[1] for row in cursor.fetchall()}
    
    # To'g'ri javoblarni olish
    cursor.execute("""
        SELECT question_num, answer 
        FROM test_answers 
        WHERE test_id = ?
    """, (test_id,))
    correct_answers = {row[0]: row[1] for row in cursor.fetchall()}
    
    if not user_answers or not correct_answers:
        continue
    
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
    
    # Yangilash
    cursor.execute("""
        UPDATE test_results 
        SET score = ? 
        WHERE id = ?
    """, (rasch_score, result_id))
    updated += 1

conn.commit()
conn.close()

print(f"✅ {updated} ta natija yangilandi!")

# Yangilangan natijalarni ko'rsatish
conn = sqlite3.connect('test_bot.db')
cursor = conn.cursor()
cursor.execute("""
    SELECT u.full_name, tr.score
    FROM test_results tr
    JOIN users u ON tr.user_id = u.user_id
    ORDER BY tr.score DESC
    LIMIT 10
""")

print("\nEng yuqori natijalar:")
for name, score in cursor.fetchall():
    grade = "A+" if score >= 70 else "A" if score >= 65 else "B+" if score >= 60 else "B" if score >= 55 else "C+" if score >= 50 else "C" if score >= 46 else "NC"
    print(f"  {name}: {score} ball ({grade})")

conn.close()
