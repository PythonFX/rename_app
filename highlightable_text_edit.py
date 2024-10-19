from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

class HighlightableTextEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.lines = []

    def update_highlight(self, search_text):
        if not search_text:
            return
        self.text_edit.clear()
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor('yellow'))
        highlight_format.setForeground(QColor('black'))

        cursor = QTextCursor(self.text_edit.document())
        original_format = cursor.charFormat()

        for index, line in enumerate(self.lines):
            cursor.insertText(line)
            print(index, line)
            remaining_line = line
            last_offset = 0
            while search_text in remaining_line:
                start_index = line.find(search_text)
                end_index = start_index + len(search_text)
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start_index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end_index - start_index)
                cursor.mergeCharFormat(highlight_format)
                cursor.movePosition(QTextCursor.EndOfLine)
            cursor.setCharFormat(original_format)
            cursor.insertText('\n')

    def display_text(self, lines):
        self.lines = lines
        self.text_edit.clear()
        for line in lines:
            self.text_edit.append(line)