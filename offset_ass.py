import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class FileDropWidget(QLabel):
    def __init__(self, callback):
        super().__init__()
        self.setText("\n\n Drop files here \n\n")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa
            }
        """)
        self.setAcceptDrops(True)
        self.callback = callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.callback(files)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ASS Subtitle Time Offset Adjuster')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.offset_input = QLineEdit(self)
        self.offset_input.setPlaceholderText('Enter time offset in seconds...')
        self.layout.addWidget(self.offset_input)

        self.drop_area = FileDropWidget(self.process_files)
        self.layout.addWidget(self.drop_area)

        self.setLayout(self.layout)

    def process_files(self, files):
        offset = float(self.offset_input.text())
        for file_path in files:
            apply_offset_to_ass(file_path, offset)

def apply_offset_to_ass(file_path, offset):
    timestamp_regex = re.compile(r'(Dialogue: \d+,)(\d+:\d{2}:\d{2}\.\d{2}),(\d+:\d{2}:\d{2}\.\d{2})')

    def timestamp_to_seconds(timestamp):
        hours, minutes, seconds = map(float, timestamp.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def seconds_to_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f'{hours:01d}:{minutes:02d}:{seconds:05.2f}'

    updated_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = timestamp_regex.match(line)
            if match:
                prefix = match.group(1)
                start_timestamp, end_timestamp = match.group(2, 3)
                start_seconds = timestamp_to_seconds(start_timestamp) + offset
                end_seconds = timestamp_to_seconds(end_timestamp) + offset
                new_line = f"{prefix}{seconds_to_timestamp(start_seconds)},{seconds_to_timestamp(end_seconds)}" + line[match.end(3):]
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
