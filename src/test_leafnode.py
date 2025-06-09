import unittest
from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "some tagless text", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "some tagless text")

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "some more tagless text", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "some more tagless text")
