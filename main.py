import random
from tkinter import Tk, OptionMenu, StringVar, Text, N, S, E, W, Scrollbar
import hexInfo

OPTIONS_INFO = {
    "Windows NTFS - Boot Sector": (hexInfo.windowsNTFSVBR, hexInfo.windowsNTFSVBRInfo),
    "Windows NTFS - MFT File Record": (hexInfo.windowsNTFSMFTFileRecord, hexInfo.windowsNTFSMFTInfo),
}

class DropdownOption:
    def __init__(self, master, callback):
        self.master = master
        self.clicked = StringVar()
        self.dropdownOpts = list(OPTIONS_INFO.keys())
        self.clicked.set(self.dropdownOpts[0])
        self.drop = OptionMenu(master, self.clicked, *self.dropdownOpts, command=callback)
        self.drop.grid(row=0, column=0, padx=10, pady=10, sticky=W)

class TextWidget:
    def __init__(self, master):
        self.master = master
        master.grid_columnconfigure(0, weight=3)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(1, weight=1)

        self.textWidget = Text(master, font=('Courier 10 bold'), padx=5, bg='white', relief='solid', bd=1)
        self.textScrollbar = Scrollbar(master)  # Create a scrollbar for the textWidget
        self.textScrollbar.config(command=self.textWidget.yview)  # Associate scrollbar with textWidget
        self.textWidget.config(yscrollcommand=self.textScrollbar.set)  # Make textWidget scrollable

        self.popupText = Text(master, font=('Courier 12 bold'), padx=5, bg='white', relief='solid', bd=1)
        self.popupScrollbar = Scrollbar(master)  # Create a scrollbar for the popupText
        self.popupScrollbar.config(command=self.popupText.yview)  # Associate scrollbar with popupText
        self.popupText.config(yscrollcommand=self.popupScrollbar.set)  # Make popupText scrollable

        self.textWidget.grid(row=1, column=0, padx=10, sticky=N+S+W+E)
        self.textScrollbar.grid(row=1, column=1, sticky=N+S)
        self.popupText.grid(row=1, column=2, padx=10, sticky=N+S+W+E)
        self.popupScrollbar.grid(row=1, column=3, sticky=N+S)

    def highlight_tag(self, tag, color):
        self.textWidget.tag_configure(tag, background=color)

    def update_popup_text(self, text, tag):
        self.popupText.delete("1.0", "end")
        self.popupText.insert("1.0", text, (tag,))

class Main:
    def __init__(self, master):
        self.master = master
        self.text_widget = TextWidget(master)
        self.dropdown = DropdownOption(master, self.showSelection)
        self.color_dict = {}
        self.showSelection()

    def iterSelection(self, mySelection):
        i = 0
        for key in mySelection:
            tag = key
            text = mySelection[key][0]
            self.text_widget.textWidget.insert('end', text, (tag,))
            print(i)
            i += 1
            self.text_widget.textWidget.tag_configure(tag)
            self.text_widget.textWidget.tag_bind(tag, "<Enter>",
                                                 lambda event, currentTag=tag, popup=mySelection[key][1]: self.popItUp(popup, self.color_dict.get(currentTag, 'red'), currentTag))
            self.text_widget.textWidget.tag_bind(tag, "<Leave>",
                                                 lambda event, currentTag=tag: self.popItUp(OPTIONS_INFO[self.dropdown.clicked.get()][1], 'white', currentTag))

    def popItUp(self, text, color, currTag):
        self.text_widget.update_popup_text(text, currTag)
        self.text_widget.highlight_tag(currTag, color)

    def showSelection(self, *args):
        currentSelection = self.dropdown.clicked.get()
        self.text_widget.textWidget.delete('1.0', 'end')
        selection_info = OPTIONS_INFO[currentSelection]
        self.color_dict = {key: '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for key in selection_info[0].keys()}
        self.iterSelection(selection_info[0])
        self.text_widget.update_popup_text(selection_info[1], None)

if __name__ == "__main__":
    root = Tk()
    app = Main(root)
    root.title("Poppetypop")
    root.geometry("1200x600+50+50")
    root.configure(bg='#F0F0F0')  # Change to a light background color
    root.mainloop()
