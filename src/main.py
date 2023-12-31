from tkinter import *
from tkinter import scrolledtext


class App(Tk):
    def __init__(self):
        super().__init__()

        self.configure_window()
        self.display_widgets()


    def configure_window(self):
        self.title("ChordSheetWriter")
        self.geometry("600x400")

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)

    def display_widgets(self):
        render_button = Button(self, text="RENDER", command=self.render_input)
        render_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        self.text_input = scrolledtext.ScrolledText(self, wrap=WORD)
        self.text_input.grid(column=0, row=1, padx=5, pady=15, sticky=NSEW)

        self.output_box = Label(self, text="", anchor=NW, justify="left")
        self.output_box.grid(column=1, row=0, rowspan=2, padx=15, pady=15, sticky=NSEW)
        self.output_box.configure(bg="white")

    def render_input(self):
        self.output_box.configure(text=self.text_input.get("1.0", END))


if __name__ == "__main__":
    app = App()
    app.mainloop()

