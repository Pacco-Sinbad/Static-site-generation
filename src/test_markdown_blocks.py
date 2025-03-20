import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_text_functions import *
from block_level_functions import *
from main import *

class TestMarkdownBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
This is **bolded** paragraph



with many new lines



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is **bolded** paragraph",
            "with many new lines",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
        
    def test_markdown_to_blocks_lots_of_whitespace(self):
        md = """
               This is **bolded** paragraph



                   with many new lines                   



           This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is **bolded** paragraph",
            "with many new lines",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
    
    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \n\t  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block with no empty lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block with no empty lines"])

    def test_markdown_to_blocks_trailing_leading_newlines(self):
        md = "\n\n\nActual content here\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Actual content here"])

# TEST BLOCK TYPES RETURNS 

    def test_markdown_headings(self):
        md = "## this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_levels(self): # Given by Boots
        for i in range(1, 7):
            md = "#" * i + " Heading"
            block_type = block_to_block_type(md)
            self.assertEqual(block_type, BlockType.HEADING)
    
    def test_markdown_code(self):
        md = "```for i in range(len(lines))```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_multiline_code(self): # Given by Boots and I changed the conditional to match
        md = """```
def sample_function():
    return "Hello World"
```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_markdown_quote(self):
        md = """>This is a quote
>with more than one 
>line.    
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_markdown_ul(self):
        md = """
        - apples
        - pears
        - cherries
        """
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_markdown_ol(self):
        md = """
        1. apples
        2. pears
        3. cherries
        """
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_paragraph(self):
        md = """this is just a paragraph
        that has no rules
It is stupid
    with white space all over"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)