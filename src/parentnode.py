from typing import List, Dict, Self 
from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:List[HTMLNode], value:str=None, props:Dict[str,str]=None ):
        if tag == None or tag == "" or tag == "None":
            raise ValueError("tag must have a value")
        if children == None or len(children) == 0:
            raise ValueError("parent must have children")
        super().__init__(tag,value,children,props)  #tag,value,children,props)

    def to_html(self) -> str:
        if self.tag == None or self.tag == "":
            raise ValueError("tag must have a value")
        if self.children == None or len(self.children) == 0:
            raise ValueError("parent must have children")
        return super().to_html()