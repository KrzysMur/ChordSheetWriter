import PySimpleGUI as sg
import os


class OpenProjectWindow:
    def __init__(self):
        self.layout = [self.create_path_input(), self.create_buttons()]
        self.window = sg.Window('Open Project', self.layout, resizable=True, return_keyboard_events=True)

    @staticmethod
    def create_path_input():
        return [sg.Text("Path to project folder"),
                sg.Input(key='PATH', enable_events=True, expand_x=True),
                sg.FolderBrowse()]

    @staticmethod
    def create_buttons():
        return [sg.Button("Open"),
                sg.Button("Cancel")]

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case sg.WINDOW_CLOSED | "Cancel":
                    self.window.close()
                    return
                case "Open":
                    with open(values["PATH"]) as file:
                        self.window.close()
                        return file.read()
