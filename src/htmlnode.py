from typing import List, Dict, Self

# def snone_tnone(value:any):
#     if value == "None":
#         return None
#     return value

def none_sempty(value:any):
    if value == None or value == "None":
        return ""
    return value

class HTMLNode:
    def __init__(self, tag:str="", value:str="", children:List[Self]=None, props:Dict[str,str]=None ):
        # print(f"HTMLNode.__init__\n  tag:({type(tag)}){tag}\n  value:({type(value)}){value}\n  children:({type(children)}){children}\n  props:({type(props)}){props}\n  ")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if self.tag == None or self.tag.strip() == "":
            return self.value
        children_html = ""
        if self.children != None and len(self.children) > 0:
            for child in self.children:
                children_html += child.to_html()
        result =  f"<{self.tag}{self.props_to_html()}>{none_sempty(self.value)}{children_html}</{self.tag}>"    
        return result

    def props_to_html(self) -> str:
        def kv_to_attribute(item):
            return f"{item[0]}=\"{item[1]}\""
        if self.props == None or len(self.props) == 0:
            return ""
        else:
            return " "+" ".join(map(kv_to_attribute,self.props.items()))
    
    def __repr__(self) -> str:
        return f"HTMLNode(\"{self.tag}\",\"{self.value}\",{self.props},{self.children})"
        
