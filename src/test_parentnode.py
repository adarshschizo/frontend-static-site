import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode(None, " normal ")
        child3 = LeafNode("i", "Italic")

        parent = ParentNode("p", [child1, child2, child3])

        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> normal <i>Italic</i></p>",
        )

    def test_parent_with_props(self):
        child = LeafNode("span", "Hello")

        parent = ParentNode(
            "div",
            [child],
            {"class": "container"},
        )

        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>Hello</span></div>',
        )

    def test_no_children(self):
        parent = ParentNode("div", [])

        self.assertEqual(
            parent.to_html(),
            "<div></div>",
        )

    def test_missing_tag(self):
        parent = ParentNode(None, [])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_missing_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
