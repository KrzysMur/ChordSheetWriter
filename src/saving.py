import PySimpleGUI as sg
import os


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

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case sg.WINDOW_CLOSED | "Cancel":
                    self.window.close()
                    return None, None
                case "Save" | "\r":
                    save_project(values["PATH"], values["PROJECTNAME"], self.input_content)
                    self.window.close()
                    return values["PATH"], values["PROJECTNAME"]



def save_project(path, name, content):
    if not os.path.exists(os.path.join(path, name)):
        os.makedirs(os.path.join(path, name))

    with open(os.path.normpath(os.path.join(path, name, name + ".txt")), "w") as file:
        file.write(content)
    with open(os.path.normpath(os.path.join(path, name, name + ".tex")), "w") as file:
        file.write(content)
