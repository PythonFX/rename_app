import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QInputDialog
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

class FileListHighlightApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_folder_button = QPushButton('Select Folder')
        self.select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_button)

        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.update_text_edit)
        layout.addWidget(self.search_field)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def select_folder(self):
        folder = QInputDialog.getText(self, 'Select Folder', 'Enter folder path:')[0]
        if folder and os.path.isdir(folder):
            self.current_folder = folder
            self.update_text_edit()

    def update_text_edit(self, search_text):
        self.text_edit.clear()
        if hasattr(self, 'current_folder') and os.path.isdir(self.current_folder):
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor('yellow'))
            highlight_format.setForeground(QColor('black'))
            cursor = QTextCursor(self.text_edit.document())
            original_format = cursor.charFormat()
            for idx, filename in enumerate(os.listdir(self.current_folder)):
                cursor.insertText(filename)
                print(idx, filename)
                if search_text and search_text in filename:
                    start_index = filename.find(search_text)
                    end_index = start_index + len(search_text)
                    cursor.movePosition(QTextCursor.StartOfLine)
                    print('move to start')
                    cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start_index)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end_index - start_index)
                    cursor.mergeCharFormat(highlight_format)
                    cursor.movePosition(QTextCursor.EndOfLine)
                    cursor.setCharFormat(original_format)
                cursor.insertText('\n')
                # cursor.movePosition(QTextCursor.Down)

app = QApplication([])
window = FileListHighlightApp()
window.show()
app.exec_()