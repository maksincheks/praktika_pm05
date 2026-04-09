from database.db import get_connection
from classes.user import User


class UserRepository:

    def get_by_username(self, username):
        conn = get_connection()
        cur = conn.cursor()
        # Убрали role, добавили role_id
        cur.execute(
            "SELECT id, username, password_hash, role_id, is_locked, failed_attempts FROM users WHERE username=%s",
            (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            # Преобразуем role_id в название роли
            role_name = self._get_role_name(row[3])
            return User(row[0], row[1], row[2], role_name, row[4], row[5])
        return None

    def _get_role_name(self, role_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM roles WHERE id=%s", (role_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else "Пользователь"

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.username, r.name, u.is_locked 
            FROM users u 
            JOIN roles r ON u.role_id = r.id 
            ORDER BY u.id
        """)
        users = [User(row[0], row[1], '', row[2], row[3], 0) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return users

    def create(self, username, password, role):
        conn = get_connection()
        cur = conn.cursor()

        # Проверка уникальности логина
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return False, "Пользователь с таким логином уже существует"

        # Получаем role_id по названию роли
        cur.execute("SELECT id FROM roles WHERE name=%s", (role,))
        role_row = cur.fetchone()
        if not role_row:
            cur.close()
            conn.close()
            return False, "Указанная роль не существует"

        role_id = role_row[0]

        cur.execute(
            "INSERT INTO users (username, password_hash, role_id, is_locked, failed_attempts) VALUES (%s,%s,%s,FALSE,0)",
            (username, password, role_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, "Пользователь создан"

    def update(self, user_id, username, role, is_locked, new_password=None):
        conn = get_connection()
        cur = conn.cursor()

        # Получаем role_id по названию роли
        cur.execute("SELECT id FROM roles WHERE name=%s", (role,))
        role_row = cur.fetchone()
        role_id = role_row[0] if role_row else 1  # 1 - Пользователь по умолчанию

        if new_password:
            cur.execute(
                "UPDATE users SET username=%s, password_hash=%s, role_id=%s, is_locked=%s, failed_attempts=0 WHERE id=%s",
                (username, new_password, role_id, is_locked, user_id))
        else:
            cur.execute("UPDATE users SET username=%s, role_id=%s, is_locked=%s, failed_attempts=0 WHERE id=%s",
                        (username, role_id, is_locked, user_id))

        conn.commit()
        cur.close()
        conn.close()

    def lock_user(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_locked=TRUE, failed_attempts=3 WHERE id=%s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def unlock(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_locked=FALSE, failed_attempts=0 WHERE id=%s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def authenticate(self, username, password):
        user = self.get_by_username(username)

        if not user:
            return None, "Неверный логин или пароль", False
        if user.is_locked:
            return None, "Вы заблокированы. Обратитесь к администратору", True
        if password == user.password_hash:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET failed_attempts=0 WHERE id=%s", (user.id,))
            conn.commit()
            cur.close()
            conn.close()
            return user, None, False

        # Неудачная попытка
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id=%s", (user.id,))
        conn.commit()
        cur.execute("SELECT failed_attempts FROM users WHERE id=%s", (user.id,))
        attempts = cur.fetchone()[0]
        cur.close()
        conn.close()

        if attempts >= 3:
            self.lock_user(user.id)
            return None, "Вы заблокированы. Обратитесь к администратору", True

        return None, "Неверный логин или пароль", False