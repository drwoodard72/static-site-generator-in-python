import unittest
from textprocessing import *
from textnode import *

class TestTextProcessing(unittest.TestCase):

    def test_valid_code_block(self):
        targetType = TextType.CODE
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", targetType)
        self.assertEqual(len(new_nodes),3,"Expecting 3 Nodes")
        self.assertEqual(new_nodes[0].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")
        self.assertEqual(new_nodes[1].text_type,targetType,f"Expecting first node be {targetType}")
        self.assertEqual(new_nodes[2].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")

    def test_valid_bold_block(self):
        targetType = TextType.BOLD
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", targetType)
        self.assertEqual(len(new_nodes),3,"Expecting 3 Nodes")
        self.assertEqual(new_nodes[0].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")
        self.assertEqual(new_nodes[1].text_type,targetType,f"Expecting first node be {targetType}")
        self.assertEqual(new_nodes[2].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")

    def test_valid_italic_block(self):
        targetType = TextType.ITALIC
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", targetType)
        self.assertEqual(len(new_nodes),3,"Expecting 3 Nodes")
        self.assertEqual(new_nodes[0].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")
        self.assertEqual(new_nodes[1].text_type,targetType,f"Expecting first node be {targetType}")
        self.assertEqual(new_nodes[2].text_type,TextType.TEXT,"Expecting first node be TextType.TEXT")

    def test_bad_delimiter(self):
        with self.assertRaises(ValueError) as context:
            targetType = TextType.ITALIC
            node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], ",", targetType)
        self.assertEqual(str(context.exception),"Invalid Delimiter")

        with self.assertRaises(ValueError) as context:
            targetType = TextType.BOLD
            node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", targetType)
        self.assertEqual(str(context.exception),"Delimiter TextType mismatch")

    def test_bad_unclosed_delimiter(self):
        with self.assertRaises(Exception) as context:
            targetType = TextType.ITALIC
            node = TextNode("This is text with a _italic block word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", targetType)
        self.assertEqual(str(context.exception),"Invalid markdown text")

if __name__ == "__main__":
    unittest.main()