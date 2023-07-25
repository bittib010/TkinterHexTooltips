import sys
import json
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QSpinBox, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtGui import QColor

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
                    if start_index < 0:
                        start_index += len(file_data)
                    if file_data.startswith(hex_data, start_index) and len(file_data) >= start_index + size:
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
                if start_index < 0:
                    start_index += sequence_length
                if start_index <= sequence_length <= end_index and sequence.upper() == data:
                    return structure['information']
        return ''

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

        self.hex_edit = QTableWidget()
        self.hex_edit.setStyleSheet("QTableWidget { background-color: black; color: green; }")
        self.hex_edit.itemClicked.connect(self.update_info)
        hex_ascii_layout.addWidget(self.hex_edit)

        self.ascii_edit = QTableWidget()
        self.ascii_edit.setStyleSheet("QTableWidget { background-color: black; color: green; }")
        self.ascii_edit.itemClicked.connect(self.update_info)
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

        self.info_edit = QTableWidget()
        self.info_edit.setStyleSheet("QTableWidget { color: green; }")
        self.layout.addWidget(self.info_edit)

    def update_display(self):
        if self.current_data is not None:
            encoding = self.encoding_input.currentText()
            line_length = self.line_length_input.value()

            hex_data = self.current_data.hex()
            hex_items = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]

            self.hex_edit.setRowCount((len(hex_items) + line_length - 1) // line_length)
            self.hex_edit.setColumnCount(line_length)

            for i in range(line_length):
                self.hex_edit.setColumnWidth(i, 2)  # Adjust as needed

            for i, item in enumerate(hex_items):
                self.hex_edit.setItem(i // line_length, i % line_length, QTableWidgetItem(item))

            try:
                ascii_data = self.current_data.decode(encoding)
                printable_ascii_data = ''.join(c if 32 <= ord(c) < 127 else '.' for c in ascii_data)
                ascii_items = [printable_ascii_data[i:i+1] for i in range(0, len(printable_ascii_data), 1)]

                self.ascii_edit.setRowCount((len(ascii_items) + line_length - 1) // line_length)
                self.ascii_edit.setColumnCount(line_length)
                for i in range(len(ascii_items)):
                    self.ascii_edit.setColumnWidth(i, 5)  # Adjust as needed

                for i, item in enumerate(ascii_items):
                    self.ascii_edit.setItem(i // line_length, i % line_length, QTableWidgetItem(item))
            except UnicodeDecodeError:
                self.ascii_edit.setRowCount(1)
                self.ascii_edit.setColumnCount(1)
                self.ascii_edit.setItem(0, 0, QTableWidgetItem('(cannot decode with encoding {})'.format(encoding)))

    def update_info(self, clicked_item):
        if self.current_data is not None:
            hex_sequence = clicked_item.text()
            sequence_length = len(hex_sequence) // 2

            for file_type, structures in self.validator.file_templates.items():
                for structure in structures:
                    data = ''.join(structure['data'].split())
                    data_size = len(data) // 2

                    start_index = structure['index']
                    end_index = start_index + data_size
                    if start_index < 0:
                        start_index += sequence_length
                    if start_index <= sequence_length <= end_index and hex_sequence.upper() == data:
                        self.info_edit.setRowCount(1)
                        self.info_edit.setColumnCount(1)
                        self.info_edit.setItem(0, 0, QTableWidgetItem(structure['information']))
                        return
            self.info_edit.setRowCount(1)
            self.info_edit.setColumnCount(1)
            self.info_edit.setItem(0, 0, QTableWidgetItem(''))

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'rb') as f:
                self.current_data = f.read()

            file_type = self.validator.get_file_type(self.current_data)
            if file_type is None:
                self.hex_edit.setRowCount(1)
                self.hex_edit.setColumnCount(1)
                self.hex_edit.setItem(0, 0, QTableWidgetItem("File type mismatch."))

                self.ascii_edit.setRowCount(1)
                self.ascii_edit.setColumnCount(1)
                self.ascii_edit.setItem(0, 0, QTableWidgetItem("File type mismatch."))

                self.info_edit.setRowCount(1)
                self.info_edit.setColumnCount(1)
                self.info_edit.setItem(0, 0                , QTableWidgetItem("No Information Available"))
                return
            else:
                self.highlight_structures = self.validator.file_templates[file_type]

        self.update_display()

def main():
    app = QApplication(sys.argv)
    template_file = "file_templates.json"
    viewer = HexViewer(template_file)
    viewer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
