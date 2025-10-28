from textnode import *
import re
from enum import Enum

BlockType = Enum('BlockType', ['paragraph','heading','code','quote','unordered_list','ordered_list'])

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
        if len(oldParts) == 1:
            newNodes.append(oldNode)
            continue
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
        if len(matches) == 0:
            newNodes.append(oldnode)
            continue
        while matches != None and len(matches) > 0:
            sections = original_text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
            newNodes.append(TextNode(sections[0],TextType.TEXT))
            newNodes.append(TextNode(matches[0][0],TextType.IMAGE,matches[0][1]))
            if len(matches) == 1 and len(sections) == 2 and len(sections[1]) == 0:
                break
            
            if len(matches) == 1 and len(sections) == 2 and len(sections[1]) > 0:
                newNodes.append(TextNode(sections[1],TextType.TEXT))
                break
            
            if len(matches) > 1 and len(sections) == 2:
                original_text = sections[1]
                matches = matches[1:]
            else:
                # sanity check... in an error state.
                raise Exception(f"Multiple matches indicates multiple images but no additional text found after first match. matches:{matches} sections:{sections}") 

    return newNodes

def split_nodes_link(oldnodes:list[TextNode]):
    newNodes = []
    for oldnode in oldnodes:
        original_text = oldnode.text
        matches = extract_markdown_links(original_text)
        if len(matches) == 0:
            newNodes.append(oldnode)
            continue
        while matches != None and len(matches) > 0:
            sections = original_text.split(f"[{matches[0][0]}]({matches[0][1]})", 1)
            newNodes.append(TextNode(sections[0],TextType.TEXT))
            newNodes.append(TextNode(matches[0][0],TextType.LINK,matches[0][1]))
            if len(matches) == 1 and len(sections) == 2 and len(sections[1]) == 0:
                break
            
            if len(matches) == 1 and len(sections) == 2 and len(sections[1]) > 0:
                newNodes.append(TextNode(sections[1],TextType.TEXT))
                break
            
            if len(matches) > 1 and len(sections) == 2:
                original_text = sections[1]
                matches = matches[1:]
            else:
                # sanity check... in an error state.
                raise Exception(f"Multiple matches indicates multiple links but no additional text found after first match. matches:{matches} sections:{sections}") 

    return newNodes

def text_to_textnodes(text):
    newNodes = []
    newNodes.append(TextNode(text,TextType.TEXT))
    newNodes = split_nodes_delimiter(newNodes,"`",TextType.CODE)
    newNodes = split_nodes_delimiter(newNodes,"**",TextType.BOLD)
    newNodes = split_nodes_delimiter(newNodes,"_",TextType.ITALIC)
    newNodes = split_nodes_image(newNodes)
    newNodes = split_nodes_link(newNodes)
    return newNodes

def markdown_to_blocks(markdown):
    markdownBlocks = markdown.split('\n\n')
    results = []
    for s in markdownBlocks:
        stripped = s.strip()
        if len(stripped) > 0:
            results.append(stripped)
    
    return results


def block_to_block_type(markdown):
    #todo: add case for each BlockType
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if markdown.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.heading
    
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if markdown.startswith("```") & markdown.endswith("```"):
        return BlockType.code

    # Every line in a quote block must start with a > character.
    if markdown.startswith(">"):
        return BlockType.quote

    # Every line in an unordered list block must start with a - character, followed by a space.
    if markdown.startswith("- "):
        return BlockType.unordered_list

    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    numeric = 0
    period = 0
    for c in markdown:
        if c == " ":
            if period == 1 and numeric > 0:
                return BlockType.ordered_list
            else:
                break
        elif c.isnumeric():
            numeric += 1
        elif c == ".":
            period += 1
        else:
            break

    # If none of the above conditions are met, the block is a normal paragraph.
        return BlockType.paragraph
