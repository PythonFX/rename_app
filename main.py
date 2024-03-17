import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QDialog
from PyQt5.QtWidgets import QRadioButton, QLineEdit, QGroupBox, QCheckBox
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt


class RuleDialog(QDialog):
    def __init__(self, fileListWidget, targetListWidget):
        super().__init__()
        self.fileListWidget = fileListWidget
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
        if not self.selectedFiles or self.fileListWidget.count() == 0:
            print("No files selected for renaming or no target files.")
            return

        for i in range(min(self.fileListWidget.count(), len(self.selectedFiles))):
            originalFilePath = self.fileListWidget.item(i).text()
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


class DragDropWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drop Files Here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color : lightgrey; }")
        self.setAcceptDrops(True)
        self.isVideoPriority = True

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            filePaths = [url.toLocalFile() for url in urls]
            self.processFiles(filePaths)

    def processFiles(self, filePaths):
        videoExtensions = ['mp4', 'mkv', 'avi', 'wmv', 'm4v', 'mov']
        videoFiles = sorted([f for f in filePaths if f.split('.')[-1].lower() in videoExtensions], key=lambda f: f.lower())
        otherFiles = sorted([f for f in filePaths if f.split('.')[-1].lower() not in videoExtensions], key=lambda f: f.lower())

        if self.isVideoPriority:
            sourceFiles = videoFiles
            targetFiles = otherFiles
        else:
            sourceFiles = otherFiles
            targetFiles = videoFiles

        minCount = min(len(sourceFiles), len(targetFiles))
        for i in range(minCount):
            sourceFileName = sourceFiles[i].rsplit('.', 1)[0]  # Get the file name without extension
            targetFileFullPath = targetFiles[i]
            targetFileExtension = targetFileFullPath.rsplit('.', 1)[-1]
            newFileName = f"{sourceFileName}.{targetFileExtension}"
            os.rename(targetFileFullPath, newFileName)
            print(f"Renamed {targetFileFullPath} to {newFileName}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batch File Renamer")
        self.setGeometry(100, 100, 1280, 800)
        self.currentFolderPath = ''
        self.files = []
        self.initUI()

    def initUI(self):
        # Main layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QHBoxLayout()

        # Left section
        leftLayout = QVBoxLayout()
        openButton = QPushButton("Open Files")
        openButton.clicked.connect(self.openFileDialog)
        self.fileListWidget = QListWidget()
        leftLayout.addWidget(openButton)
        leftLayout.addWidget(self.fileListWidget)


        # Middle section: renaming rules
        middleLayout = QVBoxLayout()
        self.ruleGroupBox = QGroupBox("Renaming Rules")
        rulesLayout = QVBoxLayout()

        # Horizontal layout for radio buttons
        radioLayout = QHBoxLayout()
        self.addRadioButton = QRadioButton("Add")
        self.deleteRadioButton = QRadioButton("Delete")
        self.replaceRadioButton = QRadioButton("Replace")
        self.addRadioButton.setChecked(True)  # Set 'add' as the default selection

        # Add radio buttons to the horizontal layout
        radioLayout.addWidget(self.addRadioButton)
        radioLayout.addWidget(self.deleteRadioButton)
        radioLayout.addWidget(self.replaceRadioButton)

        # Input fields
        self.inputNameTextField = QLineEdit()
        self.inputNameTextField.textChanged.connect(self.onRuleChanged)
        self.outputNameTextField = QLineEdit()
        self.outputNameTextField.textChanged.connect(self.onRuleChanged)

        # Connect radio buttons to slot to enable/disable second input field
        self.addRadioButton.toggled.connect(self.onRuleChanged)
        self.deleteRadioButton.toggled.connect(self.onRuleChanged)
        self.replaceRadioButton.toggled.connect(self.onRuleChanged)

        # Add a checkbox
        self.videoPriorityCheckBox = QCheckBox("Video filename priority")
        self.videoPriorityCheckBox.setChecked(True)
        self.videoPriorityCheckBox.stateChanged.connect(self.onVideoPriorityCheckBoxStateChanged)  # Connect to a slot

        # confirm button
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.clicked.connect(self.confirmRenaming)


        # Add the radio layout and input fields to the rules layout
        rulesLayout.addLayout(radioLayout)  # Add radio buttons in a horizontal layout
        rulesLayout.addWidget(self.inputNameTextField)
        rulesLayout.addWidget(self.outputNameTextField)
        rulesLayout.addWidget(self.videoPriorityCheckBox)
        rulesLayout.addWidget(self.confirmButton)
        self.ruleGroupBox.setLayout(rulesLayout)
        middleLayout.addWidget(self.ruleGroupBox)


        # Right section
        rightLayout = QVBoxLayout()
        ruleButton = QPushButton("Rule")
        ruleButton.clicked.connect(self.openRuleDialog)
        self.targetListWidget = QListWidget()
        rightLayout.addWidget(ruleButton)
        rightLayout.addWidget(self.targetListWidget)

        layout.addLayout(leftLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(rightLayout)
        self.dragDropWidget = DragDropWidget()
        layout.addWidget(self.dragDropWidget)
        centralWidget.setLayout(layout)

    def onRuleChanged(self):
        # Enable the second input field only for 'replace' mode
        # add content
        # remove content
        # replace content
        if self.replaceRadioButton.isChecked():
            # get the content of the textFromInput InputField
            textFromInput = self.inputNameTextField.text()
            textFromOutput = self.outputNameTextField.text()
            print(textFromInput, textFromOutput)

            for idx, file in enumerate(self.files):
                new_name = file.replace(textFromInput, textFromOutput)
                self.targetListWidget.item(idx).setText(new_name)
        self.outputNameTextField.setEnabled(self.replaceRadioButton.isChecked())

    def onVideoPriorityCheckBoxStateChanged(self):
        self.dragDropWidget.isVideoPriority = self.videoPriorityCheckBox.isChecked()

    def openFileDialog(self):
        settings = QSettings("YourCompanyName", "BatchFileRenamer")
        defaultDir = settings.value("lastUsedDir", "D:/Download")  # Default to D:/Download if not set
        options = QFileDialog.Options()
        self.files, _ = QFileDialog.getOpenFileNames(self, "Select Files", defaultDir, "All Files (*);;Text Files (*.txt)",
                                                    options=options)
        if self.files:
            self.currentFolderPath = defaultDir
            print(self.currentFolderPath)
            self.fileListWidget.clear()
            for file in self.files:
                filename = file.split('/')[-1]  # Extract the filename from the path
                self.fileListWidget.addItem(filename)
            # For demonstration, use the filenames in the target list as well
            self.targetListWidget.clear()  # Clear the list before adding new items
            self.targetListWidget.addItems([file.split('/')[-1] for file in self.files])
            # Save the directory of the first selected file for next time
            lastUsedDir = os.path.dirname(self.files[0])
            settings.setValue("lastUsedDir", lastUsedDir)

    def openRuleDialog(self):
        # Pass fileListWidget and targetListWidget to the dialog
        self.ruleDialog = RuleDialog(self.fileListWidget, self.targetListWidget)
        self.ruleDialog.exec_()

    import os

    def confirmRenaming(self):
        if self.fileListWidget.count() != self.targetListWidget.count():
            print("The number of original files and target filenames does not match.")
            return

        for i in range(self.fileListWidget.count()):
            originalFilePath = os.path.join(self.currentFolderPath, self.fileListWidget.item(i).text())
            newFilePath = os.path.join(self.currentFolderPath, self.targetListWidget.item(i).text())
            try:
                os.rename(originalFilePath, newFilePath)
                print(f"Renamed: {originalFilePath} to {newFilePath}")
            except Exception as e:
                print(f"Error renaming {originalFilePath} to {newFilePath}: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
