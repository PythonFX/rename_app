from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLineEdit
from highlightable_text_edit import HighlightableTextEdit


app = QApplication([])

main_widget = QWidget()
layout = QVBoxLayout(main_widget)

highlightable_text_edit = HighlightableTextEdit()
layout.addWidget(highlightable_text_edit)
highlightable_text_edit.setFixedHeight(80)

# Sample lines of text
lines = ["This is line one", "Another line with words", "A third line"]
highlightable_text_edit.display_text(lines)

search_edit = QLineEdit()
search_edit.textChanged.connect(lambda text: highlightable_text_edit.update_highlight(text))
layout.addWidget(search_edit)

main_widget.show()
app.exec_()



