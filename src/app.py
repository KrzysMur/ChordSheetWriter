import logging
import os
import sys
import subprocess
from tex_generator import TexGenerator
from input_parser import InputParser
from syntax_validator import validate_syntax
from config_provider import config
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import logging as log


def create_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    return separator


def show_error_message(text="ERROR"):
    msg = QMessageBox()
    msg.setWindowTitle("ERROR")
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def validate_tex_syntax(tex_file_path):
    command = "lacheck " + tex_file_path
    result = subprocess.getoutput(command)
    return result


class MainWindow(QMainWindow):
    def __init__(self):
        # super().__init__()

        self.project_name = "unnamedproject"

        return

        self.setWindowTitle("ChordSheetWriter")
        self.setMinimumSize(int(config.get("gui", "main_window_width")), int(config.get("gui", "main_window_height")))

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

        self.load_button = QPushButton(QIcon("../resources/icons/load.png"), "", self)
        self.load_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.load_button)

        self.start_button = QPushButton(QIcon("../resources/icons/start.png"), "", self, clicked=self.generate_pdf)
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

    def generate_pdf(self):

        with open("../example_inputs/project.chordsheet") as file:
            source = [line.strip() for line in file.readlines()]
        # source = self.text_input.toPlainText().splitlines()

        input_content = [line for line in source if line]
        log.info("Read input")

        syntax_valid = validate_syntax(input_content)

        if syntax_valid:
            log.info("Syntax valid")
        else:
            log.error("Syntax invalid")

        parser = InputParser(input_content)
        log.info("Parser initialized")

        metadata, parsed_song = parser.parse()
        log.info("Input parsed")

        tex_generator = TexGenerator(metadata, parsed_song)
        log.info("Tex generator initialilzed")

        tex_generator.generate_temp_tex_file()
        log.info("Temporary file generated")

        os.chdir("../")

        with open(f"{self.project_name}.tex", "w") as tex_file:
            tex_file.write(tex_generator.tmp_file.read())
        log.info("Tex file generated")

        err_code = os.system(f"pdflatex -interaction=nonstopmode {self.project_name}.tex")
        if err_code != 0:
            show_error_message("Unable to compile")

        os.system(f"del {self.project_name}.aux")
    #    os.system(f"del {self.project_name}.tex")
        os.system(f"del {self.project_name}.log")

        os.chdir("src/")


if __name__ == '__main__':

    logging.basicConfig(
        level=log.INFO,
        format="%(levelname)s %(message)s",
        # filename="csw.log"
    )
    app = QApplication(sys.argv)
    main_window = MainWindow().generate_pdf()
    # app.exec()
