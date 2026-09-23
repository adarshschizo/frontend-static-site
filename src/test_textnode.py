import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)

        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://boot.dev")

        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
