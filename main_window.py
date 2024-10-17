import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QDialog
from PyQt5.QtWidgets import QRadioButton, QLineEdit, QGroupBox, QCheckBox
from PyQt5.QtCore import QSettings
from drag_drop_widget import DragDropWidget
from rule_dialog import RuleDialog


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
        main_layout = QHBoxLayout()

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

        # combine layouts
        main_layout.addLayout(leftLayout)
        main_layout.addLayout(middleLayout)
        main_layout.addLayout(rightLayout)
        self.dragDropWidget = DragDropWidget()
        main_layout.addWidget(self.dragDropWidget)
        centralWidget.setLayout(main_layout)

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
