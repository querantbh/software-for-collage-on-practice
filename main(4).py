import sys
import datetime
import re
import mysql.connector
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QCheckBox, QMessageBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor, QIntValidator, QFont, QScreen, QGuiApplication, QPixmap, QIcon

class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(200, 200, 400, 400)

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 200,
            screen_geometry.height() // 2 - 200,
            400,
            400
        )

        # Загрузка изображения с интернета
        icon_url = "https://cdn-icons-png.flaticon.com/512/81/81924.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            # Создание QPixmap из байтового массива
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            # Установка значка окна
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        comic_sans_font = QFont("Comic Sans MS", 10)

        self.last_name_input = QLineEdit()
        self.last_name_input.setFont(comic_sans_font)
        self.first_name_input = QLineEdit()
        self.first_name_input.setFont(comic_sans_font)
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setFont(comic_sans_font)
        self.nickname_input = QLineEdit()
        self.nickname_input.setFont(comic_sans_font)
        self.email_input = QLineEdit()
        self.email_input.setFont(comic_sans_font)
        self.password_input = QLineEdit()
        self.password_input.setFont(comic_sans_font)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setFont(comic_sans_font)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setFont(comic_sans_font)
        self.phone_number_input.setValidator(QIntValidator())
        self.license_checkbox = QCheckBox("Я согласен с лицензионным соглашением")
        self.license_checkbox.setFont(comic_sans_font)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.register)
        button_box.rejected.connect(self.close)

        form_layout = QFormLayout()
        form_layout.addRow("Фамилия:", self.last_name_input)
        form_layout.addRow("Имя:", self.first_name_input)
        form_layout.addRow("Отчество:", self.middle_name_input)
        form_layout.addRow("Никнейм пользователя:", self.nickname_input)
        form_layout.addRow("Почта пользователя:", self.email_input)
        form_layout.addRow("Пароль пользователя:", self.password_input)
        form_layout.addRow("Повторите пароль:", self.confirm_password_input)
        form_layout.addRow("Ваш телефон:", self.phone_number_input)
        form_layout.addRow("", self.license_checkbox)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        button_box.setStyleSheet(button_style)

        self.setLayout(layout)

    def register(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_name = self.middle_name_input.text()
        nickname = self.nickname_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        phone_number = self.phone_number_input.text()
        self.reject()

        if not nickname.isalpha():
            print("Имя пользователя должно содержать только английские буквы")
            return

        if not re.match(r"^[a-zA-Z0-9._%+-]+@(?:gmail\.com|yandex\.ru|mail\.ru)$", email):
            print("Пожалуйста, используйте допустимый домен для почты")
            return

        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            print("Пароль должен содержать не менее 8 символов, хотя бы одну заглавную букву и хотя бы одну цифру")
            return

        if password != confirm_password:
            print("Пароли не совпадают")
            return

        if not self.license_checkbox.isChecked():
            print("Вы должны согласиться с лицензионным соглашением")
            return

        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = "INSERT INTO clients (Familiya, Imya, Otchestvo, Telefon) VALUES (%s, %s, %s, %s)"
        val = (last_name, first_name, middle_name, phone_number)
        cursor.execute(sql, val)
        db.commit()

        sql_check_nickname = "SELECT * FROM users WHERE Nickname = %s"
        cursor.execute(sql_check_nickname, (nickname,))
        existing_nickname = cursor.fetchone()

        sql_check_email = "SELECT * FROM users WHERE Email = %s"
        cursor.execute(sql_check_email, (email,))
        existing_email = cursor.fetchone()

        if existing_nickname:
            print("Пользователь с таким никнеймом уже существует")
            db.close()
            return

        if existing_email:
            print("Пользователь с такой почтой уже существует")
            db.close()
            return

        sql = "INSERT INTO users (Nickname, Email, Password, Role) VALUES (%s, %s, %s, %s)"
        val = (nickname, email, password, "User")
        cursor.execute(sql, val)
        db.commit()
        db.close()

        self.accept()
        self.show_main_window(nickname)

    def show_main_window(self, nickname):
        self.hide()
        main_window = RepairRequestApp(nickname)
        main_window.show()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(200, 200, 300, 100)

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 150,
            screen_geometry.height() // 2 - 50,
            300,
            100
        )

        # Загрузка изображения с интернета
        icon_url = "https://cdn-icons-png.flaticon.com/512/81/81924.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            # Создание QPixmap из байтового массива
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            # Установка значка окна
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        login_button = QPushButton("Вход")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(self.register_and_close)
        layout.addWidget(register_button)

        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        login_button.setStyleSheet(button_style)
        register_button.setStyleSheet(button_style)

        self.setLayout(layout)
        self.user_data = None

    def login(self):
        self.accept()

        login_window = LoginWindow(self)
        result = login_window.exec()

        if result == QDialog.DialogCode.Accepted:
            print("Вход выполнен")
            self.user_data = login_window.get_user_data()
            self.show_main_window()
        else:
            self.show()

    def register_and_close(self):
        self.accept()

        registration_dialog = RegistrationDialog()
        result = registration_dialog.exec()
        if result == QDialog.DialogCode.Rejected:
            self.show()

    def show_main_window(self):
        self.hide()
        main_window = RepairRequestApp(self.user_data)
        main_window.show()

    def get_user_data(self):
        return self.user_data if self.user_data is not None else ()

class LoginWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Вход")
        self.setGeometry(200, 200, 300, 150)
        self.user_data = None

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 150,
            screen_geometry.height() // 2 - 50,
            300,
            100
        )

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setFont(QFont("Comic Sans MS", 10))
        self.login_input.setStyleSheet(
            "border-radius: 5px;" 
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
        )

        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Comic Sans MS", 10))
        self.password_input.setStyleSheet(
            "border-radius: 5px;" 
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
        )

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.login)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        login_button.setStyleSheet(button_style)
        cancel_button.setStyleSheet(button_style)

        layout.addWidget(QLabel("Логин (или почта):"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql_check_user = "SELECT * FROM users WHERE (Nickname = %s OR Email = %s) AND Password = %s"
        cursor.execute(sql_check_user, (login, login, password))
        user_data = cursor.fetchone()

        if user_data:
            role = user_data[1]  # Получаем значение колонки "Role" (предполагается, что она находится на второй позиции)
            db.close()
            self.user_data = user_data

            if role == "User":
                self.accept()
                self.show_main_window()
            elif role == "Admin":
                self.accept()
                self.show_accounting_window_manager()
        else:
            db.close()
            QMessageBox.critical(self, "Ошибка", "Неверный логин (или почта) или пароль")

    def show_accounting_window_manager(self):
        self.hide()
        accounting_window_manager = AccountingWindowManager()
        accounting_window_manager.show()

    def get_user_data(self):
        return self.user_data

    def show_main_window(self):
        self.hide()
        user_data = self.get_user_data()
        role = user_data[1]  # Получаем роль пользователя из данных пользователя

        if role == "User":
            main_window = RepairRequestApp(user_data)
            main_window.show()
        elif role == "Admin":
            manager_window = AccountingWindowManager()
            manager_window.show()

class AccountingWindowManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет заявок на ремонт оборудования")
        self.setGeometry(100, 100, 800, 600)

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 400,
            screen_geometry.height() // 2 - 300,
            800,
            600
        )

        # Загрузка изображения с интернета
        icon_url = "https://cdn-icons-png.flaticon.com/512/81/81924.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            # Создание QPixmap из байтового массива
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            # Установка значка окна
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Добавьте поле ввода для поиска по ID
        self.search_id_input = QLineEdit()
        self.search_id_input.setStyleSheet(
            "border-radius: 5px;" 
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
        )

        self.search_id_button = QPushButton("Поиск по ID")
        self.search_id_button.clicked.connect(self.search_by_id)
        layout.addWidget(self.search_id_input)

        # Стиль для кнопки "Поиск по ID"
        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        self.search_id_button.setStyleSheet(button_style)  # Применяем стиль к кнопке "Поиск по ID"

        layout.addWidget(self.search_id_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Дата добавления", "Оборудование", "Тип неисправности", "Описание", "Клиент", "Статус", "Изменить статус"])
        self.table_widget.horizontalHeader().setSectionHidden(7, True)
        self.table_widget.setColumnWidth(7, 0)
        layout.addWidget(self.table_widget)

        self.load_requests()

        self.setLayout(layout)

        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """

        # Стилизация кнопки "Сохранить все изменения"
        self.save_changes_button = QPushButton("Сохранить все изменения")
        self.save_changes_button.setFont(QFont("Comic Sans MS", 10))

        # Добавьте стиль для кнопки "Сохранить все изменения"
        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        self.save_changes_button.setStyleSheet(button_style)

        layout.addWidget(self.save_changes_button)

        # Добавьте обработчик нажатия для кнопки "Сохранить все изменения"
        self.save_changes_button.clicked.connect(self.save_all_changes)

    def search_by_id(self):
        # Получите введенный пользователем ID заявки
        search_id = self.search_id_input.text()

        # Выполните запрос к базе данных для поиска по ID заявки
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = "SELECT * FROM zayavki WHERE ID_zayavki = %s"
        cursor.execute(sql, (search_id,))
        data = cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                # Установите шрифт Comic Sans MS для элементов таблицы
                item.setFont(QFont("Comic Sans MS", 10))

                self.table_widget.setItem(row_idx, col_idx, item)

            # Получите статус для установки начального значения выпадающего списка
            status_item = self.table_widget.item(row_idx, 6)  # Столбец "Статус"
            if status_item is not None:
                current_status = status_item.text()

                # Создайте выпадающий список и установите начальное значение
                status_combobox = QComboBox()
                status_combobox.addItems(["В ожидании", "В работе", "Выполнено"])
                status_combobox.setCurrentText(current_status)

                self.table_widget.setCellWidget(row_idx, 6, status_combobox)

        db.close()
        
    def load_requests(self):
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = "SELECT * FROM zayavki"
        cursor.execute(sql)
        data = cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                # Установите шрифт Comic Sans MS для элементов таблицы
                item.setFont(QFont("Comic Sans MS", 10))

                self.table_widget.setItem(row_idx, col_idx, item)

            # Получите статус для установки начального значения выпадающего списка
            status_item = self.table_widget.item(row_idx, 6)  # Столбец "Статус"
            if status_item is not None:
                current_status = status_item.text()

                # Создайте выпадающий список и установите начальное значение
                status_combobox = QComboBox()
                status_combobox.addItems(["В ожидании", "В работе", "Выполнено"])
                status_combobox.setCurrentText(current_status)

                self.table_widget.setCellWidget(row_idx, 6, status_combobox)

        # Установите стили для таблицы
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #333;
                color: white;
                gridline-color: #555;
                alternate-background-color: #444;
                selection-background-color: #6A0EAD;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #666;
                border: 1px solid #555;
            }
            QTableWidget::item {
                background-color: #333;
                padding-left: 10px;
            }
            QTableWidget::item:selected {
                background-color: #6A0EAD;
            }
        """)

    def save_all_changes(self):
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        for row in range(self.table_widget.rowCount()):
            # Получите ID и новый статус из выпадающего списка
            request_id_item = self.table_widget.item(row, 0)
            status_combobox = self.table_widget.cellWidget(row, 6)  # Столбец "Статус" с выпадающим списком

            if request_id_item is not None and status_combobox is not None:
                request_id_value = request_id_item.text()
                new_status = status_combobox.currentText()

                # Обновите статус в базе данных, используя правильное имя поля
                sql_update_status = "UPDATE zayavki SET Status_zayavki = %s WHERE ID_zayavki = %s"
                cursor.execute(sql_update_status, (new_status, request_id_value))

        db.commit()
        db.close()

        # Выводим уведомление
        success_message = QMessageBox()
        success_message.setWindowTitle("Успешно!")
        success_message.setText("Изменения успешно сохранены.")
        success_message.setIcon(QMessageBox.Icon.Information)
        success_message.exec()

class AccountingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет заявок на ремонт оборудования")
        self.setGeometry(100, 100, 800, 600)

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 400,
            screen_geometry.height() // 2 - 300,
            800,
            600
        )

        # Загрузка изображения с интернета
        icon_url = "https://cdn-icons-png.flaticon.com/512/81/81924.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            # Создание QPixmap из байтового массива
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            # Установка значка окна
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Добавьте поле ввода для поиска по ID
        self.search_id_input = QLineEdit()
        self.search_id_input.setStyleSheet(
            "border-radius: 5px;" 
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
        )

        self.search_id_button = QPushButton("Поиск по ID")
        self.search_id_button.clicked.connect(self.search_by_id)
        layout.addWidget(self.search_id_input)

        # Стиль для кнопки "Поиск по ID"
        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        self.search_id_button.setStyleSheet(button_style)  # Применяем стиль к кнопке "Поиск по ID"

        layout.addWidget(self.search_id_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)  # Теперь 9 столбцов
        self.table_widget.setHorizontalHeaderLabels(["ID", "Дата добавления", "Оборудование", "Тип неисправности", "Описание", "Клиент", "Статус", "Исполнитель"])
        self.table_widget.horizontalHeader().setSectionHidden(7, True)
        self.table_widget.setColumnWidth(7, 0)
        layout.addWidget(self.table_widget)

        self.load_requests()

        self.setLayout(layout)

        # Стилизация кнопки "Сохранить все изменения"
        self.save_changes_button = QPushButton("Сохранить все изменения")
        self.save_changes_button.setFont(QFont("Comic Sans MS", 10))

        # Добавьте стиль для кнопки "Сохранить все изменения"
        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        self.save_changes_button.setStyleSheet(button_style)

        layout.addWidget(self.save_changes_button)

        # Добавьте обработчик нажатия для кнопки "Сохранить все изменения"
        self.save_changes_button.clicked.connect(self.save_all_changes)

    def search_by_id(self):
        # Получите введенный пользователем ID заявки
        search_id = self.search_id_input.text()

        # Выполните запрос к базе данных для поиска по ID заявки
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = "SELECT * FROM zayavki WHERE ID_zayavki = %s"
        cursor.execute(sql, (search_id,))
        data = cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                # Установите шрифт Comic Sans MS для элементов таблицы
                item.setFont(QFont("Comic Sans MS", 10))

                self.table_widget.setItem(row_idx, col_idx, item)

            # Получите статус для установки начального значения выпадающего списка
            status_item = self.table_widget.item(row_idx, 6)  # Столбец "Статус"
            if status_item is not None:
                current_status = status_item.text()

                # Создайте выпадающий список и установите начальное значение
                status_combobox = QComboBox()
                status_combobox.addItems(["В ожидании", "В работе", "Выполнено"])
                status_combobox.setCurrentText(current_status)

                self.table_widget.setCellWidget(row_idx, 6, status_combobox)

            # Получите ID исполнителя из базы данных и установите его в колонку "Исполнитель"
            ispolnitel_id = row_data[8]  # Индекс столбца "Ispolnitel_id" в данных
            executor_sql = "SELECT Ispolnitel_id FROM ispolniteli WHERE ispolnitel_id = %s"
            cursor.execute(executor_sql, (ispolnitel_id,))
            executor_data = cursor.fetchone()

            if executor_data:
                executor_id_item = QTableWidgetItem(str(executor_data[0]))
                executor_id_item.setFont(QFont("Comic Sans MS", 10))
                self.table_widget.setItem(row_idx, 7, executor_id_item)  # 7 - номер колонки "Исполнитель"

        db.close()
        
    def load_requests(self):
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = "SELECT * FROM zayavki"
        cursor.execute(sql)
        data = cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                # Установите шрифт Comic Sans MS для элементов таблицы
                item.setFont(QFont("Comic Sans MS", 10))

                self.table_widget.setItem(row_idx, col_idx, item)

            # Получите статус для установки начального значения выпадающего списка
            status_item = self.table_widget.item(row_idx, 6)  # Столбец "Статус"
            if status_item is not None:
                current_status = status_item.text()

                # Создайте выпадающий список и установите начальное значение
                status_combobox = QComboBox()
                status_combobox.addItems(["В ожидании", "В работе", "Выполнено"])
                status_combobox.setCurrentText(current_status)

                self.table_widget.setCellWidget(row_idx, 6, status_combobox)

            # Получите ID исполнителя из базы данных и установите его в колонку "Исполнитель"
            ispolnitel_id = row_data[8]  # Индекс столбца "Ispolnitel_id" в данных
            executor_sql = "SELECT Ispolnitel_id FROM ispolniteli WHERE ispolnitel_id = %s"
            cursor.execute(executor_sql, (ispolnitel_id,))
            executor_data = cursor.fetchone()

            if executor_data:
                executor_id_item = QTableWidgetItem(str(executor_data[0]))
                executor_id_item.setFont(QFont("Comic Sans MS", 10))
                self.table_widget.setItem(row_idx, 7, executor_id_item)  # 7 - номер колонки "Исполнитель"

        # Установите стили для таблицы
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #333;
                color: white;
                gridline-color: #555;
                alternate-background-color: #444;
                selection-background-color: #6A0EAD;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #666;
                border: 1px solid #555;
            }
            QTableWidget::item {
                background-color: #333;
                padding-left: 10px;
            }
            QTableWidget::item:selected {
                background-color: #6A0EAD;
            }
        """)

        db.close()

    def save_all_changes(self):
        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        for row in range(self.table_widget.rowCount()):
            # Получите ID и новый статус из выпадающего списка
            request_id_item = self.table_widget.item(row, 0)
            status_combobox = self.table_widget.cellWidget(row, 6)  # Столбец "Статус" с выпадающим списком

            if request_id_item is not None and status_combobox is not None:
                request_id_value = request_id_item.text()
                new_status = status_combobox.currentText()

                # Обновите статус в базе данных, используя правильное имя поля
                sql_update_status = "UPDATE zayavki SET Status_zayavki = %s WHERE ID_zayavki = %s"
                cursor.execute(sql_update_status, (new_status, request_id_value))

        db.commit()
        db.close()

        # Выводим уведомление
        success_message = QMessageBox()
        success_message.setWindowTitle("Успешно!")
        success_message.setText("Изменения успешно сохранены.")
        success_message.setIcon(QMessageBox.Icon.Information)
        success_message.exec()

class RepairRequestApp(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Учет заявок на ремонт оборудования")
        self.setGeometry(100, 100, 600, 400)

        # Определение основного экрана
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Центрирование окна
        self.setGeometry(
            screen_geometry.width() // 2 - 300,
            screen_geometry.height() // 2 - 200,
            600,
            400
        )

        # Загрузка изображения с интернета
        icon_url = "https://cdn-icons-png.flaticon.com/512/81/81924.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            # Создание QPixmap из байтового массива
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            # Установка значка окна
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        comic_sans_font = QFont("Comic Sans MS", 10)

        self.label_title = QLabel("Добавление новой заявки")
        self.label_title.setFont(comic_sans_font)
        self.label_date_added = QLabel("Дата добавления: ")
        self.label_date_added.setFont(comic_sans_font)
        self.label_equipment = QLabel("Оборудование:")
        self.label_equipment.setFont(comic_sans_font)
        self.combo_equipment = QComboBox()
        self.combo_equipment.addItem("Не выбрано")
        self.combo_equipment.addItem("Компьютер")
        self.combo_equipment.addItem("Принтер")
        self.combo_equipment.addItem("Телефон")
        self.combo_equipment.addItem("Ноутбук")
        self.combo_equipment.addItem("Телевизор")
        self.combo_equipment.addItem("Планшет")
        self.combo_equipment.setFont(comic_sans_font)
        self.combo_equipment.setStyleSheet(
            "QComboBox {"
            "border-radius: 10px;"
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
            "}"
        )

        self.label_issue_type = QLabel("Тип неисправности:")
        self.label_issue_type.setFont(comic_sans_font)
        self.combo_issue_type = QComboBox()
        self.combo_issue_type.addItem("Не выбрано")
        self.combo_issue_type.addItem("Техническая неисправность")
        self.combo_issue_type.addItem("Программная неисправность")
        self.combo_issue_type.setFont(comic_sans_font)
        self.combo_issue_type.setStyleSheet(
            "QComboBox {"
            "border-radius: 10px;"
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
            "}"
        )

        self.label_description = QLabel("Описание проблемы:")
        self.label_description.setFont(comic_sans_font)
        self.text_description = QTextEdit()
        self.text_description.setFont(comic_sans_font)
        self.text_description.setStyleSheet(
            "QTextEdit {"
            "border-radius: 10px;"  # Закругление поля описания проблемы
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
            "}"
        )

        self.label_client = QLabel("Клиент:")
        self.label_client.setFont(comic_sans_font)
        self.line_edit_client = QLineEdit()
        self.line_edit_client.setPlaceholderText("Введите ФИО клиента")
        self.line_edit_client.setFont(comic_sans_font)
        self.line_edit_client.setStyleSheet(
            "border-radius: 10px;"  # Закругление полей ввода
            "font-size: 16px;"
            "font-family: 'Comic Sans MS';"
        )

        self.button_add_request = QPushButton("Добавить заявку")
        self.button_add_request.setFont(comic_sans_font)

        self.button_view_all_requests = QPushButton("Все заявки")
        self.button_view_all_requests.setFont(comic_sans_font)

        self.date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_date_added.setText("Дата добавления: " + self.date_added)

        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_date_added)
        layout.addWidget(self.label_equipment)
        layout.addWidget(self.combo_equipment)
        layout.addWidget(self.label_issue_type)
        layout.addWidget(self.combo_issue_type)
        layout.addWidget(self.label_description)
        layout.addWidget(self.text_description)
        client_layout = QHBoxLayout()
        client_layout.addWidget(self.label_client)
        client_layout.addWidget(self.line_edit_client)
        layout.addLayout(client_layout)  # Добавляем метку и поле ввода ФИО в один горизонтальный блок
        layout.addWidget(self.button_add_request)
        layout.addWidget(self.button_view_all_requests)
        central_widget.setLayout(layout)

        self.request_counter = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.button_add_request.clicked.connect(self.add_request)
        self.button_view_all_requests.clicked.connect(self.view_all_requests)

        button_style = """
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: 'Comic Sans MS';
            }
            QPushButton:hover {
                background-color: #6A0EAD;
            }
        """
        self.button_add_request.setStyleSheet(button_style)
        self.button_view_all_requests.setStyleSheet(button_style)

    def update_time(self):
        self.date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_date_added.setText("Дата добавления: " + self.date_added)

    def add_request(self):
        request_number = str(self.request_counter)
        self.request_counter += 1

        equipment = self.combo_equipment.currentText()
        issue_type = self.combo_issue_type.currentText()
        description = self.text_description.toPlainText()
        
        client = self.line_edit_client.text()
        
        status = "В ожидании"

        db = mysql.connector.connect(
            host="192.168.15.95",
            port=3306,
            user="user27",
            password="62462",
            database="user27"
        )

        cursor = db.cursor()

        sql = """
        INSERT INTO zayavki (Create_date, Oborudovanie, Tip_neispravnosti, Opisanie_problemi, Nickname_client, Status_zayavki)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (self.date_added, equipment, issue_type, description, client, status)
        cursor.execute(sql, val)
        db.commit()
        db.close()

        print("Номер заявки:", request_number)
        print("Дата добавления:", self.date_added)
        print("Оборудование:", equipment)
        print("Тип неисправности:", issue_type)
        print("Описание проблемы:", description)
        print("Клиент:", client)
        print("Статус заявки:", status)

    def view_all_requests(self):
        accounting_window = AccountingWindow()
        accounting_window.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    result = login_dialog.exec()

    if result == QDialog.DialogCode.Accepted:
        main_window = RepairRequestApp(tuple(login_dialog.get_user_data()))
        main_window.show()

    sys.exit(app.exec())           