import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD,
        )

        node2 = TextNode(
            "This is a text node",
            TextType.BOLD,
        )

        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode(
            "Hello",
            TextType.TEXT,
        )

        node2 = TextNode(
            "World",
            TextType.TEXT,
        )

        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode(
            "Hello",
            TextType.TEXT,
        )

        node2 = TextNode(
            "Hello",
            TextType.BOLD,
        )

        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode(
            "Click",
            TextType.LINK,
            "https://google.com",
        )

        node2 = TextNode(
            "Click",
            TextType.LINK,
            "https://boot.dev",
        )

        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            None,
        )

        self.assertEqual(
            html_node.value,
            "This is a text node",
        )

    def test_bold(self):
        node = TextNode(
            "Bold text",
            TextType.BOLD,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            "b",
        )

        self.assertEqual(
            html_node.value,
            "Bold text",
        )

    def test_italic(self):
        node = TextNode(
            "Italic text",
            TextType.ITALIC,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            "i",
        )

        self.assertEqual(
            html_node.value,
            "Italic text",
        )

    def test_code(self):
        node = TextNode(
            "print('hello')",
            TextType.CODE,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            "code",
        )

        self.assertEqual(
            html_node.value,
            "print('hello')",
        )

    def test_link(self):
        node = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            "a",
        )

        self.assertEqual(
            html_node.value,
            "Boot.dev",
        )

        self.assertEqual(
            html_node.props,
            {
                "href": "https://www.boot.dev",
            },
        )

    def test_image(self):
        node = TextNode(
            "Boot.dev logo",
            TextType.IMAGE,
            "https://example.com/logo.png",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node.tag,
            "img",
        )

        self.assertEqual(
            html_node.value,
            "",
        )

        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/logo.png",
                "alt": "Boot.dev logo",
            },
        )

    # -----------------------------
    # text_to_textnodes() tests
    # -----------------------------

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an ![obi wan image]"
            "(https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "This is ",
                TextType.TEXT,
            ),
            TextNode(
                "text",
                TextType.BOLD,
            ),
            TextNode(
                " with an ",
                TextType.TEXT,
            ),
            TextNode(
                "italic",
                TextType.ITALIC,
            ),
            TextNode(
                " word and a ",
                TextType.TEXT,
            ),
            TextNode(
                "code block",
                TextType.CODE,
            ),
            TextNode(
                " and an ",
                TextType.TEXT,
            ),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(
                " and a ",
                TextType.TEXT,
            ),
            TextNode(
                "link",
                TextType.LINK,
                "https://boot.dev",
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text."

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "This is just plain text.",
                TextType.TEXT,
            )
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text."

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "This is ",
                TextType.TEXT,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " text.",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text."

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "This is ",
                TextType.TEXT,
            ),
            TextNode(
                "italic",
                TextType.ITALIC,
            ),
            TextNode(
                " text.",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_code(self):
        text = "Run `print('hello')` here."

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "Run ",
                TextType.TEXT,
            ),
            TextNode(
                "print('hello')",
                TextType.CODE,
            ),
            TextNode(
                " here.",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_link(self):
        text = (
            "Visit [Boot.dev](https://boot.dev) today."
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "Visit ",
                TextType.TEXT,
            ),
            TextNode(
                "Boot.dev",
                TextType.LINK,
                "https://boot.dev",
            ),
            TextNode(
                " today.",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_image(self):
        text = (
            "Here is ![an image](https://example.com/image.png)"
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "Here is ",
                TextType.TEXT,
            ),
            TextNode(
                "an image",
                TextType.IMAGE,
                "https://example.com/image.png",
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )

    def test_text_to_textnodes_multiple_links(self):
        text = (
            "[Google](https://google.com) and "
            "[Boot.dev](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "Google",
                TextType.LINK,
                "https://google.com",
            ),
            TextNode(
                " and ",
                TextType.TEXT,
            ),
            TextNode(
                "Boot.dev",
                TextType.LINK,
                "https://boot.dev",
            ),
        ]

        self.assertEqual(
            nodes,
            expected,
        )


if __name__ == "__main__":
    unittest.main()