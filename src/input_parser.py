from music_sheet_elements import *


class InputParser:
    def __init__(self, _input: list[str]):
        self.input = _input

    def get_metadata(self, return_metadate_ending_index=False):
        metadata = {}
        i = 0
        while "=" in self.input[i]:
            key, value = self.input[i].split("=")
            metadata.update({key.strip().lower(): value.strip()})
            i += 1
        if "chords" in metadata:
            metadata.update({"chords": parse_chords(metadata["chords"])})
        return (fill_in_metadata(metadata), i) if return_metadate_ending_index else fill_in_metadata(metadata)

    def parse_song(self, song_starting_index=0):
        song_lines = [self.input[i] for i in range(song_starting_index, len(self.input))]
        return [parse_line(line) for line in song_lines]

    def parse(self):
        metadata, end_index = self.get_metadata(return_metadate_ending_index=True)
        song = self.parse_song(end_index)
        return metadata, song


def fill_in_metadata(metadata):
    keys = ["title", "author", "album", "key", "tempo", "chords", "capo"]
    for key in keys:
        if key not in metadata:
            metadata.update({key: "N/A"})
    return metadata


def parse_chords(chords):
    return [chord.strip() for chord in chords.split(",")]


def parse_line(line):
    time_signature = []

    if line[0] == "(":
        time_sig_end = line.find(")")
        numerator, denominator = line[1:time_sig_end].split("/")
        time_signature.append(TimeSignature(numerator, denominator))
        line = line[time_sig_end+1:].strip()

    line_elements = [line[0]]
    for char in line[1:]:
        if is_barline(line_elements[-1][-1]) == is_barline(char):
            line_elements[-1] += char
        else:
            line_elements.append(char)
    elements = []
    for i in range(len(line_elements)):
        if i % 2 == 0:
            elements.append(BarLine(line_elements[i]))
        else:
            elements.append(BarChords(line_elements[i]))
    return time_signature + elements


def is_barline(char: str):
    return char[0] in "[]|"



