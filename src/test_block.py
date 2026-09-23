import unittest

from block import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "This is a single paragraph."

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is a single paragraph."
            ],
        )

    def test_multiple_blocks(self):
        md = """# Heading

First paragraph.

Second paragraph.

- Item 1
- Item 2
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "First paragraph.",
                "Second paragraph.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_empty_blocks(self):
        md = """
        
First block


Second block



Third block

"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """

        First block

        Second block

        """

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
            ],
        )

    def test_empty_markdown(self):
        md = ""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [],
        )

    def test_only_whitespace(self):
        md = "   \n\n   \n\n   "

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [],
        )


if __name__ == "__main__":
    unittest.main()
