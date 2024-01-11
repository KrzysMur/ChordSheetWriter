import tempfile


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
        self.end_document()
        self.tmp_file.seek(0)

    def write_preamble_to_file(self):
        with open("../resources/preamble.txt") as file:
            lines = file.readlines()
        for line in lines:
            self.tmp_file.write(line)

    def write_title_and_author(self):
        self.tmp_file.write(
            f"\\LARGE {self.metadata['title']} \\hfill  {self.metadata['author']} \\newline\\tiny\\newline\\small \n")

    def write_metadata(self):
        if self.metadata.get("key") != "N/A":
            self.tmp_file.write(f"\\hfill Key: {self.metadata.get('key')} \\hfill")

        if self.metadata.get("chords") != "N/A":
            self.tmp_file.write(
                f"\\hfill Chords: {'\\hspace{0.2cm} '.join(['\\writechord{' + chord.replace("#", "\\#") + '}' 
                                                            for chord in self.metadata.get('chords')])} \\hfill")

        if self.metadata.get("capo") != "N/A":
            self.tmp_file.write("\\hfill " + self.parse_capo() + " \\hfill ")

        if self.metadata.get("tempo") != "N/A":
            self.tmp_file.write(" \\hfill Tempo: " + self.metadata.get("tempo"))

        self.tmp_file.write("\\newline\\rule{\\linewidth}{0.3pt}\\newline \n\n")

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
