# Study Organiser project 

import json

class Node:
    def __init__(self, name, is_folder=True, parent=None):
        self.children = []
        self.name = name
        self.is_folder = is_folder
        self.parent = parent
        self.content = "" 

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def __str__(self):
        return self.name

# Function to view contents of a folder
def view_contents(folder):
    print(f"Contents of {folder}:")
    for child in folder.children:
        if child.is_folder == True:
            print(f"    📁 {child.name}")
        elif child.is_folder == False:
            print(f"    📄 {child.name}")
    choice = input("Which note's content would you like to view(press 0 for none):  ").lower()
    if choice != "0":
        for child in folder.children:
            if child.name == choice and not child.is_folder:
                print(f"Content of {child.name}: {child.content}")
                break
        else:
            print("Note not found.")

def to_dict(node): 

    node_dict = {
        "name": node.name,
        "is_folder": node.is_folder,
        "content": node.content,
        "children": [to_dict(child) for child in node.children]
    }

    return node_dict

def save_structure_to_file(node):
    with open("study_structure.json", "w") as file:
        json.dump(to_dict(node), file, indent=4)


def from_dict(data):
    node = Node(data["name"], data["is_folder"])
    node.content = data["content"]

    for child in data["children"]:
        child_data = from_dict(child)
        node.add_child(child_data)

    return node

def load_structure_from_file():
    with open("study_structure.json", "r") as file:
        data = json.load(file)
        return from_dict(data)

# Function to create a new folder
def create_folder(folder,name):
    new_folder = Node(name, is_folder=True, parent=folder)
    folder.add_child(new_folder)


# Create a study note 
def create_note(folder):
    name = input("Enter the name of the note: ").lower()
    content = input("Enter the content of the note: ")
    new_note = Node(name, is_folder=False, parent=folder)
    folder.add_child(new_note)
    new_note.content = content


# Make the current folder something different
def navigate_to_folder():
    folder_name = input("Enter the name of the folder you want to navigate to: ").lower()
    for child in current_folder.children:
        if child.name == folder_name and child.is_folder:
            return child
    print("Folder not found.")
    return current_folder

def go_back():
    return current_folder.parent

def sort(folder):
    for child in current_folder.children:
        current_folder.children.sort(key=lambda x: x.name)

        print("Contents sorted A-Z.")
        view_contents(current_folder)

def delete_file(folder):
    file_name = input("Enter the name of the file you want to delete: ").lower()
    for child in folder.children:
        if child.name == file_name and not child.is_folder:
            folder.children.remove(child)
            return
    print("File not found.")

def delete_folder(folder):
    folder_name = input("Enter the name of the folder you want to delete: ").lower()
    confirmation = input("Are you sure you want to delete this folder and all its contents? (y/n): ").lower()
    if confirmation == "y":
        for child in folder.children:
            if child.name == folder_name and child.is_folder:
                folder.children.remove(child)
                return
    print("Folder not found.")



# Create the home node
root = load_structure_from_file()

# Make the current folder
current_folder = root


# Main menu loop
while True:
    print("----------------------------------")
    print(f"Current folder📁: {current_folder}")
    print("----------------------------------")

    print("1. View contents of current folder")
    print("2. Create a new folder")
    print("3. Create a new note")
    print("4. Navigate to a folder")
    print("5. Go back")
    print("6. Sort contents of the current folder A-Z")
    print("7. Delete a file")
    print("8. Delete a folder")
    print("9. Exit and save ")

    choice = input("\nWhat would you like to do? (1-9): ")

    if choice == "1":
        view_contents(current_folder)
    elif choice == "2":
        folder_name = input("Enter the name of the new folder: ").lower()
        create_folder(current_folder, folder_name)
    elif choice == "3":
        create_note(current_folder)
    elif choice == "4":
        current_folder = navigate_to_folder()
    elif choice == "5":
        current_folder = go_back()
    elif choice == "6":
        sort(current_folder)
    elif choice == "7":
        delete_file(current_folder)
    elif choice == "8":
        delete_folder(current_folder)
    elif choice == "9":
        print("Exiting...")
        save_structure_to_file(root)
        break
    else:
        print("Invalid choice. Please try again.")



    