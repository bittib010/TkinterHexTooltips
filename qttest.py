import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QSpinBox, QLabel, QHBoxLayout, QComboBox, QStatusBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QTimer, Qt


class HexViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(50, 200, 1500, 1500)
        self.setWindowTitle('Hex Viewer')
        self.showMaximized()


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        hex_ascii_layout = QHBoxLayout()

        self.hex_edit = QTableWidget()
        self.hex_edit.setStyleSheet("QTableWidget { background-color: black; color: green; }")
        self.hex_edit.cellClicked.connect(self.on_cell_clicked)
        hex_ascii_layout.addWidget(self.hex_edit)

        self.ascii_edit = QTableWidget()
        self.ascii_edit.setStyleSheet("QTableWidget { background-color: black; color: green; }")
        self.ascii_edit.cellClicked.connect(self.on_cell_clicked)
        hex_ascii_layout.addWidget(self.ascii_edit)

        self.hex_edit.setColumnCount(16)
        self.hex_edit.setHorizontalHeaderLabels([f"{i:02X}" for i in range(16)])

        self.ascii_edit.setColumnCount(16)
        self.ascii_edit.setHorizontalHeaderLabels([f"{i:02X}" for i in range(16)])

        self.layout.addLayout(hex_ascii_layout)

        self.line_length_input = QSpinBox()
        self.line_length_input.setMinimum(1)
        self.line_length_input.setValue(16)
        self.line_length_input.valueChanged.connect(self.update_display)
        line_length_layout = QHBoxLayout()
        line_length_layout.addWidget(QLabel('Line length:'))
        line_length_layout.addWidget(self.line_length_input)
        self.layout.addLayout(line_length_layout)

        self.hex_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ascii_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self.encoding_input = QComboBox()
        self.encoding_input.addItems(['iso-8859-1', 'utf-8', 'ascii', 'cp1252', 'utf-16', 'utf-32'])
        self.encoding_input.currentIndexChanged.connect(self.update_display)
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel('Encoding:'))
        encoding_layout.addWidget(self.encoding_input)
        self.layout.addLayout(encoding_layout)

        self.button = QPushButton('Load File')
        self.button.clicked.connect(self.load_file)
        self.layout.addWidget(self.button)

        self.current_data = None
        self.file_size = 0
        self.chunk_size = 1024  # Adjust the chunk size as needed
        self.current_chunk = 0
        self.num_rows = 0

        self.info_edit = QTableWidget()
        self.info_edit.setStyleSheet("QTableWidget { color: green; font: bold 12px; }")
        self.layout.addWidget(self.info_edit)

        # Create status bar to show toast messages
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_toast)

    def update_row_labels(self):
        if self.current_data is not None:
            line_length = self.line_length_input.value()
            num_rows = (len(self.current_data) + line_length - 1) // line_length

            # Calculate the byte offset for each row and convert to decimal format
            byte_offsets = [offset * line_length for offset in range(num_rows)]
            self.hex_edit.setVerticalHeaderLabels([f"{offset:04X}" for offset in byte_offsets])
            self.ascii_edit.setVerticalHeaderLabels([f"{offset:04X}" for offset in byte_offsets])

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
                    self.hex_edit.setRowHeight(i, 2)

                for i, item in enumerate(hex_items):
                    self.hex_edit.setItem(i // line_length, i % line_length, QTableWidgetItem(item))

                try:
                    ascii_data = self.current_data.decode(encoding)
                    printable_ascii_data = ''.join(c if 32 <= ord(c) < 127 else '.' for c in ascii_data)
                    ascii_items = [printable_ascii_data[i:i+1] for i in range(0, len(printable_ascii_data), 1)]

                    self.ascii_edit.setRowCount((len(ascii_items) + line_length - 1) // line_length)
                    self.ascii_edit.setColumnCount(line_length)
                    for i in range(len(ascii_items)):
                        self.ascii_edit.setColumnWidth(i, 2)  # Adjust as needed
                        self.hex_edit.setRowHeight(i, 2)
                    for i, item in enumerate(ascii_items):
                        self.ascii_edit.setItem(i // line_length, i % line_length, QTableWidgetItem(item))
                except UnicodeDecodeError:
                    self.ascii_edit.setRowCount(1)
                    self.ascii_edit.setColumnCount(1)
                    self.ascii_edit.setItem(0, 0, QTableWidgetItem('(cannot decode with encoding {})'.format(encoding)))

            self.update_row_labels()

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'rb') as f:
                self.current_data = f.read()
        self.update_display()

    def on_cell_clicked(self, row, column):
        hex_column_label = self.hex_edit.item(row, column).text()

        ascii_row_label = self.ascii_edit.verticalHeaderItem(row).text()
        ascii_header_text = self.ascii_edit.horizontalHeaderItem(column).text()
        ascii_cell = self.ascii_edit.item(row, column).text()



        # Convert hexadecimal strings to integers
        header_value = int(ascii_header_text, 16)
        row_value = int(ascii_row_label, 16)
        offset = hex(header_value + row_value)[2:].upper()

        ascii_message = f"Offset: {offset}, Cell Value: {ascii_cell} / {hex_column_label}"

        self.show_toast(ascii_message)

        # Synchronize the selected cell in the other table
        self.hex_edit.setCurrentCell(row, column)
        self.ascii_edit.setCurrentCell(row, column)



    def show_toast(self, message):
        self.status_bar.showMessage(message)
        self.timer.start(15000)

    def hide_toast(self):
        self.status_bar.clearMessage()
        self.timer.stop()

def main():
    app = QApplication(sys.argv)
    viewer = HexViewer()
    viewer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
