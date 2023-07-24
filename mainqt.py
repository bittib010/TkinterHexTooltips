import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QComboBox, QWidget, QSpinBox
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtCore import Qt
import hexInfo
from PyQt5 import *


OPTIONS_INFO = {
    "Windows NTFS - Boot Sector": (hexInfo.windowsNTFSVBR, hexInfo.windowsNTFSVBRInfo),
    "Windows NTFS - MFT File Record": (hexInfo.windowsNTFSMFTFileRecord, hexInfo.windowsNTFSMFTInfo),
}

class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        super(CustomPlainTextEdit, self).mouseMoveEvent(event)
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
        self.window().updatePopupText(False)

    def mousePressEvent(self, event):
        super(CustomPlainTextEdit, self).mousePressEvent(event)
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
        self.window().updatePopupText(True)


class HexViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.combobox = QComboBox()
        self.textWidget = CustomPlainTextEdit()
        self.asciiWidget = CustomPlainTextEdit()
        self.popupText = QPlainTextEdit()
        self.byteWidthBox = QSpinBox()

        # Setup widgets
        self.combobox.addItems(OPTIONS_INFO.keys())
        self.textWidget.setReadOnly(True)
        self.textWidget.setFont(QFont("Monospace", 12))  # Set font to Courier with size 10
        self.asciiWidget.setReadOnly(True)
        self.asciiWidget.setFont(QFont("Monospace", 10))  # Set font to Courier with size 10
        self.popupText.setReadOnly(True)
        self.byteWidthBox.setValue(16)
        self.byteWidthBox.valueChanged.connect(self.showSelection)

        # Setup widgets
        self.combobox.addItems(OPTIONS_INFO.keys())

        # Connect signals
        self.combobox.currentTextChanged.connect(self.showSelection)

        # Create layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.textWidget)
        hbox.addWidget(self.asciiWidget)
        hbox.addWidget(self.popupText)

        vbox = QVBoxLayout()
        vbox.addWidget(self.combobox)
        vbox.addWidget(self.byteWidthBox)
        vbox.addLayout(hbox)

        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(vbox)

        self.setCentralWidget(central_widget)
        self.setGeometry(0, 70, 6000, 6000)
        self.setWindowTitle("Poppetypop")

    def showSelection(self, *args):
        currentSelection = self.combobox.currentText()
        self.textWidget.clear()
        self.asciiWidget.clear()
        self.color_dict = {key: QColor(*random.choices(range(256), k=3)) for key in OPTIONS_INFO[currentSelection][0].keys()}  # Assign random color to each hex sequence

        cursor = self.textWidget.textCursor()
        asciiCursor = self.asciiWidget.textCursor()
        format = QTextCharFormat()

        hexBytes = []
        asciiBytes = []
        for key, value in OPTIONS_INFO[currentSelection][0].items():
            hexBytes.extend(value[0].split())
            asciiBytes.extend([chr(int(b, 16)) if 32 <= int(b, 16) <= 126 else '.' for b in value[0].split()])

        for i in range(0, len(hexBytes), self.byteWidthBox.value()):
            format.setBackground(QColor("white"))
            cursor.insertText(' '.join(hexBytes[i:i+self.byteWidthBox.value()]), format)
            cursor.insertText('\n')
            asciiCursor.insertText(''.join(asciiBytes[i:i+self.byteWidthBox.value()]), format)
            asciiCursor.insertText('\n')

        self.popupText.setPlainText(OPTIONS_INFO[currentSelection][1])

    def updatePopupText(self, isClicked):
        cursor = self.textWidget.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()
        for key, value in OPTIONS_INFO[self.combobox.currentText()][0].items():
            if word in value[0].replace(' ', ''):
                format = QTextCharFormat()
                format.setBackground(QColor("white") if not isClicked else self.color_dict[key])
                cursor.setCharFormat(format)
                self.popupText.setPlainText(value[1])
                return
        self.popupText.setPlainText(OPTIONS_INFO[self.combobox.currentText()][1])

if __name__ == "__main__":
    app = QApplication([])
    window = HexViewer()
    window.show()
    app.exec_()

