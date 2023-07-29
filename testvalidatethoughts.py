import tkinter as tk
from tkinter import filedialog
import json
import random

def random_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

class HexViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.file_info = {
  "SQLiteDatabase": {
    "header": {
      "index": 0,
      "size": 16,
      "information": "The header string: \"SQLite format 3\\000\". This is the magic string that identifies the file as a valid SQLite database file."
    },
    "pageSizeBytes": {
      "index": 17,
      "size": 2,
      "information": "The database page size in bytes. Must be a power of two between 512 and 32768 inclusive, or the value 1 representing a page size of 65536. The size of the database pages affects the performance and storage efficiency of the database. The default page size is 4096 bytes."
    },
    "writeVersion": {
      "index": 19,
      "size": 1,
      "information": "File format write version. 1 for legacy; 2 for Write-Ahead Logging (WAL). The write version indicates the version of the database file format. Legacy mode (write version 1) uses rollback journal mode for transactions, while Write-Ahead Logging mode (write version 2) uses a log file for transactions, which provides better concurrency and crash recovery capabilities."
    },
    "fileChangeCounter": {
      "index": 24,
      "size": 4,
      "information": "The file change counter is a 32-bit unsigned integer at offset 24 that is incremented whenever the database file changes. It is used by some VFS (Virtual File System) to cache the file's content. It helps in detecting when the database file has changed since it was last accessed."
    },
    "databaseSizePages": {
      "index": 28,
      "size": 4,
      "information": "The size of the database file in pages. It is a 32-bit unsigned integer at offset 28. The database file size in bytes can be calculated by multiplying this value by the page size."
    },
    "firstFreelistTrunk": {
      "index": 32,
      "size": 4,
      "information": "The page number of the first freelist trunk page. A freelist trunk page is the head of a linked list of free pages that can be reused for new content. This is a 32-bit unsigned integer at offset 32. If the database has no free pages, the value will be 0."
    },
    "totalFreelistPages": {
      "index": 36,
      "size": 4,
      "information": "The total number of freelist pages. A freelist page is used to store a list of other free pages in the database. This is a 32-bit unsigned integer at offset 36. If there are no free pages, the value will be 0."
    },
    "schemaCookie": {
      "index": 40,
      "size": 4,
      "information": "The schema cookie is a 32-bit unsigned integer at offset 40. It is incremented whenever the database schema changes. The schema cookie is used by clients to determine if their cached schema is still valid."
    },
    "schemaFormatNumber": {
      "index": 44,
      "size": 4,
      "information": "The schema format number is a 32-bit unsigned integer at offset 44. It is used to determine the format of the database schema. The format number is incremented whenever the database schema changes."
    },
    "defaultPageCacheSize": {
      "index": 47,
      "size": 4,
      "information": "The default page cache size is a 32-bit signed integer at offset 47. This value represents the suggested maximum number of pages in the page cache. A page cache is a cache that holds frequently accessed pages in memory to improve database performance."
    }
  }
}

        self.section_colors = {section: random_color() for section in self.file_info["SQLiteDatabase"]}

        self.open_button = tk.Button(self, text='Open File', command=self.open_file)
        self.open_button.pack()

        self.text_box = tk.Text(self, width=40, font=('Courier', 10))
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.info_box = tk.Text(self, width=40)
        self.info_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        with open(filepath, 'rb') as f:
            data = f.read()

        hex_data = [f'{b:02x}' for b in data]

        self.text_box.delete('1.0', tk.END)  # clear existing data

        for i in range(len(hex_data)):
            byte = hex_data[i]
            tag = f'byte_{i}'
            info = self.find_byte_info(i)
            if info:
                self.text_box.tag_configure(tag, background=self.section_colors[info["section"]])
            self.text_box.insert(tk.END, byte + ' ' if (i+1) % 16 else '\n', tag)

        self.text_box.bind('<Motion>', self.on_mouse_over)

    def find_byte_info(self, byte_index):
        for section_name in self.file_info["SQLiteDatabase"]:
            section = self.file_info["SQLiteDatabase"][section_name]
            if byte_index >= section["index"] and byte_index < section["index"] + section["size"]:
                return {"section": section_name, **section}
        return None

    def on_mouse_over(self, event):
        tag_names = self.text_box.tag_names(f'@{event.x},{event.y}')
        byte_tags = [tag for tag in tag_names if tag.startswith('byte_')]
        if byte_tags:
            byte_index = int(byte_tags[0].replace('byte_', ''))
            info = self.find_byte_info(byte_index)
            if info:
                self.info_box.delete('1.0', tk.END)
                self.info_box.insert(tk.END, info["information"])

if __name__ == '__main__':
    app = HexViewer()
    app.mainloop()
