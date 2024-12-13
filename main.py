import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from library_list_screen import LibraryListScreen
from library_detail_screen import LibraryDetailScreen


class Garmoshka(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.library_detail_screen = None
        self.add_library_list_screen()

    def add_library_list_screen(self):
        self.library_list_screen = LibraryListScreen()
        self.library_list_screen.library_selected.connect(self.show_library_detail_screen)
        self.library_list_screen.refresh_library.connect(self.refresh_library_screen)
        self.main_layout.addWidget(self.library_list_screen)

    def show_library_detail_screen(self, library_name):
        self.library_list_screen.hide()

        if self.library_detail_screen:
            self.library_detail_screen.deleteLater()

        self.library_detail_screen = LibraryDetailScreen(library_name, self.show_library_screen)
        self.main_layout.addWidget(self.library_detail_screen)
        self.library_detail_screen.show()

    def show_library_screen(self):
        if self.library_detail_screen:
            self.library_detail_screen.hide()
            self.library_detail_screen.deleteLater()
            self.library_detail_screen = None
        self.refresh_library_screen()

    def refresh_library_screen(self):
        self.library_list_screen.hide()
        self.library_list_screen.deleteLater()
        self.add_library_list_screen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Garmoshka()
    ex.setWindowTitle('Гармошка')
    ex.resize(800, 600)
    ex.show()
    sys.exit(app.exec())
