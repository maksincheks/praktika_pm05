import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from database.db import get_connection
from classes.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        conn = get_connection()
        conn.close()
    except Exception as e:
        sys.exit(1)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()