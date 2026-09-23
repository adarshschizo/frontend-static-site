import unittest

from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode(
            "This is `code` and **bold**",
            TextType.TEXT,
        )

        nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        nodes = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        self.assertEqual(nodes, expected)

    def test_multiple_code_blocks(self):
        node = TextNode(
            "Use `print()` and `input()`",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("input()", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    def test_non_text_node_is_unchanged(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(new_nodes, [node])

    def test_unclosed_delimiter(self):
        node = TextNode(
            "This is `unclosed code",
            TextType.TEXT,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )

    def test_no_delimiter(self):
        node = TextNode(
            "This is normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is normal text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertListEqual(expected, matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images(
            "This is just normal text."
        )

        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )

        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            matches,
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://www.boot.dev) "
            "and [YouTube](https://www.youtube.com)"
        )

        expected = [
            ("Boot.dev", "https://www.boot.dev"),
            ("YouTube", "https://www.youtube.com"),
        ]

        self.assertListEqual(expected, matches)

    def test_link_does_not_match_image(self):
        matches = extract_markdown_links(
            "![image](https://example.com/image.png)"
        )

        self.assertListEqual([], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links(
            "This is just normal text."
        )

        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()