from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

class HighlightableTextEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.lines = []
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor('yellow'))
        self.highlight_format.setForeground(QColor('black'))
        self.cursor = QTextCursor(self.text_edit.document())
        self.original_format = self.cursor.charFormat()

    def display_lines(self):
        self.text_edit.clear()
        self.cursor.setCharFormat(self.original_format)
        for line in self.lines:
            self.cursor.insertText(line + '\n')

    def update_highlight(self, search_text):
        if not search_text:
            return self.display_lines()
        self.text_edit.clear()
        for line in self.lines:
            self.cursor.insertText(line)
            remaining_line = line
            end_index = 0
            while search_text in remaining_line:
                start_index = remaining_line.find(search_text) + end_index
                end_index = start_index + len(search_text)
                self.cursor.movePosition(QTextCursor.StartOfLine)
                self.cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start_index)
                self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end_index - start_index)
                self.cursor.mergeCharFormat(self.highlight_format)
                remaining_line = line[end_index:]
            self.cursor.movePosition(QTextCursor.EndOfLine)
            self.cursor.setCharFormat(self.original_format)
            self.cursor.insertText('\n')

    def display_text(self, lines):
        self.lines = lines
        self.text_edit.clear()
        for line in lines:
            self.text_edit.append(line)