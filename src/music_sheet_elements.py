

class BarLine:
    def __init__(self, _input: str):
        self.symbol = _input

    def get_tex_code(self):
        match self.symbol:
            case "[":
                return "\\leftrepeat"
            case "]":
                return "\\rightrepeat"
            case "|":
                return "\\normalbar"
            case "][":
                return "\\leftrightrepeat"


class BarChords:
    def __init__(self, _input):
        self.text = _input
        self.chords = self.text.split("_")

    def get_tex_code(self, bar_width):
        chords = [chord.replace("#", "\\sharp ")
                  for chord in self.chords]

        chord_width = round(bar_width / len(chords), 2)

        col_types = " ".join([f"p{{{chord_width}cm}}"
                              for _ in range(len(chords))])

        bar_content = " & ".join([f" \\adjustbox{{max width={chord_width}cm}}{{\\writechord{{{chord}}}}}"
                                  for chord in chords])

        return f"\\begin{{tabular}}[t]{{{col_types}}} {bar_content}  \\end{{tabular}} \n"


class TimeSignature:
    def __init__(self, top_number, bottom_number):
        self.top_number = top_number
        self.bottom_number = bottom_number

    def get_tex_code(self):
        return f"$ \\frac{{{self.top_number}}}{{{self.bottom_number}}} $ "

