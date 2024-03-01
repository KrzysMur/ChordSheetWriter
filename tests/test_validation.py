import sys
import unittest

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
        self.assertEqual(categorize_line_type(r"[C_C]D|E\[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("|C_C|D|E[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("(3/4))C_C[D]E[C_D]"), CHORDS_LINE)
        self.assertEqual(categorize_line_type("("), CHORDS_LINE)


class TestLineValidation(unittest.TestCase):
    def test_valid_lines_no_time_signature(self):
        self.assertTrue(is_valid("|C|C_D|"))
        self.assertTrue(is_valid("[C_D|C___D]"))
        self.assertTrue(is_valid("|C#|Db|F|_|"))
        self.assertTrue(is_valid("[C][F#7b5_Dbsus4|C_D]"))
        self.assertTrue(is_valid("[_]"))

    def test_valid_lines_with_time_signature(self):
        self.assertTrue(is_valid("(3/4) [C_D_E][F_G_B]"))
        self.assertTrue(is_valid("(4/4) |C|D|"))
        self.assertTrue(is_valid("(13/5) |C|_|_|Bb_G|"))
        self.assertTrue(is_valid("(2/4) |C|_______Bsus2|"))
        self.assertTrue(is_valid("(4/4) | C | Db7_C#m|"))

    def test_invalid_lines_no_time_signature(self):
        self.assertFalse(is_valid("][Bb_D]"))
        self.assertFalse(is_valid("|[Bb_D]"))
        self.assertFalse(is_valid("[Bb_D|]"))
        self.assertFalse(is_valid("[Bb_D"))
        self.assertFalse(is_valid("[Bb_D| [Gm_F#m]"))
        self.assertFalse(is_valid("[_"))
        self.assertFalse(is_valid("_"))
        self.assertFalse(is_valid("|||||||||||||||||"))
        self.assertFalse(is_valid("[C][D]]"))

    def test_invalid_lines_with_time_signature(self):
        self.assertFalse(is_valid("(4/) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(/3) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(/) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(a/b) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(3/a) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(b/3) [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("() [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(4/3 [C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("4/3 ) C_D|Cm_Dm|C|Bbm]"))
        self.assertFalse(is_valid("(4/3) [C_D|Cm_Dm||C|Bbm]"))
        self.assertFalse(is_valid("(4/3) [C_D|Cm_Dm|C|Bbm"))

    def test_valid_metadata_lines(self):
        self.assertTrue(is_valid("title = foo"))
        self.assertTrue(is_valid("title= 123 abc"))
        self.assertTrue(is_valid("author = foo bar"))
        self.assertTrue(is_valid("key =C#m"))
        self.assertTrue(is_valid("chords=C,D,E,F,G"))
        self.assertTrue(is_valid("chords =  A , B , C   , D   ,E,Fm "))
        self.assertTrue(is_valid("tempo = 123"))
        self.assertTrue(is_valid("tempo=123.4"))
        self.assertTrue(is_valid("capo =3"))

    def test_invalid_metadata_lines(self):
        self.assertFalse(is_valid("keys = value"))
        self.assertFalse(is_valid("author = author = author"))
        self.assertFalse(is_valid("k e y = v a l"))
        self.assertFalse(is_valid("= "))
        self.assertFalse(is_valid("title="))
        self.assertFalse(is_valid("author ="))
        self.assertFalse(is_valid(" = value"))
        self.assertFalse(is_valid("=="))