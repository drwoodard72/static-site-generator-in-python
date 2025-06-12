from textnode import *

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
