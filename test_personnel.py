import io
import sys
import unittest
import models
import re


class TestPlayers(unittest.TestCase):

    def test_player_printer(self):
        g = models.PresidentGame()
        capturedOutput = io.StringIO()  # Create StringIO object
        prevStdout = sys.stdout
        sys.stdout = capturedOutput  # and redirect stdout.
        g.introduction_player()
        sys.stdout = prevStdout  # Reset redirect.
        output_string = str(capturedOutput.getvalue())
        number = re.findall(r'\d+', output_string)
        self.assertFalse(len(number) == 0)

if __name__ == '__main__':
    unittest.main()

