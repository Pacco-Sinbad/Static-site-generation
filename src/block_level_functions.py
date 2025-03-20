import re
from block_types import BlockType
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

def markdown_to_blocks(markdown):
    block_list = markdown.split('\n\n')
    result = []
    for block in block_list:
        stripped_block = block.strip()
        if stripped_block:
            lines = stripped_block.split('\n')
            cleaned_lines = [line.strip() for line in lines]
            normalized_block = "\n".join(cleaned_lines)
            result.append(normalized_block)
    return result
   
def block_to_block_type(markdown_block):
    if re.match(r"#{1,6} ", markdown_block):
        return BlockType.HEADING
    elif re.match(r"```", markdown_block.strip()) and re.search(r'```$', markdown_block.strip()):
        return BlockType.CODE
    elif markdown_block.startswith('>'):
        lines = markdown_block.split("\n")
        tru_lines = list(filter(lambda x: x.strip() != "", lines))
        if all(line.startswith('>') for line in tru_lines):
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    elif re.search(r"^\s*- ", markdown_block, re.MULTILINE):
        lines = markdown_block.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        if all(line.strip().startswith('- ') for line in non_empty_lines):
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    elif re.search(r"^\s*1\. ", markdown_block, re.MULTILINE):
        lines = markdown_block.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        for i, line in enumerate(non_empty_lines):
            expected_prefix = f"{i+1}. "
            if not line.strip().startswith(expected_prefix):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
        
        
    