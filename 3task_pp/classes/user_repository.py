from database.db import get_connection
from classes.user import User


class UserRepository:
    def get_by_username(self, username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role, is_locked, failed_attempts FROM users WHERE username=%s",
                    (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return User(row[0], row[1], row[2], row[3], row[4], row[5]) if row else None

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, role, is_locked FROM users ORDER BY id")
        users = [User(row[0], row[1], '', row[2], row[3], 0) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return users

    def create(self, username, password, role):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return False, "Пользователь с таким логином уже существует"
        cur.execute(
            "INSERT INTO users (username, password_hash, role, is_locked, failed_attempts) VALUES (%s,%s,%s,FALSE,0)",
            (username, password, role))
        conn.commit()
        cur.close()
        conn.close()
        return True, "Пользователь создан"

    def update(self, user_id, username, role, is_locked, new_password=None):
        conn = get_connection()
        cur = conn.cursor()
        if new_password:
            cur.execute(
                "UPDATE users SET username=%s, password_hash=%s, role=%s, is_locked=%s, failed_attempts=0 WHERE id=%s",
                (username, new_password, role, is_locked, user_id))
        else:
            cur.execute("UPDATE users SET username=%s, role=%s, is_locked=%s, failed_attempts=0 WHERE id=%s",
                        (username, role, is_locked, user_id))
        conn.commit()
        cur.close()
        conn.close()

    def lock_user(self, user_id):
        """Заблокировать пользователя"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_locked=TRUE, failed_attempts=3 WHERE id=%s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def authenticate(self, username, password):
        user = self.get_by_username(username)
        if not user:
            return None, "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные", False
        if user.is_locked:
            return None, "Вы заблокированы. Обратитесь к администратору", True
        if password == user.password_hash:
            # Сброс счетчика
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET failed_attempts=0 WHERE id=%s", (user.id,))
            conn.commit()
            cur.close()
            conn.close()
            return user, None, False
        else:
            # Увеличиваем счетчик в БД
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id=%s", (user.id,))
            conn.commit()
            cur.execute("SELECT failed_attempts FROM users WHERE id=%s", (user.id,))
            attempts = cur.fetchone()[0]
            if attempts >= 3:
                cur.execute("UPDATE users SET is_locked = TRUE WHERE id=%s", (user.id,))
                conn.commit()
                cur.close()
                conn.close()
                return None, "Вы заблокированы. Обратитесь к администратору", True
            cur.close()
            conn.close()
            return None, "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные", False

    def unlock(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_locked=FALSE, failed_attempts=0 WHERE id=%s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()