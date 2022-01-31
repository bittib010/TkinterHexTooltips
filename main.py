from tkinter import *
import hexInfo
from functools import partial

class Main(object):
    def __init__(self, master):
        self.master = master

        dropdownOpts = [
            "Windows - NTFS VBR",
            "Windows - NTFS MFT"
        ]

        clicked = StringVar()
        clicked.set(dropdownOpts[0])

        drop = OptionMenu(master, clicked, *dropdownOpts)
        drop.grid(row=0, column=0)
        showSelectedBtn = Button(master, text="Show record", command=lambda: showSelection()).grid(row=0, column=1)
        textWidget = Text(master, width=47, height=54, font=('Courier 10 bold'), bd=4, padx=5)
        popupText = Text(master, width=48, height=48, font=('Courier 12 bold'), bd=4, padx=5)
        textWidget.grid(row=1, column=0, columnspan=2)
        popupText.grid(row=1, column=2)

        # We want to iterate each element in the dictionary
        def iterSelection(mySelection):
            for key in mySelection:
                tag = key
                text = mySelection[key][0]
                textWidget.insert('end', text, (tag,))

                textWidget.tag_configure(tag)
                textWidget.tag_bind(tag, "<Enter>",
                                    lambda event, currentTag=tag, popup=mySelection[key][1]: popItUp(popup, 'red', currentTag))
                textWidget.tag_bind(tag, "<Leave>",
                                    lambda event, currentTag=tag: popItUp(showSelection(), 'white', currentTag))


            # function to delete and then insert the popuptext.
            def popItUp(text, color, currTag):
                popupText.delete("1.0", "end")
                popupText.insert("1.0", text, (currTag,))
                textWidget.tag_configure(currTag, background=color)


        def showSelection():
            currentSelection = clicked.get()
            textWidget.delete('1.0', 'end')
            if currentSelection == "Windows - NTFS VBR":
                iterSelection(hexInfo.windowsNTFSVBR)
                popupText.delete('1.0', 'end')
                popupText.insert("1.0", hexInfo.windowsNTFSVBRInfo)
                return hexInfo.windowsNTFSVBRInfo
            elif currentSelection == "Windows - NTFS MFT":
                iterSelection(hexInfo.windowsNTFSMFT)
                popupText.delete('1.0', 'end')
                popupText.insert("1.0", hexInfo.windowsNTFSMFTInfo)
                return hexInfo.windowsNTFSMFTInfo




root = Tk()
app = Main(root)
root.title("Poppetypop")
root.geometry("900x900+500+50")

root.mainloop()