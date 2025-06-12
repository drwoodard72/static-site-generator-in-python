import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def assertEqualSecondOrThird(self, first, second, third, msg = None):
        if first != second and first != third:
            assert msg

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        node2 = TextNode("This is a BOLD node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a BOLD node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,"http://kernel.org")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node",TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertAlmostEqual
        self.assertEqualSecondOrThird(html_node.tag, "", None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(),"This is a text node")

    def test_bold(self):
        node = TextNode("bold text",TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.to_html(),"<b>bold text</b>")

    def test_link(self):
        node = TextNode("link text",TextType.LINK,"http://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link text")
        self.assertEqual(html_node.to_html(),"<a href=\"http://google.com\">link text</a>")


if __name__ == "__main__":
    unittest.main()