from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QHBoxLayout, QMessageBox

class UserDialog(QDialog):
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Добавить пользователя" if not user else "Редактировать пользователя")
        self.setFixedSize(350, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.login_edit = QLineEdit()
        if self.user:
            self.login_edit.setText(self.user[1])
        self.login_edit.setPlaceholderText("Введите логин")
        layout.addRow("Логин:", self.login_edit)
        
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        if not self.user:
            self.pwd_edit.setPlaceholderText("Введите пароль")
        layout.addRow("Пароль:", self.pwd_edit)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Пользователь", "Администратор"])
        if self.user:
            self.role_combo.setCurrentText(self.user[2])
        layout.addRow("Роль:", self.role_combo)
        
        self.locked_check = QCheckBox("Заблокирован")
        if self.user:
            self.locked_check.setChecked(self.user[3])
        layout.addRow(self.locked_check)
        
        btns = QHBoxLayout()
        save = QPushButton("Сохранить")
        save.clicked.connect(self.accept)
        cancel = QPushButton("Отмена")
        cancel.clicked.connect(self.reject)
        btns.addWidget(save)
        btns.addWidget(cancel)
        layout.addRow(btns)
        
        self.setLayout(layout)
    
    def get_data(self):
        return (self.login_edit.text().strip(), self.pwd_edit.text(),
                self.role_combo.currentText(), self.locked_check.isChecked())