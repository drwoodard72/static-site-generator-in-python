from typing import List, Dict, Self 
from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag:str=None, value:str=None, props:Dict[str,str]=None ):
        super().__init__(tag,value,None,props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError()
        if self.tag == None or len(self.tag) == 0:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

