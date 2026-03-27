import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from database.db import get_connection
from classes.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Проверка подключения к БД
    try:
        conn = get_connection()
        conn.close()
        print("✅ Подключение к БД успешно!")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Не удалось подключиться к БД!\n\n{e}")
        sys.exit(1)
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()