from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from classes.user_repository import UserRepository
from classes.captcha_puzzle import CaptchaPuzzle
from classes.main_window import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()
        self.setWindowTitle("Авторизация - Информационная система")
        self.setMinimumSize(450, 600)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Вход в систему")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setMaxLength(100)
        self.login_input.setMinimumHeight(35)
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMaxLength(255)
        self.password_input.setMinimumHeight(35)
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel("Соберите пазл"))

        self.puzzle = CaptchaPuzzle()
        layout.addWidget(self.puzzle)

        self.btn = QPushButton("Войти")
        self.btn.setMinimumHeight(40)
        self.btn.clicked.connect(self.login)
        layout.addWidget(self.btn)
        layout.addStretch()

        self.setTabOrder(self.login_input, self.password_input)
        self.setTabOrder(self.password_input, self.puzzle)

    def login(self):
        username = self.login_input.text().strip()
        password = self.password_input.text()

        # Проверка заполнения полей
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните логин и пароль")
            return  # ВАЖНО: возврат из метода

        # Проверка пазла
        if not self.puzzle.is_solved():
            QMessageBox.warning(self, "Ошибка", "Соберите пазл правильно!")
            self.puzzle.reset()
            self.password_input.clear()
            return  # ВАЖНО: возврат из метода

        # Аутентификация
        user, error, is_locked = self.user_repo.authenticate(username, password)

        if user:
            QMessageBox.information(self, "Успех", "Вы успешно авторизовались")
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", error)
            self.puzzle.reset()
            self.password_input.clear()
            return  # ВАЖНО: возврат из метода

