import re
from block_types import BlockType
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
#HELPER
def markdown_stripper(md):
    stripped_block = md.strip()
    if stripped_block:
        lines = stripped_block.split('\n')
        cleaned_lines = [line.strip() for line in lines if line]
        normalized_block = "\n".join(cleaned_lines)
        return normalized_block
# HELPER    
def non_empty(md, delimiter):   
    lines = md.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return bool(non_empty_lines) and all(line.startswith(delimiter) for line in non_empty_lines)
    


def markdown_to_blocks(markdown):
    block_list = markdown.split('\n\n')
    result = [markdown_stripper(block) for block in block_list if markdown_stripper(block)]
    return result


def block_to_block_type(markdown_block):
    md = markdown_stripper(markdown_block)
    
    if re.match(r"#{1,6} ", md):
        return BlockType.HEADING
    elif re.match(r"```", md) and re.search(r'```$', md):
        return BlockType.CODE
    elif md.startswith('>'):
        if non_empty(md, '>'):
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    elif md.startswith("- "):       
        if non_empty(md, '- '):
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    elif md.startswith("1. "):
        lines = md.split('\n')
        for i, line in enumerate(lines):
            expected_prefix = f"{i+1}. "
            if not line.startswith(expected_prefix):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
        
        
    