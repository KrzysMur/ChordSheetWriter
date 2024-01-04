import PySimpleGUI as sg
import os


class App:
    def __init__(self, theme='DarkGrey4'):
        sg.theme(theme)
        self.layout = self.create_input_column()
        self.window = sg.Window('ChordSheetWriter', self.layout, resizable=True)
        self.project_path = None
        self.project_name = None

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
                    if self.project_path is not None and os.path.exists(self.project_path):
                        # TODO: saving after location change raises filenotfound error
                        # Project has been saved before and location didn`t change
                        self.save(values["INPUT"])
                    else:
                        # Saving project for the first time or after location change
                        save_window = SaveWindow(values["INPUT"])
                        self.project_path, self.project_name = save_window.run()
        self.window.close()

    def save(self, content):
        with open(os.path.join(self.project_path, self.project_name, self.project_name + ".txt"), "w") as file:
            file.write(content)
        with open(os.path.join(self.project_path, self.project_name, self.project_name + ".tex"), "w") as file:
            file.write(content)


class SaveWindow:
    def __init__(self, input_content):
        self.input_content = input_content
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
        try:
            os.makedirs(os.path.normpath(os.path.join(path, name)))
        except FileExistsError:
            sg.popup("Project directory already exists", title="ERROR")
        else:
            with open(os.path.normpath(os.path.join(path, name, name + ".txt")), "w") as file:
                file.write(self.input_content)
            with open(os.path.normpath(os.path.join(path, name, name + ".tex")), "w") as file:
                file.write(self.input_content)

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case sg.WINDOW_CLOSED | "Cancel":
                    break
                case "Save" | "\r":
                    self.save_project(values["PATH"], values["PROJECTNAME"])
                    self.window.close()
                    return values["PATH"], values["PROJECTNAME"]
        self.window.close()


if __name__ == '__main__':
    app = App()
    app.run()
