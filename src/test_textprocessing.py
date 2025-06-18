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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")        
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")        
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images_and_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_links(text)        
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()