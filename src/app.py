import logging
import os
import sys
import subprocess
import time
import logging as log

from tex_generator import TexGenerator
from input_parser import InputParser
from syntax_validator import validate_syntax
from config_provider import config

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt


def show_error_message(text="ERROR"):
    msg = QMessageBox()
    msg.setWindowTitle("ERROR")
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_name = "unnamedproject"
        self.path_to_project = None
        self.project_directory = os.getcwd()

        self.setWindowTitle("ChordSheetWriter")
        self.setMinimumSize(config.get_main_window_width(), config.get_main_window_height())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.layout)

        self.text_input = QTextEdit()

        # Toolbar section

        self.tool_bar = QHBoxLayout()
        self.tool_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_size = config.get_toolbar_button_size()

        self.save_button = QPushButton(QIcon("../resources/icons/save.png"), "", self)
        self.save_button.clicked.connect(self.save_project)
        self.save_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.save_button)

        self.load_button = QPushButton(QIcon("../resources/icons/load.png"), "", self)
        self.load_button.setFixedSize(button_size, button_size)
        self.load_button.clicked.connect(self.open_project)
        self.tool_bar.addWidget(self.load_button)

        self.start_button = QPushButton(QIcon("../resources/icons/start.png"), "", self)
        self.start_button.clicked.connect(self.generate_pdf)
        self.start_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.start_button)

        self.tool_bar.addSpacing(config.get_toolbar_group_spacing())

        self.undo_button = QPushButton(QIcon("../resources/icons/undo.png"), "", self)
        self.undo_button.clicked.connect(self.text_input.undo)
        self.tool_bar.addWidget(self.undo_button)

        self.redo_button = QPushButton(QIcon("../resources/icons/redo.png"), "", self)
        self.redo_button.clicked.connect(self.text_input.redo)
        self.redo_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.redo_button)

        self.tool_bar.addSpacing(config.get_toolbar_group_spacing())

        self.settings_button = QPushButton(QIcon("../resources/icons/settings.png"), "", self)
        self.settings_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.settings_button)

        self.tool_bar.addStretch()

        self.status_label = QLabel("Welcome to ChordSheetWriter!")
        self.tool_bar.addWidget(self.status_label)

        # Init Layout

        self.layout.addLayout(self.tool_bar)

        self.layout.addWidget(self.text_input)

        self.show()

        # Initialize and handle keyboard shortcuts
        save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        save_shortcut.activated.connect(self.save_project)

        generate_pdf_shortcut = QShortcut(QKeySequence(Qt.Key.Key_R | Qt.KeyboardModifier.ControlModifier), self)
        generate_pdf_shortcut.activated.connect(self.generate_pdf)

    def generate_pdf(self):

        self.save_project()
        if not self.path_to_project:
            return

        source = self.text_input.toPlainText().splitlines()

        input_content = [line for line in source if line]
        log.info("Read input")

        syntax_valid = validate_syntax(input_content)

        if syntax_valid:
            log.info("Syntax valid")
        else:
            show_error_message("Invalid syntax. Cannot continue. \n See console_output.log file for further information")
            return

        parser = InputParser(input_content)
        log.info("Parser initialized")

        metadata, parsed_song = parser.parse()
        log.info("Input parsed")

        tex_generator = TexGenerator(metadata, parsed_song)
        log.info("Tex generator initialilzed")

        tex_generator.generate_temp_tex_file()
        log.info("Temporary file generated")

        with open(f"{self.project_name}.tex", "w") as tex_file:
            tex_file.write(tex_generator.tmp_file.read())
        log.info("Tex file generated")

        err_code = os.system(f"pdflatex -interaction=nonstopmode {self.project_name}.tex")
        if err_code != 0:
            show_error_message("Unable to compile")
            log.error("Unable to compile")
        else:
            log.debug("Compiled successfully")

        os.system(f"del {self.project_name}.aux")
        os.system(f"del {self.project_name}.tex")
        os.system(f"del {self.project_name}.log")

    def save_project(self):
        if not self.path_to_project:
            directory_dialog = SaveProjectWindow()
            directory_dialog.exec()
            self.path_to_project = directory_dialog.path
            self.project_name = directory_dialog.project_name
        if self.path_to_project is not None:
            with open(self.path_to_project, "w") as file:
                file.write(self.text_input.toPlainText())

    def open_project(self):
        dialog = OpenProjectWindow()
        dialog.exec()
        path_to_chord_sheet = os.path.normpath(dialog.path)

        if path_to_chord_sheet:
            self.project_name = os.path.basename(path_to_chord_sheet).split(".")[0]

            self.path_to_project = path_to_chord_sheet
            self.project_directory = os.path.dirname(path_to_chord_sheet)

            os.chdir(self.project_directory)

            with open(path_to_chord_sheet, "r") as file:
                self.text_input.setText(file.read())


class SaveProjectWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.path = None
        self.project_name = None
        self.setWindowTitle("Save project as...")
        self.setFixedSize(config.get_save_window_width(), config.get_save_window_height())
        self.layout = QVBoxLayout()

        # Init directory input section
        self.location_input_layout = QHBoxLayout()

        self.location_browser = QFileDialog(self)
        self.location_browser.setFileMode(QFileDialog.FileMode.Directory)
        self.location_input_layout.addWidget(self.location_browser)

        select_button = QPushButton("Browse")
        select_button.clicked.connect(self.select_directory)
        self.location_input_layout.addWidget(select_button)

        self.location_input = QLineEdit()
        self.location_input_layout.addWidget(self.location_input)

        # Save and Cancel Buttons init section
        self.buttons_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.get_project_path)
        self.buttons_layout.addWidget(self.save_button)

        # Layout init
        self.layout.addWidget(QLabel("Select directory for your chord sheet:"))
        self.layout.addLayout(self.location_input_layout)

        self.layout.addWidget(QLabel("Name your chord sheet:"))
        self.project_name_input = QLineEdit()
        self.layout.addWidget(self.project_name_input)

        info_text = QLabel("Note that PDF and log files will be generated in the project directory.")
        info_text.setStyleSheet("font-size: 7pt;")
        self.layout.addWidget(info_text)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def get_project_path(self):
        directory = self.location_input.text().strip()
        self.project_name = self.project_name_input.text().strip()
        if directory and self.project_name:
            try:
                self.path = os.path.join(directory, self.project_name + ".chordsheet")
                self.path = os.path.normpath(self.path)
                log.debug("Selected path:  " + self.path)
            except ValueError:
                log.warning("Invalid path characters")
        else:
            log.warning("Invalid location and project name")
            show_error_message("Invalid location and project name")
            self.path = None
        self.close()

    def select_directory(self):
        selected_directory = self.location_browser.getExistingDirectory(self, "Select Directory", "")
        if selected_directory:
            self.location_input.setText(os.path.normpath(selected_directory))


class OpenProjectWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(config.get_open_window_width(), config.get_open_window_height())
        self.setWindowTitle("Open project")

        self.path = None

        # Input layout section
        input_layout = QHBoxLayout()

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_file)
        input_layout.addWidget(browse_button)

        self.dir_input = QLineEdit()
        input_layout.addWidget(self.dir_input)

        # Buttons layout section
        buttons_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_button)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.get_file_location_to_open)
        buttons_layout.addWidget(open_button)

        # Init layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(input_layout)
        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)

    def get_file_location_to_open(self):
        self.path = self.dir_input.text().strip()

        if not os.path.exists(self.path) or not os.path.isfile(self.path):
            self.path = None
        self.close()

    def select_file(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Chord Sheet Files (*.chordsheet *.txt)")
        if selected_file is not None:
            self.dir_input.setText(selected_file)


if __name__ == '__main__':

    logging.basicConfig(
        level=config.get_logging_level(),
        format="%(levelname)s %(message)s",
    #    filename="../console_output.log"
    )

    log.info(f"Welcome to ChordSheetWriter log file! Entered proccess at {time.time()}")

    app = QApplication(sys.argv)
    log.debug("Initialized QApplication")

    main_window = MainWindow()
    log.debug("Initialized MainWindow")

    sys.exit(app.exec())

