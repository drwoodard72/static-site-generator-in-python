import unittest
from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_1(self):        
        newNode = HTMLNode("div","value text")
        self.assertEqual(str(newNode),'HTMLNode("div","value text",None,None)')

    def test_2(self):        
        childNodes = [HTMLNode("a","kernel",None,{"href":"http://www.kernel.org/","target":"_blank"})]
        newNode = HTMLNode("div","value text",childNodes)
        self.assertEqual(str(newNode),"HTMLNode(\"div\",\"value text\",None,[HTMLNode(\"a\",\"kernel\",{'href': 'http://www.kernel.org/', 'target': '_blank'},None)])")

    def test_3(self):        
        childNodes = [HTMLNode("a","kernel",None,{"href":"http://www.kernel.org/","target":"_blank"})]
        newNode = HTMLNode("div","value text",childNodes)
        self.assertEqual(newNode.to_html(),"<div>value text<a href=\"http://www.kernel.org/\" target=\"_blank\">kernel</a></div>")

if __name__ == "__main__":
    unittest.main()