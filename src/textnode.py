from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str=""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other:TextType):
        return self.text == other.text and  self.text_type == other.text_type and self.url == other.url # pyright: ignore[reportAttributeAccessIssue]

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",TextNode.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img",props={"alt":text_node.text, "src":text_node.url})
    raise ValueError("Unknown TextType")
