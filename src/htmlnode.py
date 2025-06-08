from typing import List, Dict, Self

class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:List[Self]=None, props:Dict[str,str]=None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if self.children == None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            children = []
            for child in self.children:
                if child != None:
                    children.append(child.to_html())
            return f"<{self.tag}{self.props_to_html()}>{self.value}{"".join(children)}</{self.tag}>"
        # raise NotImplementedError()
    
    def props_to_html(self) -> str:
        def kv_to_attribute(item):
            return f"{item[0]}=\"{item[1]}\""
        if self.props == None or len(self.props) == 0:
            return ""
        else:
            return " "+" ".join(map(kv_to_attribute,self.props.items()))
    
    def __repr__(self) -> str:
        return f"HTMLNode(\"{self.tag}\",\"{self.value}\",{self.props},{self.children})"
        
