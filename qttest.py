import sys
import json
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QFileDialog, QSpinBox, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor, QTextDocument

class FileValidator:
    def __init__(self, template_file):
        with open(template_file, 'r') as f:
            self.file_templates = json.load(f)

    def get_file_type(self, file_data):
        for ext, structures in self.file_templates.items():
            for structure in structures:
                start_index = structure['index'] * 3
                size = structure['size'] * 3
                data = structure['data']
                try:
                    hex_data = bytes.fromhex(data)
                    if file_data.startswith(hex_data) and len(file_data) >= start_index + size:
                        return ext
                except ValueError:
                    pass
        return None

    def get_info_for_sequence(self, sequence):
        sequence = ''.join(sequence.split())
        sequence_length = len(sequence) // 2

        for file_type, structures in self.file_templates.items():
            for structure in structures:
                data = ''.join(structure['data'].split())
                data_size = len(data) // 2

                start_index = structure['index']
                end_index = start_index + data_size
                if start_index <= sequence_length <= end_index and sequence.upper() == data:
                    return structure['information']

        return ''


class InteractiveTextBrowser(QTextBrowser):
    emit_info_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        selected_text = cursor.selectedText()
        if selected_text:
            self.emit_info_signal.emit(selected_text)


class HexViewer(QWidget):
    def __init__(self, template_file):
        super().__init__()

        self.initUI()
        self.validator = FileValidator(template_file)

        self.highlight_structures = []

    def initUI(self):
        self.setGeometry(50, 200, 1500, 1500)
        self.setWindowTitle('Hex Viewer')
        self.showMaximized()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        hex_ascii_layout = QHBoxLayout()

        self.hex_edit = InteractiveTextBrowser()
        hex_ascii_layout.addWidget(self.hex_edit)

        self.ascii_edit = InteractiveTextBrowser()
        hex_ascii_layout.addWidget(self.ascii_edit)

        self.layout.addLayout(hex_ascii_layout)

        self.line_length_input = QSpinBox()
        self.line_length_input.setMinimum(1)
        self.line_length_input.setValue(16)
        self.line_length_input.valueChanged.connect(self.update_display)
        line_length_layout = QHBoxLayout()
        line_length_layout.addWidget(QLabel('Line length:'))
        line_length_layout.addWidget(self.line_length_input)
        self.layout.addLayout(line_length_layout)

        self.encoding_input = QComboBox()
        self.encoding_input.addItems(['utf-8', 'ascii', 'iso-8859-1', 'cp1252', 'utf-16', 'utf-32'])
        self.encoding_input.currentIndexChanged.connect(self.update_display)
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel('Encoding:'))
        encoding_layout.addWidget(self.encoding_input)
        self.layout.addLayout(encoding_layout)

        self.button = QPushButton('Load File')
        self.button.clicked.connect(self.load_file)
        self.layout.addWidget(self.button)

        self.current_data = None

        self.info_edit = QTextBrowser()
        self.layout.addWidget(self.info_edit)

        self.hex_edit.emit_info_signal.connect(self.update_info)
        self.ascii_edit.emit_info_signal.connect(self.update_info)

    def add_highlight_structure(self, index, size, information, color):
        structure = {'index': index, 'size': size, 'information': information, 'color': color}
        self.highlight_structures.append(structure)

    def highlight_data_structures(self):
        if self.current_data is not None:
            hex_data = self.current_data.hex()

            cursor = self.hex_edit.textCursor()

            for structure in self.highlight_structures:
                start_index = structure['index'] * 3
                size = structure['size'] * 3

                if start_index + size > len(hex_data):
                    continue

                hex_format = QTextCharFormat()
                hex_format.setBackground(QColor(structure['color']))

                cursor.setPosition(start_index)
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, size)

                cursor.setCharFormat(hex_format)

    def update_info(self, selected_text):
        if self.current_data is not None:
            hex_sequence = ''.join(selected_text.split())  # Remove spaces from the clicked sequence
            sequence_length = len(hex_sequence) // 2  # Calculate the sequence length in bytes

            for file_type, structures in self.validator.file_templates.items():
                for structure in structures:
                    data = ''.join(structure['data'].split())  # Remove spaces from the template data
                    data_size = len(data) // 2  # Calculate the structure's data size in bytes

                    # Calculate the byte index and check if it is within the structure's range
                    start_index = structure['index']
                    end_index = start_index + data_size
                    if start_index <= sequence_length <= end_index and hex_sequence.upper() == data:
                        self.info_edit.setPlainText(structure['information'])
                        return
            self.info_edit.setPlainText('')


    def update_display(self):
        if self.current_data is not None:
            
            encoding = self.encoding_input.currentText()
            line_length = self.line_length_input.value()

            hex_data = self.current_data.hex()
            hex_width = line_length * 3
            formatted_hex_data = ' '.join([hex_data[i:i+2] for i in range(0, len(hex_data), 2)])
            formatted_hex_data = '\n'.join([formatted_hex_data[i:i+hex_width] for i in range(0, len(formatted_hex_data), hex_width)])
            self.hex_edit.setPlainText(formatted_hex_data)

            try:
                ascii_data = self.current_data.decode(encoding)
                printable_ascii_data = ''.join(c if 32 <= ord(c) < 127 else '.' for c in ascii_data)
                ascii_width = line_length
                formatted_ascii_data = '\n'.join([printable_ascii_data[i:i+ascii_width] for i in range(0, len(printable_ascii_data), ascii_width)])
            except UnicodeDecodeError:
                formatted_ascii_data = '(cannot decode with encoding {})'.format(encoding)
            self.ascii_edit.setPlainText(formatted_ascii_data)

            self.highlight_data_structures()

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'rb') as f:
                self.current_data = f.read()

            file_type = self.validator.get_file_type(self.current_data)
            if file_type is None:
                self.hex_edit.setPlainText("File type mismatch.")
                self.ascii_edit.setPlainText("File type mismatch.")
                self.info_edit.setPlainText("No Information Available")
                return
            else:
                self.highlight_structures = self.validator.file_templates[file_type]

        self.update_display()
        self.hex_edit.moveCursor(QTextCursor.Start)
        self.ascii_edit.moveCursor(QTextCursor.Start)


def main():
    app = QApplication(sys.argv)

    template_file = "file_templates.json"
    viewer = HexViewer(template_file)
    viewer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
