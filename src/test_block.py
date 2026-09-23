import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


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


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_multiline_paragraph(self):
        block = (
            "This is a paragraph.\n"
            "This is still the same paragraph."
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_level_1(self):
        block = "# Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_2(self):
        block = "## Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_3(self):
        block = "### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_4(self):
        block = "#### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_5(self):
        block = "##### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_6(self):
        block = "###### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_invalid_heading_without_space(self):
        block = "###Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_invalid_heading_too_many_hashes(self):
        block = "####### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\nprint('Hello, world!')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_multiline_code_block(self):
        block = (
            "```\n"
            "def hello():\n"
            "    print('Hello')\n"
            "\n"
            "hello()\n"
            "```"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_invalid_code_block(self):
        block = "```\nprint('Hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote_block(self):
        block = (
            "> This is a quote\n"
            "> This is another quote"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_without_space(self):
        block = (
            ">First quote\n"
            ">Second quote"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote_block(self):
        block = (
            "> First quote\n"
            "This line is not a quote"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = (
            "- First item\n"
            "- Second item\n"
            "- Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_requires_space(self):
        block = (
            "- First item\n"
            "-Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one(self):
        block = (
            "2. First item\n"
            "3. Second item\n"
            "4. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_increment(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "4. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_requires_space(self):
        block = (
            "1. First item\n"
            "2.Second item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()