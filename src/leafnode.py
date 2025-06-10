from typing import List, Dict, Self 
from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag:str="", value:str="", props:Dict[str,str]=None ):
        super().__init__(tag,value,None,props)

    def to_html(self) -> str:
        if self.value == None or self.value == "":
            raise ValueError()
        return super().to_html()

