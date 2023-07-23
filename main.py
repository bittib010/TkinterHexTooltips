from tkinter import Tk, OptionMenu, StringVar, Text
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
        self.drop.grid(row=0, column=0)

class TextWidget:
    def __init__(self, master):
        self.master = master
        self.textWidget = Text(master, width=47, height=54, font=('Courier 10 bold'), bd=4, padx=5)
        self.popupText = Text(master, width=48, height=48, font=('Courier 12 bold'), bd=4, padx=5)
        self.textWidget.grid(row=1, column=0, columnspan=2)
        self.popupText.grid(row=1, column=2)

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
        self.showSelection()

    def iterSelection(self, mySelection):
        for key in mySelection:
            tag = key
            text = mySelection[key][0]
            self.text_widget.textWidget.insert('end', text, (tag,))
            self.text_widget.textWidget.tag_configure(tag)
            self.text_widget.textWidget.tag_bind(tag, "<Enter>",
                                                 lambda event, currentTag=tag, popup=mySelection[key][1]: self.popItUp(popup, 'red', currentTag))
            self.text_widget.textWidget.tag_bind(tag, "<Leave>",
                                                 lambda event, currentTag=tag: self.popItUp(OPTIONS_INFO[self.dropdown.clicked.get()][1], 'white', currentTag))

    def popItUp(self, text, color, currTag):
        self.text_widget.update_popup_text(text, currTag)
        self.text_widget.highlight_tag(currTag, color)

    def showSelection(self, *args):
        currentSelection = self.dropdown.clicked.get()
        self.text_widget.textWidget.delete('1.0', 'end')
        selection_info = OPTIONS_INFO[currentSelection]
        self.iterSelection(selection_info[0])
        self.text_widget.update_popup_text(selection_info[1], None)

if __name__ == "__main__":
    root = Tk()
    app = Main(root)
    root.title("Poppetypop")
    root.geometry("900x900+500+50")
    root.mainloop()
