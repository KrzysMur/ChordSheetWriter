import logging
from input_parser import divide_line_into_elements, is_barline

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(message)s",
    # filename="../console_output.log"
)

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

    for char in line:
        if ord(char) > 127:
            logging.error(f"'{line}'   Invalid character: '{char}'")
            return False

    if not line_type:
        logging.error(f"'{line}'   Invalid line")
        return False

    if line_type == METADATA_LINE:

        split_line = line.split("=")
        logging.debug(split_line)
        if len(split_line) != 2:
            logging.error(f"'{line}'    Unexpected '='")
            return False
        if split_line[0].strip() not in METADATA_KEYS:
            logging.error(f"'{line}'    Invalid metadata key")
            return False
        if split_line[1].strip() == "":
            logging.error(f"'{line}'   Metadata value cannot be empty")
            return False

    if line_type == CHORDS_LINE:

        line_no_time_signature = line.replace(" ", "")

        if line[0] == "(":
            if ")" not in line_no_time_signature:
                logging.error(f"'{line}'   No closing bracket in time signature")
                return False

            time_signature = line_no_time_signature[1:line_no_time_signature.find(")")].split("/")
            line_no_time_signature = line_no_time_signature[line_no_time_signature.find(")")+1:]

            if line_no_time_signature == "":
                logging.error(f"'{line}'   Empty line")
                return False

            if len(time_signature) == 1:
                logging.error(f"'{line}'   '/' expected in time signature")
                return False
            if len(time_signature) > 2:
                logging.error(f"'{line}'   Unexpected '/' in time signature")
                return False
            for el in time_signature:
                try:
                    int(el)
                except ValueError:
                    logging.error(f"'{line}'   Expected a number in time signature, got '{el}'")
                    return False

        if line_no_time_signature[0] not in "[|":
            logging.error(f"'{line}'   No bar line at the beginning of the line")
            return False

        if line_no_time_signature[-1] not in "]|":
            logging.error(f"'{line}'   No bar line at the end of the line")
            return False

        line_elements = divide_line_into_elements(line_no_time_signature)

        for element in line_elements:
            if is_barline(element[0]):
                if len(element) > 1:
                    if element != "][":
                        logging.error(f"'{line}'   Empty bar: '{element}'")
                        return False
    return True


def validate_syntax(lines):
    is_chords_line = False
    for line in lines:
        if not is_valid(line):
            return False
        elif line[0] in "[(|" and line[-1] in "]|":
            is_chords_line = True
    return is_chords_line
