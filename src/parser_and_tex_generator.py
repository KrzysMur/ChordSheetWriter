import tempfile


def read_preamble():
    with open("../resources/preamble.txt") as preamble:
        return [line.strip() for line in preamble.readlines()]


def parse_barlines_and_chords(line):
    elements = []
    bar = ""
    for char in line:
        if char in ["[", "]", "|"] and bar:
            elements.append(bar)
            bar = ""
        match char:
            case "[":
                elements.append("\\leftrepeat")
            case "]":
                elements.append("\\rightrepeat")
            case "|":
                elements.append("\\normalbar")
            case "#":
                bar += "\\" + char
            case _:
                bar += char
    return elements


class ParserAndTexGenerator:
    def __init__(self, input_text: list[str]):
        self.input_text = input_text
        self.tmp_file = tempfile.NamedTemporaryFile("a+t")
        self.metadata = self.get_metadata()
        self.preamble = read_preamble()
        self.write_preamble_and_header_to_file()
        self.write_metadata_to_file()
        self.generate_table()
        self.tmp_file.write("\n\\end{document}")

    def get_metadata(self):
        metadata = {}
        while self.input_text[0] != "":
            line = self.input_text.pop(0).split("=")
            metadata.update({line[0].strip(): line[1].strip()})

        if "capo" in metadata.keys():
            metadata["capo"] = int(metadata.get("capo"))
        if "chords" in metadata.keys():
            metadata["chords"] = [chord.strip() for chord in metadata.get("chords").split(",")]
        self.input_text.pop(0)
        return metadata

    def write_preamble_and_header_to_file(self):
        for line in self.preamble:
            self.tmp_file.write(line+"\n")

    def write_metadata_to_file(self):
        self.tmp_file.write(f"\\LARGE {self.metadata['title']} \\hfill  {self.metadata['author']} \\newline\\tiny\\newline \n")

        chords = " ".join(["\\writechord{" + chord + "} \\hspace{0.4cm}"
                          for chord in self.metadata.get("chords", 0)])

        self.tmp_file.write(f"\\small Key: {self.metadata.get("key", 0)} \\hfill Chords: {chords} \\hfill")
        if "capo" in self.metadata:
            self.tmp_file.write(self.parse_capo())
        if "tempo" in self.metadata:
            self.tmp_file.write(f" \\hfill Tempo: {self.metadata.get('tempo')}")
        self.tmp_file.write("\\newline\\rule{\\linewidth}{0.3pt}\\newline")

    def parse_capo(self):
        match self.metadata.get("capo", 0):
            case 1:
                return " Capo: 1\\textsuperscript{st} fret"
            case 2:
                return " Capo: 2\\textsuperscript{nd} fret"
            case 3:
                return " Capo: 1\\textsuperscript{rd} fret"
            case num:
                return f" Capo: {num}\\textsuperscript{{th}} fret"

    def generate_table(self):
        self.tmp_file.write("\\newline \\centering \\large \\begin{tabular}{c c c c c c c c c} \n")
        for line in self.input_text:
            line = line.strip()
            elements = []
            match line[0]:
                case "(":
                    continue
                    time_signature = list(int(n) for n in line[1:line.find(")")].split("/"))
                    elements = [f"\\frac{{{time_signature[0]}}}{{{time_signature[1]}}}"]
                case "[" | "|":
                    elements = parse_barlines_and_chords(line)
                    for i in range(len(elements)):
                        if elements[i][0] != "\\":
                            elements[i] = "\\bartable" + "".join(f"{{{chord}}}" for chord in elements[i].split("_"))
            self.tmp_file.write(" & ".join(elements) + " \\\\ \n")
        self.tmp_file.write("\\end{tabular} \n")

