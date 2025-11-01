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

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type(self):
        # Headings start with 1-6 # characters, followed by a space and then the heading text.
        result = block_to_block_type("# level 1 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("## level 2 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("### level 3 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("#### level 4 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("##### level 5 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("###### level 6 heading text")
        self.assertEqual(result,BlockType.heading)
        result = block_to_block_type("#invalid quote block text")
        self.assertEqual(result,BlockType.paragraph)

        # Code blocks must start with 3 backticks and end with 3 backticks.
        result = block_to_block_type("```code block text```")
        self.assertEqual(result,BlockType.code)
        result = block_to_block_type("```invalid quote block text")
        self.assertEqual(result,BlockType.paragraph)
        result = block_to_block_type("invalid quote block text```")
        self.assertEqual(result,BlockType.paragraph)

        # Every line in a quote block must start with a > character.
        result = block_to_block_type(">quote block text")
        self.assertEqual(result,BlockType.quote)

        # Every line in an unordered list block must start with a - character, followed by a space.
        result = block_to_block_type("- unordered list block text")
        self.assertEqual(result,BlockType.unordered_list)
        result = block_to_block_type("-invalid unordered list block text")
        self.assertEqual(result,BlockType.paragraph)

        # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
        result = block_to_block_type("1. ordered list block text")
        self.assertEqual(result,BlockType.ordered_list)
        result = block_to_block_type("10. ordered list block text")
        self.assertEqual(result,BlockType.ordered_list)
        result = block_to_block_type("100. ordered list block text")
        self.assertEqual(result,BlockType.ordered_list)
        result = block_to_block_type(".invalid ordered list block text")
        self.assertEqual(result,BlockType.paragraph)

        # If none of the above conditions are met, the block is a normal paragraph.
        result = block_to_block_type("the block is a normal paragraph")
        self.assertEqual(result,BlockType.paragraph)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
if __name__ == "__main__":
    unittest.main()