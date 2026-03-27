class User:

    def __init__(self, user_id=None, username='', password_hash='', role='Пользователь',
                 is_locked=False, failed_attempts=0):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.is_locked = is_locked
        self.failed_attempts = failed_attempts

    def is_admin(self):
        return self.role == 'Администратор'
