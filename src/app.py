import PySimpleGUI as sg

class App:
    def __init__(self, theme='DarkGrey4'):
        sg.theme(theme)
        self.create_input_column()
        self.create_output_column()
        self.layout = [
            [self.input_column, self.output_column]
        ]

        self.window = sg.Window('ChordSheetWriter', self.layout)

    def create_input_column(self):
        self.input_column = sg.Column([
            [sg.Button("RENDER"), sg.Button("SAVE")],
            [sg.Multiline(size=(50, 25),
                          key="INPUT")]
        ], element_justification="left")

    def create_output_column(self):
        self.output_column = sg.Column([
            [sg.Image(filename="C:\\Users\\murek\\Desktop\\example.png",
                      key="OUTPUT",
                      size=(200, 200),
                      auto_size_image=True)]
        ], element_justification="right")

    def run(self):
        while True:
            event, values = self.window.read()

            match event:
                case sg.WINDOW_CLOSED:
                    break
                case "RENDER":
                    print("render")
                case "SAVE":
                    print("save")


        self.window.close()



app = App()
app.run()
