import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
    else:
        raise Exception("The text does not match any defined text types")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue
        if node.text.count(f'{delimiter}') % 2 > 0:
            raise Exception('Improper markdown syntax. Any substring with a special text type must be contained between an openning and closing tag')
        else:
            node_split_by_delimiter = node.text.split(delimiter)
            for i, st in enumerate(node_split_by_delimiter):
                if st == "":
                    continue
                if i % 2 != 0:
                    new_node_list.append(TextNode(st, text_type))
                else:
                    new_node_list.append(TextNode(st, TextType.TEXT))
    return new_node_list
               
def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return links
        
def split_nodes_image(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0:
            new_node_list.append(node)
            continue
        else:
            images = extract_markdown_images(node.text)
            split_up_text = node.text

            for img in images:
                alt_text = img[0]
                Iurl = img[1]
                image_text = f"![{alt_text}]({Iurl})"

                split_lst = split_up_text.split(image_text, 1)
                if split_lst[0] != "":
                    new_node_list.append(TextNode(f"{split_lst[0]}", TextType.TEXT))
                new_node_list.append(TextNode(f"{alt_text}", TextType.IMAGE, Iurl))
                if len(split_lst) > 1:
                    split_up_text = split_lst[1]
                else:
                    split_up_text = ""
            if split_up_text != "":
                new_node_list.append(TextNode(f'{split_up_text}', TextType.TEXT))    
    return new_node_list
                

def split_nodes_link(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if len(extract_markdown_links(node.text)) == 0:
            new_node_list.append(node)
            continue
        else:
            links = extract_markdown_links(node.text)
            split_up_text = node.text
            for link in links:
                alt_text = link[0]
                Lurl = link[1]
                link_text = f"[{alt_text}]({Lurl})"

                split_lst = split_up_text.split(link_text, 1)
                if split_lst[0] != "":
                    new_node_list.append(TextNode(f"{split_lst[0]}", TextType.TEXT))
                new_node_list.append(TextNode(f"{alt_text}", TextType.LINK, Lurl))
                if len(split_lst) > 1:
                    split_up_text = split_lst[1]
                else:
                    split_up_text = ""
            if split_up_text != "":
                new_node_list.append(TextNode(f'{split_up_text}', TextType.TEXT))  
    return new_node_list  

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text,TextType.TEXT)], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    result = []
    for node in nodes:
        result.extend(split_nodes_image([node]))
    last_result =[]
    for node in result:
        last_result.extend(split_nodes_link([node]))
    return last_result
   
        







def main():

    pass


if __name__ == "__main__":
     main()

