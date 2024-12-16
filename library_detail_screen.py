from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from card_edit_modal import CardEditModal
from constants import BUTTON_STYLE, ADD_BUTTON_STYLE
from db import get_cards, update_card_stat, get_card, clear_card_stat
from library_edit_modal import LibraryEditModal


class LibraryDetailScreen(QWidget):
    def __init__(self, library_name, on_back_clicked):
        super().__init__()
        self.library_name = library_name
        self.on_back_clicked = on_back_clicked
        self.rows_to_card_ids = {}
        self.row = 0
        self.sureness_evaluation_in_progress = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Кнопка назад
        back_btn = QPushButton("← Назад к библиотекам", self)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.clicked.connect(self.on_back_clicked)
        layout.addWidget(back_btn)

        # Заголовок с названием библиотеки
        title_label = QLabel(f'Библиотека: {self.library_name}', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.fill_table()
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        self.table.cellClicked.connect(self.handle_cell_click)
        self.table.cellDoubleClicked.connect(self.show_card_modal)

        self.table.horizontalHeader().setVisible(False)  # Hide horizontal headers
        self.table.verticalHeader().setVisible(False)  # Hide vertical headers

        layout.addWidget(self.table)

        # Кнопки навигации
        button_layout = QVBoxLayout()

        self.clear_stat_button = QPushButton("Очистить статистику", self)
        self.clear_stat_button.setStyleSheet(BUTTON_STYLE)
        self.clear_stat_button.clicked.connect(self.clear_stat)
        button_layout.addWidget(self.clear_stat_button)

        self.add_card_button = QPushButton("Добавить карточку", self)
        self.add_card_button.setStyleSheet(BUTTON_STYLE)
        self.add_card_button.clicked.connect(self.show_card_modal)
        button_layout.addWidget(self.add_card_button)

        self.edit_library_button = QPushButton("Изменить библиотеку", self)
        self.edit_library_button.setStyleSheet(ADD_BUTTON_STYLE)
        self.edit_library_button.clicked.connect(self.edit_library_modal)
        button_layout.addWidget(self.edit_library_button)

        layout.addLayout(button_layout)

    def fill_table(self):
        self.table.clearContents()

        cards = get_cards(self.library_name)
        self.table.setRowCount(len(cards))

        for i, card in enumerate(cards):
            que = QTableWidgetItem(card[1])
            ans = QTableWidgetItem(card[2])
            que.setFlags(Qt.ItemFlag.ItemIsEnabled)
            ans.setFlags(Qt.ItemFlag.ItemIsEnabled)
            ans.setForeground(QColor("transparent"))
            self.table.setItem(i, 0, que)
            self.table.setItem(i, 1, ans)
            progress_bar = QProgressBar()
            # progress_bar.setFixedWidth(200)
            # progress_bar.setGeometry(50, 50, 200, 30)
            progress_bar.setValue(self.calc_progress(card))
            self.table.setCellWidget(i, 2, progress_bar)
            self.rows_to_card_ids[i] = card[0]

    def show_card_modal(self, row=None, column=None):
        if self.sureness_evaluation_in_progress:
            return
        card_id = self.rows_to_card_ids[row] if row is not False else None
        modal = CardEditModal(self.library_name, card_id)
        modal.exec()
        self.fill_table()

    def edit_library_modal(self):
        if self.sureness_evaluation_in_progress:
            return
        modal = LibraryEditModal(self.library_name)
        modal.exec()
        self.on_back_clicked()

    def resizeEvent(self, event):
        total_width = self.table.viewport().width()
        self.table.setColumnWidth(0, int(total_width * 0.35))
        self.table.setColumnWidth(1, int(total_width * 0.35))
        self.table.setColumnWidth(2, int(total_width * 0.3))
        super().resizeEvent(event)

    def calc_progress(self, card):
        if card[4] == 0:
            return 0
        return round(float(card[5]) / card[4] * 25)

    def handle_cell_click(self, row, column):
        if column == 1:
            if self.sureness_evaluation_in_progress:
                return
            self.sureness_evaluation_in_progress = True
            self.row = row
            item = self.table.item(row, column)
            item.setForeground(QColor("black"))
            bar = self.table.cellWidget(row, 2)
            bar.hide()
            button1 = QPushButton(":(")
            button1.setFixedSize(40, 40)
            button2 = QPushButton(":|")
            button2.setFixedSize(40, 40)
            button3 = QPushButton(":)")
            button3.setFixedSize(40, 40)
            button4 = QPushButton(":D")
            button4.setFixedSize(40, 40)
            button1.clicked.connect(self.make_button_handler(1))
            button2.clicked.connect(self.make_button_handler(2))
            button3.clicked.connect(self.make_button_handler(3))
            button4.clicked.connect(self.make_button_handler(4))
            layout = QHBoxLayout()
            layout.addWidget(button1)
            layout.addWidget(button2)
            layout.addWidget(button3)
            layout.addWidget(button4)
            cell_widget = QWidget()
            cell_widget.setLayout(layout)
            self.table.setCellWidget(row, 2, cell_widget)

    def make_button_handler(self, knowledge_feeling_number):
        def knowledge_feeling_button_clicked():
            update_card_stat(self.rows_to_card_ids[self.row], knowledge_feeling_number)
            item = self.table.item(self.row, 1)
            item.setForeground(QColor("transparent"))
            self.sureness_evaluation_in_progress = False
            progress_bar = QProgressBar()
            card = get_card(self.rows_to_card_ids[self.row])
            progress_bar.setValue(self.calc_progress(card))
            self.table.setCellWidget(self.row, 2, progress_bar)

        return knowledge_feeling_button_clicked

    def clear_stat(self):
        if self.sureness_evaluation_in_progress:
            return
        confirmation = QMessageBox.question(
            self,
            "Подтверждение сброса",
            "Вы уверены, что хотите сбросить прогресс?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            clear_card_stat(self.library_name)
            self.fill_table()
