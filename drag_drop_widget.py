import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


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

    # rename subtitles to match video files
    # if using in batch, make sure the file names are in responding sequence
    # batch processing is very useful when renaming drama series
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