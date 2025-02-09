import os
import shutil
import hashlib
from collections import defaultdict

def menu():
    print("\n--- File Sorter Menu ---")
    print("1. List all files")
    print("2. Sort files into general folders")
    print("3. Delete duplicate files")
    print("4. Exit")
    return input("Enter your choice: ")

def list_files(directory):
    print("\nListing all files...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))
    print("Total files listed.")

def sort_files(directory):
    file_types = {
        'Documents': ['.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.odt'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.svg'],
        'Videos': ['.avi', '.mp4', '.mov', '.wmv', '.flv', '.mkv'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
        'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2']
    }

    file_types = {key: [ext.lower() for ext in value] for key, value in file_types.items()}

    print("\nSorting files...")
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            extension = '.' + item.split('.')[-1].lower()
            found = False
            for folder, extensions in file_types.items():
                if extension in extensions:
                    target_folder = os.path.join(directory, folder)
                    if not os.path.exists(target_folder):
                        os.mkdir(target_folder)
                    shutil.move(os.path.join(directory, item), os.path.join(target_folder, item))
                    found = True
                    break
            if not found:
                misc_folder = os.path.join(directory, 'Miscellaneous')
                if not os.path.exists(misc_folder):
                    os.mkdir(misc_folder)
                shutil.move(os.path.join(directory, item), os.path.join(misc_folder, item))
    print("Files sorted.")

def find_duplicates(directory):
    print("\nFinding duplicates...")
    files_hash = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
            files_hash[file_hash].append(path)
    return {key: paths for key, paths in files_hash.items() if len(paths) > 1}

def delete_duplicates(directory):
    duplicates = find_duplicates(directory)
    print("\nDeleting duplicates...")
    for file_hash, paths in duplicates.items(): 
        for path in paths[1:]:
            os.remove(path)
            print(f"Deleted duplicate: {path}")
    print("Duplicate files deleted.")

def main():
    base_directory = input("Enter the base directory path: ")
    while True:
        choice = menu()
        if choice == '1':
            list_files(base_directory)
        elif choice == '2':
            sort_files(base_directory)
        elif choice == '3':
            delete_duplicates(base_directory)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()