import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
            props={},
        )

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
        )

        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
            props={"class": "text"},
        )

        representation = repr(node)

        self.assertIn("tag='p'", representation)
        self.assertIn("value='Hello'", representation)
        self.assertIn("props={'class': 'text'}", representation)


if __name__ == "__main__":
    unittest.main()
