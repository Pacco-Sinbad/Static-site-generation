import os
import unittest
from main import *

class Test_Markdown_Extraction(unittest.TestCase):

    def test_extract_title(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien"""
        self.assertEqual(extract_title(md), 'Tolkien Fan Club')
    def test_no_title_raise(self):
        md = ' Hello'
        with self.assertRaises(Exception):
            extract_title(md)