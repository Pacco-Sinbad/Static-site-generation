import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block_level_functions import *
from inline_text_functions import *

# TAKES MARKDOWN AND CREATES A LIST OF BLOCKS. FROM THAT LIST IT CREATES A LIST OF TUPLES WHERE THE FIRST ELEMENT IS THE BLOCK AND THE SECOND IS THE BLOCKTYPE
def prep_markdown(markdown):
    block_list = markdown_to_blocks(markdown)
    
    block_types = []
    for block in block_list:
        block_type = block_to_block_type(block)
        block_types.append((block, block_type))
    return block_types


# MEANT TO WORK WITH TEXT TO CHILDREN FOR UNDORDERED LISTS AND QUOTEBLOCKS
def block_split(block, delim, block_type=None):

    block_list = block.split('\n')
    if block_type == BlockType.QUOTE:       
        clean_blocks = [block.replace(delim,'',1)+' ' for block in block_list if block]
        clean_blocks[-1] = clean_blocks[-1].strip()
        textnodes = [TextNode(line,TextType.TEXT) for line in clean_blocks]
    else:
        clean_blocks = [block.replace(delim,'') for block in block_list if block]
        textnodes = [node for line in clean_blocks for node in text_to_textnodes(line)]

    return textnodes

# CONVERTS THE RAW MARKDOWN INTO TEXTNODES FOR EACH TUPLE. AND RETURNS A LIST OF NEW TUPLE WITH THE TEXTNODES IN THE THIRD POSITION
def text_to_children(blocks_with_types):
    blocks_types_textnodes = []
    for block, block_type in blocks_with_types:
        # print(f"DEBUGGER Unexpected block type: {block_type}")
        if block_type == BlockType.CODE:
            clean_block = block.strip('`').strip()     
            blocks_types_textnodes.append((block, block_type, [TextNode(clean_block + '\n', TextType.CODE)]))
        elif block_type == BlockType.HEADING:
            clean_block = block.replace('#', ' ').strip()
            blocks_types_textnodes.append((block, block_type, text_to_textnodes(clean_block)))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split('\n')
            all_item_nodes = []
    
            for item in list_items:
                if item.strip().startswith('- '):
                # Remove the "- " prefix
                    item_text = item.strip()[2:]
                # Process any formatting in the list item
                    item_nodes = text_to_textnodes(item_text)
                # Add these nodes as a group (one item)
                    if item_nodes:  # Only add non-empty items
                        all_item_nodes.append(item_nodes)   
    # Now each item in all_item_nodes represents one list item
            blocks_types_textnodes.append((block, block_type, all_item_nodes))

            # print(f'DEBUGGER {block}')
            # textnodes = block_split(block, '- ')
            # blocks_types_textnodes.append((block, block_type, textnodes))
        elif block_type == BlockType.ORDERED_LIST:
            block_list = block.split('\n')
            all_item_nodes = []
    
            for i, block_item in enumerate(block_list):
                if block_item.strip():  # Skip empty lines
                    expected_prefix = f'{i+1}. '
                    item_text = block_item.replace(expected_prefix, '', 1)
                    # Process the item text to handle formatting like bold, italic, code, etc.
                    item_nodes = text_to_textnodes(item_text)
                    if item_nodes:  # Only add non-empty items
                        all_item_nodes.append(item_nodes)
    
            blocks_types_textnodes.append((block, block_type, all_item_nodes))
        elif block_type == BlockType.QUOTE:
            textnodes = block_split(block, '> ', block_type)
            blocks_types_textnodes.append((block, block_type, textnodes))
        elif block_type == BlockType.PARAGRAPH:
            cleaned_block = block.replace('\n', ' ')  # Collapse all internal newlines into spaces
            blocks_types_textnodes.append((block,block_type, text_to_textnodes(cleaned_block)))
        else:
            raise Exception("The block type is not recognized")
    return blocks_types_textnodes

# def li_generator(text_nodes):
#     link_nodes = [text_node_to_html_node(node) for node in text_nodes]
#     lis = [LeafNode('li', link.to_html()) for link in link_nodes]
#     return lis
def li_generator(text_nodes):
    lis = []
    
    # Check if we have a list of lists (grouped by item) or just a flat list
    if text_nodes and isinstance(text_nodes[0], list):
        # We have a list of lists - each inner list is one item
        for item_nodes in text_nodes:
            # Convert each text node in this item to HTML
            html_nodes = [text_node_to_html_node(node) for node in item_nodes]
            # Combine the HTML
            item_html = ''.join(node.to_html() for node in html_nodes)
            lis.append(LeafNode('li', item_html))
    else:
        # We have a flat list - each node is one item
        link_nodes = [text_node_to_html_node(node) for node in text_nodes]
        lis = [LeafNode('li', link.to_html()) for link in link_nodes]
    
    return lis

#  SIMPLY CONVERTS ALL OF THE TEXTNODES INTO HTML NODES BUT DOES NOT PRESERVE THEM
def textnodes_to_LeafNodes(tuples):
    blocks_types_htmlnodes = []
    for block, block_type, text_nodes in tuples:
        if block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
            blocks_types_htmlnodes.append((block,block_type,li_generator(text_nodes)))
        else:
            new_nodes = [text_node_to_html_node(node) for node in text_nodes]
            blocks_types_htmlnodes.append((block,block_type,new_nodes))
    return blocks_types_htmlnodes



# CREATE PARENT NODES
def parent_nodes_with_leaf_nodes(blocks_types_htmlnodes):
    parent_nodes = []
    for block, block_type, html_nodes in blocks_types_htmlnodes:
        if block_type == BlockType.PARAGRAPH:
            parent_nodes.append(ParentNode('p', html_nodes))
        elif block_type == BlockType.HEADING:
            clean_block = block.strip()
            count = 0
            for i in range(len(clean_block)):
                if clean_block[i] == '#':
                    count += 1
                else:
                    break
            parent_nodes.append(ParentNode(f'h{count}', html_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            parent_nodes.append(ParentNode('ol', html_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            parent_nodes.append(ParentNode('ul', html_nodes))
        elif block_type == BlockType.QUOTE:
            parent_nodes.append(ParentNode('blockquote', html_nodes))
        elif block_type == BlockType.CODE:
            # code = ParentNode('code', html_nodes)
            parent_nodes.append(ParentNode('pre', html_nodes))
    return parent_nodes

def one_big_div(markdown):
    first = prep_markdown(markdown)
    second = text_to_children(first)
    third = textnodes_to_LeafNodes(second)
    fourth = parent_nodes_with_leaf_nodes(third)
    div = ParentNode('div', fourth)
    return div.to_html()

            
            