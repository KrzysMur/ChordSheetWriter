import os
import sys
import subprocess
import logging

from src.tex_generator import TexGenerator
from src.input_parser import InputParser
from src.syntax_validator import validate_syntax
from src.config_provider import config, icons_dir, config_file_path

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtCore import Qt

logging.debug(f"Icons folder path: {icons_dir}")


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

        self.project_name = None
        self.project_file_path = None
        self.project_directory = None

        self.setWindowTitle("ChordSheetWriter")
        self.setWindowIcon(QIcon(os.path.join(icons_dir, "logo.ico")))
        self.setMinimumSize(config.get_main_window_width(), config.get_main_window_height())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.layout)

        self.text_input = QTextEdit()
        self.text_input.textChanged.connect(self.input_text_changed)

        # Toolbar section

        self.tool_bar = QHBoxLayout()
        self.tool_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_size = config.get_toolbar_button_size()

        self.save_button = QPushButton(QIcon(os.path.join(icons_dir, "save.png")), "", self)
        self.save_button.clicked.connect(self.save_project)
        self.save_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.save_button)

        self.load_button = QPushButton(QIcon(os.path.join(icons_dir, "load.png")), "", self)
        self.load_button.setFixedSize(button_size, button_size)
        self.load_button.clicked.connect(self.open_project)
        self.tool_bar.addWidget(self.load_button)

        self.start_button = QPushButton(QIcon(os.path.join(icons_dir, "start.png")), "", self)
        self.start_button.clicked.connect(self.generate_pdf)
        self.start_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.start_button)

        self.tool_bar.addSpacing(config.get_toolbar_group_spacing())

        self.undo_button = QPushButton(QIcon(os.path.join(icons_dir, "undo.png")), "", self)
        self.undo_button.clicked.connect(self.text_input.undo)
        self.tool_bar.addWidget(self.undo_button)

        self.redo_button = QPushButton(QIcon(os.path.join(icons_dir, "redo.png")), "", self)
        self.redo_button.clicked.connect(self.text_input.redo)
        self.redo_button.setFixedSize(button_size, button_size)
        self.tool_bar.addWidget(self.redo_button)

        self.tool_bar.addSpacing(config.get_toolbar_group_spacing())

        self.settings_button = QPushButton(QIcon(os.path.join(icons_dir, "settings.png")), "", self)
        self.settings_button.clicked.connect(self.settings_dialog)
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
        if not self.project_file_path:
            return

        source = self.text_input.toPlainText().splitlines()

        input_content = [line for line in source if line]
        logging.info("Read input")

        syntax_valid = validate_syntax(input_content)

        if syntax_valid:
            logging.info("Syntax valid")
        else:
            show_error_message("Invalid syntax. Cannot continue. \n See console_output.log file for further information")
            return

        parser = InputParser(input_content)
        logging.info("Parser initialized")

        metadata, parsed_song = parser.parse()
        logging.info("Input parsed")

        tex_generator = TexGenerator(metadata, parsed_song)
        logging.info("Tex generator initialilzed")

        tex_generator.generate_temp_tex_file()
        logging.info("Temporary file generated")

        tex_file_path = os.path.join(self.project_directory, f"{self.project_name}.tex")
        logging.info(f"Tex file path: {tex_file_path}")

        with open(tex_file_path, "w") as tex_file:
            tex_file.write(tex_generator.tmp_file.read())
        logging.info("Tex file generated")

        self.status_label.setText("Generating PDF...")
        command = f"pdflatex -interaction=nonstopmode -output-directory={self.project_directory} {tex_file_path}"
        err_code = os.system(command)

        if err_code != 0:
            show_error_message("Unable to compile")
            logging.error("Unable to compile. See texput.log for LaTeX debugging info")
        else:
            project_path_no_extention = os.path.join(self.project_directory, self.project_name)
            os.system(f"del {project_path_no_extention}.tex")
            os.system(f"del {project_path_no_extention}.aux")
            os.system(f"del {project_path_no_extention}.log")

            if os.path.exists(project_path_no_extention+".pdf"):
                logging.info("Compiled successfully")
                self.status_label.setText("PDF compiled successfully")
            else:
                logging.error("Pdf did not compile correctly")
                self.status_label.setText("Something went wrong while compiling PDF")

    def save_project(self):

        if not self.project_file_path:

            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Chord Sheet (*.chordsheet)")
            file_path = os.path.normpath(file_path)
            if file_path == ".":
                return

            self.project_file_path = file_path
            logging.debug(f"Saved project file path: {self.project_file_path}")

            self.project_name = os.path.basename(file_path).split(".")[0]
            logging.debug(f"Saved project name: {self.project_name}")

            self.project_directory = os.path.dirname(self.project_file_path)
            logging.debug(f"Saved project directory: {self.project_directory}")

        if self.project_file_path and self.project_name:

            with open(self.project_file_path, "w") as file:
                file.write(self.text_input.toPlainText())

            logging.debug("Input content saved to file")

        self.status_label.setText("Project has been saved")

    def open_project(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Chord Sheet Files (*.chordsheet)")
        logging.debug(f"Selected path to open: {selected_file}")

        if selected_file:
            logging.debug("Selected path is valid.")

            selected_file = os.path.normpath(selected_file)

            self.project_name = os.path.basename(selected_file).split(".")[0]
            logging.debug(f"Selected project name: {self.project_name}")

            self.project_file_path = selected_file
            self.project_directory = os.path.dirname(selected_file)

            logging.debug(f"Path to project: {self.project_file_path} Project directory: {self.project_directory}")

            with open(selected_file, "r") as file:
                chord_sheet_input = file.read()

            logging.debug("Read file content")
            self.text_input.setText(chord_sheet_input)
            logging.info("File content opened in editor")
            self.status_label.setText(f"{self.project_name} has been opened")
        else:
            logging.debug("Empty path. Cannot open")

    def input_text_changed(self):
        self.status_label.setText("Unsaved changes")

    def settings_dialog(self):
        settings_window = SettingsWindow()
        settings_window.exec()
        config_to_value = settings_window.config_to_value
        if config_to_value is None:
            return



class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.config_to_value = None
        logging.debug("Initializing SettingsWindow")

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(os.path.join(icons_dir, "logo.ico")))

        layout = QVBoxLayout()

        # Left margin

        left_margin_layout = QHBoxLayout()
        left_margin_label = QLabel("Left margin: ")
        left_margin_label.setFixedWidth(150)
        left_margin_slider = QSlider(Qt.Orientation.Horizontal)
        left_margin_slider.setMinimum(0)
        left_margin_slider.setMaximum(50)
        left_margin_slider.setValue(10)
        left_margin_slider.setTickInterval(1)
        left_margin_slider.valueChanged.connect(self.set_left_margin_value)
        self.left_margin_value = QLabel(str(left_margin_slider.value()/10))
        left_margin_layout.addWidget(left_margin_label)
        left_margin_layout.addWidget(left_margin_slider)
        left_margin_layout.addWidget(self.left_margin_value)
        layout.addLayout(left_margin_layout)

        # Right margin

        right_margin_layout = QHBoxLayout()
        right_margin_label = QLabel("Right margin: ")
        right_margin_label.setFixedWidth(150)
        right_margin_slider = QSlider(Qt.Orientation.Horizontal)
        right_margin_slider.setMinimum(0)
        right_margin_slider.setMaximum(50)
        right_margin_slider.setValue(10)
        right_margin_slider.setTickInterval(1)
        right_margin_slider.valueChanged.connect(self.set_right_margin_value)
        self.right_margin_value = QLabel(str(right_margin_slider.value() / 10))
        right_margin_layout.addWidget(right_margin_label)
        right_margin_layout.addWidget(right_margin_slider)
        right_margin_layout.addWidget(self.right_margin_value)
        layout.addLayout(right_margin_layout)

        # Top margin

        top_margin_layout = QHBoxLayout()
        top_margin_label = QLabel("Top margin: ")
        top_margin_label.setFixedWidth(150)
        top_margin_slider = QSlider(Qt.Orientation.Horizontal)
        top_margin_slider.setMinimum(0)
        top_margin_slider.setMaximum(50)
        top_margin_slider.setValue(7)
        top_margin_slider.setTickInterval(1)
        top_margin_slider.valueChanged.connect(self.set_top_margin_value)
        self.top_margin_value = QLabel(str(top_margin_slider.value() / 10))
        top_margin_layout.addWidget(top_margin_label)
        top_margin_layout.addWidget(top_margin_slider)
        top_margin_layout.addWidget(self.top_margin_value)
        layout.addLayout(top_margin_layout)

        # Bottom margin

        bottom_margin_layout = QHBoxLayout()
        bottom_margin_label = QLabel("Bottom margin: ")
        bottom_margin_label.setFixedWidth(150)
        bottom_margin_slider = QSlider(Qt.Orientation.Horizontal)
        bottom_margin_slider.setMinimum(0)
        bottom_margin_slider.setMaximum(50)
        bottom_margin_slider.setValue(5)
        bottom_margin_slider.setTickInterval(1)
        bottom_margin_slider.valueChanged.connect(self.set_bottom_margin_value)
        self.bottom_margin_value = QLabel(str(bottom_margin_slider.value() / 10))
        bottom_margin_layout.addWidget(bottom_margin_label)
        bottom_margin_layout.addWidget(bottom_margin_slider)
        bottom_margin_layout.addWidget(self.bottom_margin_value)
        layout.addLayout(bottom_margin_layout)

        # Line spacing

        line_spacing_layout = QHBoxLayout()
        line_spacing_label = QLabel("Line spacing: ")
        line_spacing_label.setFixedWidth(150)
        line_spacing_slider = QSlider(Qt.Orientation.Horizontal)
        line_spacing_slider.setMinimum(5)
        line_spacing_slider.setMaximum(70)
        line_spacing_slider.setValue(int(config.get_line_spacing())*10)
        line_spacing_slider.setTickInterval(1)
        line_spacing_slider.valueChanged.connect(self.set_line_spacing_value)
        self.line_spacing_value = QLabel(str(line_spacing_slider.value() / 10))
        line_spacing_layout.addWidget(line_spacing_label)
        line_spacing_layout.addWidget(line_spacing_slider)
        line_spacing_layout.addWidget(self.line_spacing_value)
        layout.addLayout(line_spacing_layout)

        # Buttons

        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.ok_button_pressed)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ok_button_pressed(self):
        self.config_to_value = {
            "left_margin": self.left_margin_value.text(),
            "right_margin": self.right_margin_value.text(),
            "top_margin": self.top_margin_value.text(),
            "bottom_margin": self.bottom_margin_value.text(),
            "line_spacing": self.left_margin_value.text()
        }
        self.close()

    def set_left_margin_value(self, v):
        self.left_margin_value.setText(str(v/10))

    def set_right_margin_value(self, v):
        self.right_margin_value.setText(str(v/10))

    def set_top_margin_value(self, v):
        self.top_margin_value.setText(str(v/10))

    def set_bottom_margin_value(self, v):
        self.bottom_margin_value.setText(str(v/10))

    def set_line_spacing_value(self, v):
        self.line_spacing_value.setText(str(v/10))


def main():
    if os.system("pdflatex --version") != 0:
        show_error_message("To use this program you have to install MikTex.")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(message)s",
        # filename="../console_output.log"
    )

    logging.info(f"Welcome to ChordSheetWriter!")

    app = QApplication(sys.argv)
    logging.debug("Initialized QApplication")

    main_window = MainWindow()
    logging.debug("Initialized MainWindow")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
