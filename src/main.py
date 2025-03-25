import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block_level_functions import *
from inline_text_functions import *
from text_to_html_gen import *

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
        
    


def main():
    copy_static_files('static', 'public')

if __name__ == "__main__":
     main()

