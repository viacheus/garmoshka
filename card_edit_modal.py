from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QTextEdit,
)

from db import get_card, add_card, update_card, delete_card


class CardEditModal(QDialog):
    def __init__(self, library_id, card_id=None):
        super().__init__()
        self.library_id = library_id
        self.card_id = card_id
        if card_id:
            self.card = get_card(card_id)
        else:
            self.card = [0, "", ""]
        self.setWindowTitle("Изменение вопроса")
        self.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout()

        self.question_field = QTextEdit(self)
        self.question_field.setText(self.card[1])
        self.answer_field = QTextEdit(self)
        self.answer_field.setText(self.card[2])

        layout.addWidget(QLabel("Вопрос:"))
        layout.addWidget(self.question_field)
        layout.addWidget(QLabel("Ответ:"))
        layout.addWidget(self.answer_field)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)

        if self.card_id:
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
            "Вы уверены, что хотите удалить вопрос?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            delete_card(self.card_id)

        self.close()

    def on_save(self):
        question = self.question_field.toPlainText()
        answer = self.answer_field.toPlainText()

        if not question or not answer:
            QMessageBox.warning(self, "Ошибка", "Поля вопрос и ответ обязательные.")
            return

        if self.card_id:
            update_card(self.card_id, question, answer)
        else:
            add_card(self.library_id, question, answer)

        self.close()
