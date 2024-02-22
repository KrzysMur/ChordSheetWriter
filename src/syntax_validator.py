import logging as log


METADATA_LINE = 1
CHORDS_LINE = 2

METADATA_KEYS = ["title", "author", "album", "key", "tempo", "chords", "capo"]





def categorize_line_type(line):
    if "=" in line:
        return METADATA_LINE
    if line[0] in "([|":
        return CHORDS_LINE



def is_valid(line):
    line_type = categorize_line_type(line)

    if not line_type:
        log.error(f"'{line}'   Invalid line")
        return False

    if line_type == METADATA_LINE:

        split_line = line.split("=")
        log.debug(split_line)
        if len(split_line) != 2:
            log.error(f"'{line}'    Unexpected '='")
            return False
        if split_line[0].strip() not in METADATA_KEYS:
            log.error(f"'{line}'    Invalid metadata key")
            return False
        if split_line[1].strip() == "":
            log.error(f"'{line}'   Metadata value cannot be empty")
            return False

    if line_type == CHORDS_LINE:

        line_no_time_signature = line.replace(" ", "")

        if line[0] == "(":

            time_signature = line_no_time_signature[1:line_no_time_signature.find(")")].split("/")
            line_no_time_signature = line_no_time_signature[line_no_time_signature.find(")")+1:]

            if len(time_signature) == 1:
                log.error(f"'{line}'   '/' expected in time signature")
                return False
            if len(time_signature) > 2:
                log.error(f"'{line}'   Unexpected '/' in time signature")
                return False
            for el in time_signature:
                try:
                    int(el)
                except ValueError:
                    log.error(f"'{line}'   Expected a number in time signature, got '{el}'")
                    return False

        if line_no_time_signature[0] not in "[|":
            log.error(f"'{line}'   No bar line at the begining of the line")
            return False

        if line_no_time_signature[-1] not in "]|":
            log.error(f"'{line}'   No bar line at the end of the line")
            return False

        segments = [line_no_time_signature[0]]
        for i in range(1, len(line_no_time_signature)):
            if segments[-1][-1] in


    return True



def validate_syntax(lines):
    for line in lines:
        if not is_valid(line):
            return False
    return True
