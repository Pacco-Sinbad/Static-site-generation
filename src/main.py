import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block_level_functions import *
from inline_text_functions import *
from text_to_html_gen import *

def extract_title(markdown):
    lines = markdown.split('\n')
    header = ""
    for line in lines:
        if line.startswith('# '):
            header = line.replace('# ', '').replace('\n', '').strip()
            break
        else:
            raise Exception('No h1 element was found to assign the title from.')
    
    return header


def copy_recursive(source_dir, dest_dir):
    items = os.listdir(source_dir)
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            print(f'Copying file: {source_path} -> {dest_path}')
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_recursive(source_path, dest_path)

def copy_static_files(source_dir, dest_dir):
    if os.path.exists(source_dir):
        contents = os.listdir(source_dir)
        print(f"Contents of {source_dir}", contents)
    else:
        print(f"{source_dir} does not exist")
        return
    
     # Handle destination directory
    if os.path.exists(dest_dir):
        print(f"Deleting everything in {dest_dir}...")
        shutil.rmtree(dest_dir)
    else:
        # Interactive prompt if destination doesn't exist
        while True:
            choice = input(f"Destination directory '{dest_dir}' doesn't exist. Would you like to:\n"
                          f"1. Create '{dest_dir}' and continue\n"
                          f"2. Enter a different destination directory\n"
                          f"3. Cancel operation\n"
                          f"Enter your choice (1, 2 or 3): ")
            
            if choice == '1':
                print(f"Creating {dest_dir} directory...")
                break
            elif choice == '2':
                new_dest = input("Enter new destination directory path: ")
                dest_dir = new_dest
                # Check if the new directory exists
                if os.path.exists(dest_dir):
                    print(f"Deleting everything in {dest_dir}...")
                    shutil.rmtree(dest_dir)
                    break
                # If new destination still doesn't exist, loop will continue
            elif choice == '3':
                print('Operation cancelled.')
                return # Exit function
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    # Create destination directory
    os.mkdir(dest_dir)
    
    # Recursively copy files
    copy_recursive(source_dir, dest_dir)
        
def generate_page(from_path, template_path, dest_path):
    if os.path.exists(from_path) and os.path.exists(template_path):
        print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    else:
        raise Exception('File paths could not be found')
    with open(from_path, 'r') as f:
        from_contents = f.read()
    with open(template_path) as f:
        template_contents = f.read()
    html_str = one_big_div(from_contents)
    title = extract_title(from_contents)
    populated_template = template_contents.replace('{{ Title }}', title).replace('{{ Content }}', html_str)
    dest_path_only = os.path.dirname(dest_path)
    os.makedirs(dest_path_only, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(populated_template)



        
        




def main():
    copy_static_files('static', 'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')
    

if __name__ == "__main__":
     main()

