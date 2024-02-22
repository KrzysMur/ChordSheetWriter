import sys
import unittest

sys.path.append("..")

from src.syntax_validator import *


class TestCategorizingLines(unittest.TestCase):
    def test_correct_metadata_lines(self):
        self.assertEqual(categorize_line_type("title=foo"), METADATA_LINE)
        self.assertEqual(categorize_line_type("asdf =  C#m"), METADATA_LINE)

    def test_incorrect_lines(self):
        self.assertEqual(categorize_line_type("foo"), None)
        self.assertEqual(categorize_line_type("asd [][][as]dd[]c|||]"), None)
        self.assertEqual(categorize_line_type("\\"), None)
        self.assertEqual(categorize_line_type("]["), None)
        self.assertEqual(categorize_line_type("adsfsadf asdf asdf asdf asdfasdff"), None)

    def test_correct_chords_lines(self):
        self.assertEqual(categorize_line_type("[C_C]D|E\[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("|C_C|D|E[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("(3/4))C_C[D]E[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("("), CHORDS_LINE)
