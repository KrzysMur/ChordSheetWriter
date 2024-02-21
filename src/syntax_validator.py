import logging as log


METADATA_LINE = 1
CHORDS_LINE = 2

METADATA_KEYS = ["title", "author", "album", "key", "tempo", "chords", "capo"]


def categorize_line_type(line):
    if "=" in line:
        return METADATA_LINE
    if line.strip()[0] in "([|":
        return CHORDS_LINE
    log.error("Can't categorize line")


def is_valid(line):
    line_type = categorize_line_type(line)
    if line_type == METADATA_LINE:
        split_line = line.split("=")
        if len(split_line) != 2 or split_line[0].strip() not in METADATA_KEYS:
            return False


    return True



def validate_syntax(lines):
    for line in lines:
        if not is_valid(line):
            return False
    return True
