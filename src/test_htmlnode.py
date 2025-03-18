import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        # Test when props is None
        node = HTMLNode("p", "Hello World")  # No props provided
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one(self):
        node = HTMLNode("p", "Hello World", None, {'href': 'https://example.com'})  # one prop provided
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_some(self):
        node = HTMLNode("p", "Hello World", None, {'href': 'https://example.com', 'target': "_blank"})  # multipe props provided
        result = node.props_to_html()
        res1 = ' href="https://example.com" target="_blank"'
        res2 = ' target="_blank" href="https://example.com"'
        self.assertTrue(result == res1 or result == res2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode('p', "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_leaf_to_html_a_with_prop(self):
        node = LeafNode('a', "Hello World", {'href': 'https://www.example.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Hello World</a>')

    def test_leaf_to_html_span_with_class(self):
        node= LeafNode('span', "Date", {'class': 'content'})
        self.assertEqual(node.to_html(), '<span class="content">Date</span>')

class TestParentNode(unittest.TestCase):
    def test_ParentNode_to_html(self):
        child_node = LeafNode('span', "child")
        node = ParentNode('p', [child_node])
        self.assertEqual(node.to_html(), '<p><span>child</span></p>')
    
    def test_ParentNode_with_grandchild_to_html(self):
        grandchild_node = LeafNode('i', 'grandchild')
        child_node = ParentNode('span', [grandchild_node])
        node = ParentNode('p', [child_node])
        self.assertEqual(node.to_html(), '<p><span><i>grandchild</i></span></p>')
   
    def test_ParentNode_with_multiple_grandchildren_to_html(self):
        grandchild_node1 = LeafNode('i', 'grandchild#1')
        grandchild_node2 = LeafNode('i', 'grandchild2')
        grandchild_node3 = LeafNode('i', 'grandchild3')
        child_node1 = ParentNode('span', [grandchild_node1,grandchild_node2])
        child_node2 = ParentNode('p', [grandchild_node3])
        node = ParentNode('article', [child_node1,child_node2], {'class': 'content'})
        self.assertEqual(node.to_html(), '<article class="content"><span><i>grandchild#1</i><i>grandchild2</i></span><p><i>grandchild3</i></p></article>')
        
    def test_ParentNode_without_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode('p', [])

    def test_ParentNode_without_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode('span', 'child')])


if __name__ == "__main__":
    unittest.main()