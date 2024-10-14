import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLabel, QSpinBox, QFormLayout, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QTimer

class TextStatsCounter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.words_per_page = 250  # Default value
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Statistics Counter')
        self.setGeometry(100, 100, 500, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create text edit
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Create labels for stats
        stats_layout = QHBoxLayout()
        self.word_count_label = QLabel('Words: 0')
        self.char_count_label = QLabel('Characters: 0')
        self.page_count_label = QLabel('Pages: 0')
        
        stats_layout.addWidget(self.word_count_label)
        stats_layout.addWidget(self.char_count_label)
        stats_layout.addWidget(self.page_count_label)
        
        layout.addLayout(stats_layout)

        # Create form for words per page input
        form_layout = QFormLayout()
        self.words_per_page_input = QSpinBox()
        self.words_per_page_input.setRange(1, 1000)
        self.words_per_page_input.setValue(self.words_per_page)
        self.words_per_page_input.valueChanged.connect(self.update_words_per_page)
        form_layout.addRow("Words per page:", self.words_per_page_input)
        layout.addLayout(form_layout)

        # Create Save button
        self.save_button = QPushButton('Save File')
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        # Set up timer for updating stats
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(100)  # Update every 100 ms

    def update_words_per_page(self, value):
        self.words_per_page = value
        self.update_stats()

    def update_stats(self):
        text = self.text_edit.toPlainText()
        
        # Word count
        words = len(text.split())
        self.word_count_label.setText(f'Words: {words}')
        
        # Character count (including spaces)
        chars = len(text)
        self.char_count_label.setText(f'Characters: {chars}')
        
        # Page count (using customizable words per page)
        pages = max(1, round(words / self.words_per_page, 1))
        self.page_count_label.setText(f'Pages: {pages}')

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())

def main():
    app = QApplication(sys.argv)
    ex = TextStatsCounter()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()