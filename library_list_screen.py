from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from constants import BUTTON_STYLE, ADD_BUTTON_STYLE
from db import get_libraries
from library_edit_modal import LibraryEditModal


class LibraryListScreen(QWidget):
    library_selected = pyqtSignal(str)
    refresh_library = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        library_layout = QVBoxLayout()
        self.setLayout(library_layout)

        # Заголовок для экрана библиотеки
        title_label = QLabel('Выберите библиотеку', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        library_layout.addWidget(title_label)

        # Добавляем кнопки библиотек
        libraries = get_libraries()
        self.button_layout = QVBoxLayout()
        for lib in libraries:
            btn = QPushButton(lib[0], self)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.clicked.connect(lambda checked, lib=lib: self.library_selected.emit(lib[0]))
            self.button_layout.addWidget(btn)
        library_layout.addLayout(self.button_layout)

        btn = QPushButton("Добавить библиотеку", self)
        btn.setStyleSheet(ADD_BUTTON_STYLE)
        btn.clicked.connect(self.on_click)
        library_layout.addWidget(btn)

    def on_click(self):
        modal = LibraryEditModal()
        modal.exec()
        self.refresh_button_layout()

    def refresh_button_layout(self):
        self.refresh_library.emit()
