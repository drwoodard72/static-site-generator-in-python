import unittest
from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_1_simple_div(self):        
        newNode = HTMLNode("div","value text")
        self.assertEqual(newNode.to_html(),'<div>value text</div>')

    def test_2_anchor(self):        
        anchorNode = HTMLNode("a","kernel",None,{"href":"http://www.kernel.org/","target":"_blank"})
        self.assertEqual(anchorNode.to_html(),'<a href="http://www.kernel.org/" target="_blank">kernel</a>')

    def test_3_p_with_text_and_anchor(self):
        anchorNode = HTMLNode("a","kernel",None,{"href":"http://www.kernel.org/","target":"_blank"})
        pNode = HTMLNode("p","link to kernel web page",[anchorNode])
        self.assertEqual(pNode.to_html(),'<p>link to kernel web page<a href="http://www.kernel.org/" target="_blank">kernel</a></p>')

if __name__ == "__main__":
    unittest.main()