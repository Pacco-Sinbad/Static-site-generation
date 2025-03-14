from textnode import TextNode, TextType

def main():
    new_node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")

    print(new_node)

main()