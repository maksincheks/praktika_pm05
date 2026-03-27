from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QTableWidget, \
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from classes.user_repository import UserRepository
from classes.user_dialog import UserDialog


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.user_repo = UserRepository()
        self.setWindowTitle(f"Информационная система - {user.username} ({user.role})")
        self.setMinimumSize(600, 400)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Приветствие
        lbl = QLabel(f"Добро пожаловать, {self.current_user.username}!")
        lbl.setFont(QFont("Arial", 14, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        # Только для администратора - управление пользователями
        if self.current_user.is_admin():
            group = QGroupBox("Управление пользователями")
            group.setFont(QFont("Arial", 11, QFont.Bold))
            vbox = QVBoxLayout()

            self.users_table = QTableWidget()
            self.users_table.setColumnCount(4)
            self.users_table.setHorizontalHeaderLabels(["ID", "Логин", "Роль", "Статус"])
            self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            vbox.addWidget(self.users_table)

            btns = QHBoxLayout()
            for name, func in [("Добавить", self.add_user), ("Редактировать", self.edit_user),
                               ("Разблокировать", self.unlock_user)]:
                btn = QPushButton(name)
                btn.clicked.connect(func)
                btns.addWidget(btn)
            vbox.addLayout(btns)

            group.setLayout(vbox)
            layout.addWidget(group)
            self.load_users()

        # Кнопка выхода
        logout_btn = QPushButton("Выйти")
        logout_btn.setMaximumWidth(150)
        logout_btn.clicked.connect(self.logout)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(logout_btn)
        hbox.addStretch()
        layout.addLayout(hbox)

    def load_users(self):
        users = self.user_repo.get_all()
        self.users_table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.users_table.setItem(i, 0, QTableWidgetItem(str(u.id)))
            self.users_table.setItem(i, 1, QTableWidgetItem(u.username))
            self.users_table.setItem(i, 2, QTableWidgetItem(u.role))
            self.users_table.setItem(i, 3, QTableWidgetItem("Заблокирован" if u.is_locked else "Активен"))

    def add_user(self):
        dlg = UserDialog(self)
        if dlg.exec_():
            login, pwd, role, _ = dlg.get_data()
            if not login or not pwd:
                QMessageBox.warning(self, "Ошибка", "Заполните логин и пароль")
                return
            ok, msg = self.user_repo.create(login, pwd, role)
            QMessageBox.information(self, "Успех" if ok else "Ошибка", msg)
            if ok: self.load_users()

    def edit_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        uid = int(self.users_table.item(row, 0).text())
        login = self.users_table.item(row, 1).text()
        role = self.users_table.item(row, 2).text()
        locked = self.users_table.item(row, 3).text() == "Заблокирован"

        dlg = UserDialog(self, (uid, login, role, locked))
        if dlg.exec_():
            new_login, new_pwd, new_role, new_locked = dlg.get_data()
            if not new_login:
                QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым")
                return
            self.user_repo.update(uid, new_login, new_role, new_locked, new_pwd if new_pwd else None)
            QMessageBox.information(self, "Успех", "Пользователь обновлен")
            self.load_users()

    def unlock_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        self.user_repo.unlock(int(self.users_table.item(row, 0).text()))
        QMessageBox.information(self, "Успех", "Пользователь разблокирован")
        self.load_users()

    def logout(self):
        self.close()
        from classes.login_window import LoginWindow
        LoginWindow().show()