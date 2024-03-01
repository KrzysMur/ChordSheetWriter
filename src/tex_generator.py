import os
import tempfile
from src.music_sheet_elements import *
from src.config_provider import config

current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir_path = os.path.abspath(os.path.join(current_dir, "..", "resources"))


class TexGenerator:
    def __init__(self, metadata: dict, song: list[list]):
        self.tmp_file = tempfile.NamedTemporaryFile("a+t")
        self.metadata = metadata
        self.song = song

    def generate_temp_tex_file(self):
        self.write_preamble_to_file()
        self.begin_document()

        self.write_title_and_author()
        self.write_metadata()

        self.centering()
        self.begin_table()

        self.generate_table_content()

        self.end_table()
        self.end_document()
        self.tmp_file.seek(0)


    def begin_table(self):
        bars = self.get_max_bars_per_line()
        self.tmp_file.write(f"\\begin{{tabularx}}{{\\textwidth}}{{{self.get_column_types(bars)}}} \n")

    def generate_table_content(self):
        for line in self.song:
            self.write_table_line_to_file(line)

    def write_table_line_to_file(self, line):
        elements_tex_codes = []

        for element in line:
            if isinstance(element, BarChords):
                elements_tex_codes.append(element.get_tex_code(bar_width=self.get_bar_width()))

            else:
                elements_tex_codes.append(element.get_tex_code())

        if isinstance(line[0], TimeSignature):
            self.tmp_file.write(" & ".join(elements_tex_codes) + " \\\\ \n")
        else:
            self.tmp_file.write(" & " + " & ".join(elements_tex_codes) + " \\\\ \n")

    def end_table(self):
        self.tmp_file.write("\\end{tabularx}\n\n")

    def get_column_types(self, bars):
        bar_width = self.get_bar_width()
        return " L L " + " L ".join([f"p{{{bar_width}cm}}" for _ in range(bars)]) + "L"

    def get_bar_width(self):
        bars = self.get_max_bars_per_line()

        space = (float(config.get_page_width())
                 - float(config.get_left_margin())
                 - float(config.get_right_margin()))

        return (space - float(config.get_bar_line_width_coefficient()) *
                float(config.get_bar_line_width())*(bars+2)) / bars

    def get_max_bars_per_line(self):
        max_bars = 0
        for line in self.song:
            line_count = 0
            for element in line:
                if isinstance(element, BarChords):
                    line_count += 1
            if line_count > max_bars:
                max_bars = line_count
        return max_bars

    def write_preamble_to_file(self):
        with open(os.path.join(resources_dir_path, "preamble.txt")) as file:
            lines = file.readlines()
        for line in lines:
            self.tmp_file.write(line)

        self.tmp_file.write(f"\\renewcommand{{\\arraystretch}}{{{config.get_line_spacing()}}}\n")

        self.tmp_file.write(f"\\geometry{{top={config.get_top_margin()}cm, "
                            f"bottom={config.get_bottom_margin()}cm, "
                            f"left={config.get_left_margin()}cm, "
                            f"right={config.get_right_margin()}cm}}\n\n\n")

    def write_title_and_author(self):
        self.tmp_file.write(
            f"\\LARGE {self.metadata['title']} \\hfill  {self.metadata['author']} \\newline\\tiny\\newline\\small \n")

    def write_metadata(self):
        if self.metadata.get("key") != "N/A":
            self.tmp_file.write(f"\\hfill Key: {self.metadata.get('key')} \\hfill")

        if self.metadata.get("chords") != "N/A":
            self.tmp_file.write(
                f"\\hfill Chords: {'\\hspace{0.2cm} '.join(['\\writechord{' + chord + '}' 
                                                            for chord in self.metadata.get('chords')])} \\hfill")

        if self.metadata.get("capo") != "N/A":
            self.tmp_file.write("\\hfill " + self.parse_capo() + " \\hfill ")

        if self.metadata.get("tempo") != "N/A":
            self.tmp_file.write(" \\hfill Tempo: " + self.metadata.get("tempo"))

        self.tmp_file.write("\\newline\\rule{\\linewidth}{0.3pt}\\newline \\large \\bfseries \n\n")

    def begin_document(self):
        self.tmp_file.write("\\begin{document} \n")

    def end_document(self):
        self.tmp_file.write("\\end{document} \n")

    def parse_capo(self):
        match self.metadata.get("capo", 0):
            case "1":
                return "\\hfill Capo: 1\\textsuperscript{st} fret \\hfill"
            case "2":
                return "\\hfill Capo: 2\\textsuperscript{nd} fret \\hfill"
            case "3":
                return "\\hfill Capo: 1\\textsuperscript{rd} fret \\hfill"
            case num:
                return f"\\hfill Capo: {num}\\textsuperscript{{th}} fret \\hfill"

    def centering(self):
        self.tmp_file.write("\n \\centering \n\n")
