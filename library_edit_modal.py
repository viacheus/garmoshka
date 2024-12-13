import csv

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QLineEdit, QFileDialog,
)

from db import get_card, add_card, update_card, delete_card, update_library, add_library, delete_library


class LibraryEditModal(QDialog):
    def __init__(self, library_id=None):
        super().__init__()
        self.library_id = library_id
        self.setWindowTitle("Изменение библиотеки")
        self.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout()

        self.name_field = QLineEdit(self)
        self.name_field.setText(self.library_id)

        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_field)

        self.file_path_field = QLineEdit()
        layout.addWidget(self.file_path_field)

        self.upload_button = QPushButton("Загрузить файл")
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)

        if self.library_id:
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(self.on_delete)
            button_layout.addWidget(delete_button)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.on_save)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.setModal(True)

    def on_cancel(self):
        self.close()

    def on_delete(self):
        confirmation = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить библиотеку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            delete_library(self.library_id)

        self.close()

    def on_save(self):
        name = self.name_field.text()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Поля название обязательное.")
            return

        file_path = self.file_path_field.text()
        card_list = []
        if file_path:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                card_list = list(reader)

        if self.library_id:
            update_library(self.library_id, name, card_list)
        else:
            add_library(name, card_list)

        self.close()

    def open_file_dialog(self):
        # Диалоговое окно выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                   "CSV файлы (*.csv)")
        # "Все файлы (*.*);;Текстовые файлы (*.csv)")
        if file_path:
            self.file_path_field.setText(file_path)
