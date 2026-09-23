import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(
            extract_title(markdown),
            "Hello",
        )

    def test_extract_title_with_whitespace(self):
        markdown = "#    Hello World    "

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_extract_title_with_other_headings(self):
        markdown = (
            "## Not the title\n"
            "\n"
            "# Real Title\n"
            "\n"
            "Some content"
        )

        self.assertEqual(
            extract_title(markdown),
            "Real Title",
        )

    def test_extract_title_not_first_line(self):
        markdown = (
            "Some text\n"
            "\n"
            "# My Title\n"
            "\n"
            "More text"
        )

        self.assertEqual(
            extract_title(markdown),
            "My Title",
        )

    def test_extract_title_missing(self):
        markdown = "## Only an H2"

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
