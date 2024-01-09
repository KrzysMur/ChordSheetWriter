import PySimpleGUI as sg
import os
from saving import SaveWindow, save_project
from opening import OpenProjectWindow
from parser_and_tex_generator import ParserAndTexGenerator
from input_parser import InputParser


class App:
    def __init__(self, theme='DarkGrey4'):
        sg.theme(theme)
        self.layout = self.create_input_column()
        self.window = sg.Window('ChordSheetWriter', self.layout, resizable=True)
        self.project_path = None
        self.project_name = None

    @staticmethod
    def create_input_column():
        column = [[sg.Button("RENDER"), sg.Button("SAVE"), sg.Button("OPEN")],
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
                    if self.project_path is not None:
                        save_project(self.project_path, self.project_name, values["INPUT"])
                    else:
                        save_window = SaveWindow(values["INPUT"])
                        self.project_path, self.project_name = save_window.run()
                case "OPEN":
                    open_window = OpenProjectWindow()
                    text_from_file = open_window.run()
                    print(text_from_file)

        self.window.close()


if __name__ == '__main__':
    with open("../example_inputs/project.chordsheet") as file:
        input_content = [line.strip() for line in file.readlines() if line != "\n"]
        parser = InputParser(input_content)
        metadata, metadata_ending_index = parser.get_metadata(return_metadate_ending_index=True)
        parser.parse_song(metadata_ending_index)
        with open("../tutorial.tex", "w") as tex_file:
            pass

