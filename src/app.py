import PySimpleGUI as sg
import os
from tex_generator import TexGenerator
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
                    pass
                case "OPEN":
                    pass

        self.window.close()


if __name__ == '__main__':
    with open("../example_inputs/project.chordsheet") as file:
        input_content = [line.strip() for line in file.readlines() if line != "\n"]

    parser = InputParser(input_content)
    metadata, metadata_ending_index = parser.get_metadata(return_metadate_ending_index=True)
    parsed_song = parser.parse_song(metadata_ending_index)

    tex_generator = TexGenerator(metadata, parsed_song)
    tex_generator.generate_temp_tex_file()

    print(tex_generator.song)

    with open("../tutorial.tex", "w") as tex_file:
        tex_file.write(tex_generator.tmp_file.read())

