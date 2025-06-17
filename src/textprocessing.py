from textnode import *
import re

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    newNodes = []
    newTextType = None
    match delimiter:
        case "`":
            newTextType = TextType.CODE
        case "**":
            newTextType = TextType.BOLD
        case "_":
            newTextType = TextType.ITALIC
        case _:
            raise ValueError("Invalid Delimiter")
    if newTextType != text_type:
        raise ValueError("Delimiter TextType mismatch")
    
    for oldNode in old_nodes:
       if oldNode.text_type != TextType.TEXT:
           newNodes.append(oldNode)
           continue
       oldParts = oldNode.text.split(delimiter)
       if len(oldParts) != 3:
           raise Exception("Invalid markdown text")
       oldParts[0] = TextNode(oldParts[0],TextType.TEXT)
       oldParts[1] = TextNode(oldParts[1],newTextType)
       oldParts[2] = TextNode(oldParts[2],TextType.TEXT)
       newNodes.extend(oldParts)

    return newNodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(oldnodes:list[TextNode]):
    newNodes = []
    for oldnode in oldnodes:
        original_text = oldnode.text
        matches = extract_markdown_images(original_text)
        if len(matches == 0):
            newNodes.append(oldnode)
            continue
        while matches != None and len(matches) > 0:
            sections = original_text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
            newNodes.append(TextNode(sections[0],TextType.TEXT))
            newNodes.append(TextNode(matches[0][0],TextType.IMAGE,matches[0][1]))
            if len(matches == 1) and len(sections == 2):
                newNodes.append(TextNode(sections[1],TextType.TEXT))
            elif len(matches > 1) and len(sections == 2):
                original_text = sections[1]
                matches = matches[1:]
            else:
                # todo: sanity check? is this an error state... 