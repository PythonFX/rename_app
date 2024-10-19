import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QDialog
from highlightable_text_edit import HighlightableTextEdit


class RuleDialog(QDialog):
    def __init__(self, sourceListWidget: HighlightableTextEdit, targetListWidget):
        super().__init__()
        self.sourceListWidget = sourceListWidget
        self.targetListWidget = targetListWidget
        self.selectedFiles = []  # To store paths of files selected for new names
        self.setWindowTitle("Select Rule")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        selectFilesButton = QPushButton("Select Files for Names")
        selectFilesButton.clicked.connect(self.openFileDialog)
        replaceNamesButton = QPushButton("Replace Names")
        replaceNamesButton.clicked.connect(self.replaceNames)
        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)
        layout.addWidget(selectFilesButton)
        layout.addWidget(replaceNamesButton)
        layout.addWidget(closeButton)
        self.setLayout(layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Replacement Names", "", "All Files (*);;Text Files (*.txt)", options=options)
        if files:
            self.selectedFiles = files

    def replaceNames(self):
        if not self.selectedFiles or self.sourceListWidget.count() == 0:
            print("No files selected for renaming or no target files.")
            return

        for i in range(min(self.sourceListWidget.count(), len(self.selectedFiles))):
            originalFilePath = self.sourceListWidget.text_at(i)
            newFileName = self.selectedFiles[i].split('/')[-1]
            # Extract original file extension
            originalFileExtension = originalFilePath.split('.')[-1] if '.' in originalFilePath else ''
            newFileNameWithoutExtension = newFileName.rsplit('.', 1)[0]
            newFilePath = f"{originalFilePath.rsplit('/', 1)[0]}/{newFileNameWithoutExtension}.{originalFileExtension}"
            # Here you can add the actual file renaming logic using os.rename
            print(f"Would rename: {originalFilePath} to {newFilePath}")
            # Update the target list widget
            if i < self.targetListWidget.count():
                self.targetListWidget.item(i).setText(f"{newFileNameWithoutExtension}.{originalFileExtension}")
            else:
                self.targetListWidget.addItem(f"{newFileNameWithoutExtension}.{originalFileExtension}")