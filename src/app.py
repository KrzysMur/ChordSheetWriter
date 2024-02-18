import os
import sys
from tex_generator import TexGenerator
from input_parser import InputParser
from config_provider import config
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


def create_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    return separator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChordSheetWriter")
        self.setMinimumSize(300, 350)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.layout)

        self.tool_bar = QHBoxLayout()
        self.tool_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_size = int(config.get("gui", "toolbar_button_size"))

        self.save_button = QPushButton(QIcon("../resources/icons/save.png"), "", self)
        self.save_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.save_button)

        self.start_button = QPushButton(QIcon("../resources/icons/start.png"), "", self)
        self.start_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.start_button)

        self.tool_bar.addWidget(create_separator())

        self.undo_button = QPushButton(QIcon("../resources/icons/undo.png"), "", self)
        self.undo_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.undo_button)

        self.redo_button = QPushButton(QIcon("../resources/icons/redo.png"), "", self)
        self.redo_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.redo_button)

        self.tool_bar.addWidget(create_separator())

        self.settings_button = QPushButton(QIcon("../resources/icons/settings.png"), "", self)
        self.settings_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.settings_button)

        self.layout.addLayout(self.tool_bar)

        self.text_input = QTextEdit()
        self.layout.addWidget(self.text_input)

        self.show()



if __name__ == '__main__':

    project_name = "project1"

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())

    with open(f"../example_inputs/{project_name}.chordsheet") as file:
        input_content = [line.strip() for line in file.readlines() if line != "\n"]

    parser = InputParser(input_content)
    metadata, parsed_song = parser.parse()

    tex_generator = TexGenerator(metadata, parsed_song)
    tex_generator.generate_temp_tex_file()

    with open(f"../{project_name}.tex", "w") as tex_file:
        tex_file.write(tex_generator.tmp_file.read())

    os.chdir("../")
    os.system(f"pdflatex {project_name}.tex")
    os.system(f"del {project_name}.aux")
    os.system(f"del {project_name}.tex")
    os.system(f"del {project_name}.log")


