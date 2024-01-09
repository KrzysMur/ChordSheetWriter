

class BarLine:
    def __init__(self, _input: str):
        self.symbol = _input

    def get_tex_code(self):
        match self.symbol:
            case "[":
                return "\\leftrepreat"
            case "]":
                return "\\rightrepeat"
            case "|":
                return "\\normalbar"


class BarChords:
    def __init__(self, _input):
        self.text = _input
        self.chords = self.text.split("_")


class TimeSignature:
    def __init__(self, top_number, bottom_number):
        self.top_number = top_number
        self.bottom_number = bottom_number
