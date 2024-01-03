import PySimpleGUI as sg
import os


class App:
    def __init__(self, theme='DarkGrey4'):
        sg.theme(theme)
        self.layout = self.create_input_column()
        self.window = sg.Window('ChordSheetWriter', self.layout, resizable=True)

    @staticmethod
    def create_input_column():
        column = [[sg.Button("RENDER"), sg.Button("SAVE")],
                  [sg.Multiline(size=(50, 25),
                                key="INPUT",
                                expand_x=True,
                                expand_y=True)]]
        return column

    def run(self):

        while True:
            event, values = self.window.read()

            match event:
                case sg.WINDOW_CLOSED:
                    break
                case "RENDER":
                    print(values["INPUT"])
                case "SAVE":
                    save_window = SaveWindow()
                    save_window.run()
        self.window.close()


class SaveWindow:
    def __init__(self):
        self.layout = [self.create_path_input(),
                       self.create_project_name_input(),
                       self.create_buttons()]
        self.window = sg.Window('Save Project', self.layout, resizable=True, return_keyboard_events=True)

    @staticmethod
    def create_path_input():
        return [sg.Text("Path to project destination"),
                sg.Input(key='PATH', enable_events=True, expand_x=True),
                sg.FolderBrowse()]

    @staticmethod
    def create_project_name_input():
        return [sg.Text("Enter project name"),
                sg.Input(key="PROJECTNAME", expand_x=True, enable_events=True)]

    @staticmethod
    def create_buttons():
        return [sg.Button("Save"), sg.Button("Cancel")]

    def save_project(self, path, name):
        print(os.path.normpath(os.path.join(path, name)))

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case sg.WINDOW_CLOSED | "Cancel":
                    break
                case "Save" | "\r":
                    self.save_project(values["PATH"], values["PROJECTNAME"])
                    break
        self.window.close()


if __name__ == '__main__':
    app = App()
    app.run()
