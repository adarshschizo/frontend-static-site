import unittest

from block import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


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
            ["This is a single paragraph."],
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


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n"
            "\n"
            "This is another paragraph with _italic_ "
            "text and `code` here\n"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph "
            "text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> "
            "text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>This is a heading</h1></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "## This is **bold** and _italic_"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h2>This is <b>bold</b> and <i>italic</i></h2></div>",
        )

    def test_quote(self):
        md = (
            "> This is a quote\n"
            "> This is the second line\n"
            "> And this is **bold**"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>"
            "This is a quote This is the second line "
            "And this is <b>bold</b>"
            "</blockquote></div>",
        )

    def test_quote_without_space(self):
        md = (
            ">First quote\n"
            ">Second quote"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>"
            "First quote Second quote"
            "</blockquote></div>",
        )

    def test_unordered_list(self):
        md = (
            "- First item\n"
            "- Second item\n"
            "- Third **bold** item"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third <b>bold</b> item</li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = (
            "1. First item\n"
            "2. Second item\n"
            "3. Third item"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third item</li>"
            "</ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = (
            "1. First **bold** item\n"
            "2. Second _italic_ item\n"
            "3. Third `code` item"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol>"
            "<li>First <b>bold</b> item</li>"
            "<li>Second <i>italic</i> item</li>"
            "<li>Third <code>code</code> item</li>"
            "</ol></div>",
        )

    def test_unordered_list_with_links(self):
        md = (
            "- Visit [Boot.dev](https://boot.dev)\n"
            "- Visit [Google](https://google.com)"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            '<div><ul>'
            '<li>Visit <a href="https://boot.dev">Boot.dev</a></li>'
            '<li>Visit <a href="https://google.com">Google</a></li>'
            "</ul></div>",
        )

    def test_link_and_image(self):
        md = (
            "This has a [link](https://boot.dev) "
            "and ![image](https://example.com/image.png)"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            '<div><p>This has a '
            '<a href="https://boot.dev">link</a> '
            'and <img src="https://example.com/image.png" '
            'alt="image"></img></p></div>',
        )

    def test_multiple_blocks(self):
        md = (
            "# Title\n"
            "\n"
            "This is a paragraph.\n"
            "\n"
            "- One\n"
            "- Two\n"
            "\n"
            "> A quote\n"
            "\n"
            "1. First\n"
            "2. Second"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>This is a paragraph.</p>"
            "<ul><li>One</li><li>Two</li></ul>"
            "<blockquote>A quote</blockquote>"
            "<ol><li>First</li><li>Second</li></ol>"
            "</div>",
        )

    def test_empty_markdown(self):
        md = ""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div></div>",
        )


if __name__ == "__main__":
    unittest.main()