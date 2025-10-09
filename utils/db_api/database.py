import sqlite3
from typing import Optional, List, Dict


class Database:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Foydalanuvchilar jadvali
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Testlar jadvali
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Test javoblari (to'g'ri javoblar)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                question_num TEXT NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY (test_id) REFERENCES tests(test_id)
            )
        """)

        # Foydalanuvchi javoblari
        self.cursor.execute("""
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

        # Test natijalari
        self.cursor.execute("""
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

        self.connection.commit()

    # ========== USERS ==========
    def add_user(self, user_id: int, full_name: str, phone: str):
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, full_name, phone) VALUES (?, ?, ?)",
            (user_id, full_name, phone)
        )
        self.connection.commit()

    def get_user(self, user_id: int) -> Optional[tuple]:
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    # ========== TESTS ==========
    def create_test(self, test_name: str, created_by: int) -> int:
        self.cursor.execute(
            "INSERT INTO tests (test_name, created_by) VALUES (?, ?)",
            (test_name, created_by)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_tests(self) -> List[tuple]:
        self.cursor.execute("SELECT test_id, test_name FROM tests")
        return self.cursor.fetchall()

    def get_active_tests(self) -> List[tuple]:
        """Faqat aktiv testlarni olish"""
        self.cursor.execute("SELECT test_id, test_name FROM tests WHERE is_active = 1")
        return self.cursor.fetchall()

    def get_test(self, test_id: int) -> Optional[tuple]:
        self.cursor.execute("SELECT * FROM tests WHERE test_id = ?", (test_id,))
        return self.cursor.fetchone()

    def finish_test(self, test_id: int):
        """Testni tugatish"""
        self.cursor.execute("UPDATE tests SET is_active = 0 WHERE test_id = ?", (test_id,))
        self.connection.commit()

    def get_active_test_users(self, test_id: int) -> List[int]:
        """Test topshirayotgan userlarni olish"""
        self.cursor.execute(
            """SELECT DISTINCT user_id FROM user_answers WHERE test_id = ?""",
            (test_id,)
        )
        users = [row[0] for row in self.cursor.fetchall()]
        # Debug: print(f"📋 Test {test_id}: {len(users)} ta user topildi")
        return users

    def delete_test(self, test_id: int):
        """Testni butunlay o'chirish (barcha ma'lumotlari bilan)"""
        # Test javoblarini o'chirish
        self.cursor.execute("DELETE FROM test_answers WHERE test_id = ?", (test_id,))
        # Foydalanuvchi javoblarini o'chirish
        self.cursor.execute("DELETE FROM user_answers WHERE test_id = ?", (test_id,))
        # Test natijalarini o'chirish
        self.cursor.execute("DELETE FROM test_results WHERE test_id = ?", (test_id,))
        # Testni o'chirish
        self.cursor.execute("DELETE FROM tests WHERE test_id = ?", (test_id,))
        self.connection.commit()

    # ========== TEST ANSWERS ==========
    def add_test_answer(self, test_id: int, question_num: str, answer: str):
        self.cursor.execute(
            "INSERT INTO test_answers (test_id, question_num, answer) VALUES (?, ?, ?)",
            (test_id, question_num, answer)
        )
        self.connection.commit()

    def get_test_answers(self, test_id: int) -> Dict[str, str]:
        self.cursor.execute(
            "SELECT question_num, answer FROM test_answers WHERE test_id = ?",
            (test_id,)
        )
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    # ========== USER ANSWERS ==========
    def add_user_answer(self, user_id: int, test_id: int, question_num: str, answer: str):
        try:
            # Agar savol allaqachon javob berilgan bo'lsa, yangilash
            self.cursor.execute(
                "DELETE FROM user_answers WHERE user_id = ? AND test_id = ? AND question_num = ?",
                (user_id, test_id, question_num)
            )
            self.cursor.execute(
                "INSERT INTO user_answers (user_id, test_id, question_num, answer) VALUES (?, ?, ?, ?)",
                (user_id, test_id, question_num, answer)
            )
            self.connection.commit()
            # Debug: print(f"💾 User {user_id}, Test {test_id}, Savol {question_num}: '{answer}' saqlandi")
        except Exception as e:
            print(f"❌ Javob saqlashda xato: User {user_id}, Test {test_id}, Savol {question_num} - {e}")
            self.connection.rollback()

    def get_user_answers(self, user_id: int, test_id: int) -> Dict[str, str]:
        self.cursor.execute(
            "SELECT question_num, answer FROM user_answers WHERE user_id = ? AND test_id = ?",
            (user_id, test_id)
        )
        answers = {row[0]: row[1] for row in self.cursor.fetchall()}
        # Debug: print(f"📖 User {user_id}, Test {test_id}: {len(answers)} javob topildi")
        return answers

    def clear_user_answers(self, user_id: int, test_id: int):
        self.cursor.execute(
            "DELETE FROM user_answers WHERE user_id = ? AND test_id = ?",
            (user_id, test_id)
        )
        self.connection.commit()

    # ========== RESULTS ==========
    def save_result(self, user_id: int, test_id: int, score: float):
        try:
            # Agar user uchun bu testning natijasi allaqachon saqlangan bo'lsa, yangilaymiz
            self.cursor.execute(
                "SELECT id FROM test_results WHERE user_id = ? AND test_id = ?",
                (user_id, test_id)
            )
            existing = self.cursor.fetchone()

            if existing:
                # Natijani yangilash
                self.cursor.execute(
                    "UPDATE test_results SET score = ?, completed_at = CURRENT_TIMESTAMP WHERE user_id = ? AND test_id = ?",
                    (score, user_id, test_id)
                )
                # Debug: print(f"🔄 User {user_id}, Test {test_id}: Natija yangilandi - {score:.2f} ball")
            else:
                # Yangi natija qo'shish
                self.cursor.execute(
                    "INSERT INTO test_results (user_id, test_id, score) VALUES (?, ?, ?)",
                    (user_id, test_id, score)
                )
                # Debug: print(f"✅ User {user_id}, Test {test_id}: Yangi natija saqlandi - {score:.2f} ball")
            self.connection.commit()
        except Exception as e:
            print(f"❌ Natija saqlashda xato: User {user_id}, Test {test_id} - {e}")
            self.connection.rollback()

    def get_user_results(self, user_id: int) -> List[tuple]:
        self.cursor.execute(
            """SELECT tr.score, t.test_name, tr.completed_at
               FROM test_results tr
               JOIN tests t ON tr.test_id = t.test_id
               WHERE tr.user_id = ?
               ORDER BY tr.completed_at DESC""",
            (user_id,)
        )
        return self.cursor.fetchall()

    def get_test_results_summary(self, test_id: int) -> List[tuple]:
        """Test bo'yicha barcha foydalanuvchilar natijalarini olish"""
        self.cursor.execute(
            """SELECT
                u.user_id,
                u.full_name,
                tr.score,
                tr.completed_at
               FROM test_results tr
               JOIN users u ON tr.user_id = u.user_id
               WHERE tr.test_id = ?
               AND tr.id = (
                   SELECT id FROM test_results
                   WHERE user_id = tr.user_id AND test_id = tr.test_id
                   ORDER BY completed_at DESC
                   LIMIT 1
               )
               ORDER BY tr.score DESC, u.full_name ASC""",
            (test_id,)
        )
        return self.cursor.fetchall()

    def count_correct_answers(self, user_id: int, test_id: int) -> int:
        """Foydalanuvchining to'g'ri javoblari sonini hisoblash"""
        # Test javoblarini olish
        test_answers = self.get_test_answers(test_id)
        # Foydalanuvchi javoblarini olish
        user_answers = self.get_user_answers(user_id, test_id)

        correct_count = 0
        for question_num, correct_answer in test_answers.items():
            user_answer = user_answers.get(question_num, "")
            if user_answer.strip().lower() == correct_answer.strip().lower():
                correct_count += 1

        return correct_count

    def close(self):
        self.connection.close()
