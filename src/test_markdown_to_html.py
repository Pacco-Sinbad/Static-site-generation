import re
import unittest
from textnode import *
from htmlnode import *
from inline_text_functions import *
from block_level_functions import *
from main import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        html = one_big_div(md)
        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>" )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        
        html = one_big_div(md)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item
    3. Third item
    """
       
        html = one_big_div(md)
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )
    def test_unordered_list(self):
        md = """
    - First item
    - Second item
    - Third item
    """
       
        html = one_big_div(md)
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )
    def test_blockquote(self):
        md = """
    > This is a quote block
    > that spans multiple lines.
    """
       
        html = one_big_div(md)
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block that spans multiple lines.</blockquote></div>",
        )