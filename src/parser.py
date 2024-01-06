
class Parser:
    def __init__(self, input_text: list[str]):
        self.input_text = input_text
        self.metadata = self.get_metadata()
        self.sections = self.divide_into_sections()

    def get_metadata(self):
        metadata = {}
        while self.input_text[0] != "":
            line = self.input_text.pop(0).split("=")
            metadata.update({line[0]: line[1]})
        if "tempo" in metadata.keys():
            metadata["tempo"] = int(metadata.get("tempo"))
        if "capo" in metadata.keys():
            metadata["capo"] = int(metadata.get("capo"))
        if "chords" in metadata.keys():
            metadata["chords"] = [chord.strip() for chord in metadata.get("chords").split(",")]
        self.input_text.pop(0)
        return metadata

    def divide_into_sections(self):
        sections = []
        for i in range(len(self.input_text)):
            if self.input_text[i][0] == "@":
                sections.append([])
            sections[-1].append(self.input_text[i])
        return sections
