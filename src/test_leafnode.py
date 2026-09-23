import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "My Heading")

        self.assertEqual(
            node.to_html(),
            "<h1>My Heading</h1>",
        )

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "This is just text.")

        self.assertEqual(
            node.to_html(),
            "This is just text.",
        )

    def test_leaf_without_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
