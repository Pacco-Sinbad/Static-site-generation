class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #a string representing the HTML tag name 
        self.value = value #a string representing the value of the HTML tag "ie the text inside a paragraph"
        self.children = children #a list of the HTMLNode objects representing the children of this node
        self.props = props  #PROPERTIES a dicitonary of the key-value pairs representing the attributes of the HTML tag. for a link this could be {'href': 'https://www.google.com'}
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is not None:
            props_string = ""
            for k in self.props:
                props_string += f' {k}="{self.props[k]}"'
            return props_string
        return ""

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, properties={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError('all leaf nodes must have a value')
        if self.tag == None:
            return f"{self.value}"
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):

        if not tag:
            raise ValueError("Parent node must have a valid tag")
        
        if not children:
            raise ValueError("Parent node must contain children")
        
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a valid tag")
        if self.children is None:
            raise ValueError("Parent node must contain children")
        child_string = ""
        for child in self.children:
            child_res = child.to_html()
            child_string+= child_res
        return f'<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>'