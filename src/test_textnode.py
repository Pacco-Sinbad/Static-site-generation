import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_text_functions import *
from main import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_TextType_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_URL_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

# TEXT NODE TO HTML

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "http://www.example.com"})
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "http://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img" )
        self.assertEqual(html_node.props, {'src': "http://www.example.com", 'alt':node.text})
        self.assertEqual(html_node.value, "")

# CONSTRUCT NODE LISTS WITH BOLD ITALIC AND CODE TEXT
    
    def test_bold(self):
        node = TextNode("This is a text node with **bold** text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a text node with ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD), 
            TextNode(" text.", TextType.TEXT) 
            ])
    
    def test_raise_for_odd_delimiters(self):
        node = TextNode("This is a text node with **bold text.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '**', TextType.BOLD)

    def test_for_no_delimiters(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode('This text has no delimiters', TextType.TEXT)])

    def test_for_front_delimiters(self):
        node = TextNode("**This** is a text node.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes,[
            TextNode('This', TextType.BOLD),
            TextNode(' is a text node.', TextType.TEXT)
        ])
    
    def test_for_double_delimiters(self):
        node = TextNode("This is **a****lot** of asterisks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode('This is ', TextType.TEXT),
            TextNode('a', TextType.BOLD),
            TextNode('lot', TextType.BOLD),
            TextNode(' of asterisks', TextType.TEXT)
        ])

# EXTRACT LINKS AND IMAGES

    def test_for_link_extraction(self):
        node = TextNode('This node contains [a link](https://example.com) [with](https://another.com)', TextType.TEXT)
        link_tups = extract_markdown_links(node.text)
        self.assertEqual(link_tups, [('a link','https://example.com'), ('with','https://another.com')])

    def test_for_image_extraction(self):
        node = TextNode('This node contains ![an image](https://example.com) ![with](https://another.com)', TextType.TEXT)
        img_tups = extract_markdown_images(node.text)
        self.assertEqual(img_tups, [('an image','https://example.com'), ('with','https://another.com')])

    def test_for_image_with_link(self):
        node = TextNode('This node contains ![an image](https://example.com) [with](https://another.com)', TextType.TEXT)
        img_tups = extract_markdown_images(node.text)
        self.assertEqual(img_tups, [('an image','https://example.com')])
    
    def test_for_link_with_image(self):
        node = TextNode('This node contains [a link](https://example.com) ![with](https://another.com)', TextType.TEXT)
        link_tups = extract_markdown_links(node.text)
        self.assertEqual(link_tups, [('a link','https://example.com')])

# CONSTRUCT NODE LISTS WITH LINKS AND IMAGES

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes)

    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://www.example.com) and another [link2](https://www.example2.com)",
        TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://www.example2.com")
        ],
        new_nodes)

    def test_split_images_with_link(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ],
        new_nodes)

    def test_split_2_images_with_link(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) another ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" another ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ],
        new_nodes)

    def test_split_links_with_image(self):
        node = TextNode(
        "This is text with a [link](https://www.example.com) and an ![image](https://www.example2.com)",
        TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and an ![image](https://www.example2.com)", TextType.TEXT),
        ],
        new_nodes)

    def test_split_2_links_with_image(self):
        node = TextNode(
        "This is text with a [link](https://www.example.com) another [link](https://www.example.com) and an ![image](https://www.example2.com)",
        TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and an ![image](https://www.example2.com)", TextType.TEXT)
        ],
        new_nodes)

# CREATING A TEXTNODE LIST FROM RAW MARKDOWN

    def test_text_to_text_nodes_list(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_node_list = text_to_textnodes(text)
        self.assertListEqual(
            
              [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                text_node_list  
            
        )
    

if __name__ == "__main__":
    unittest.main()