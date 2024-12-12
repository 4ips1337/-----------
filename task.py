import os
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor

def create_target_directory(target_dir, extension):
    """Create a subdirectory for a given extension if it does not exist."""
    ext_dir = os.path.join(target_dir, extension)
    if not os.path.exists(ext_dir):
        os.makedirs(ext_dir)
    return ext_dir

def copy_file(file_path, target_dir):
    """Copy a file to the target directory, sorted by its extension."""
    _, file_name = os.path.split(file_path)
    extension = file_name.split('.')[-1].lower()
    ext_dir = create_target_directory(target_dir, extension)
    shutil.copy2(file_path, os.path.join(ext_dir, file_name))

def process_directory(source_dir, target_dir):
    """Process a single directory: copy its files and delegate subdirectories."""
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(source_dir):
            
            for file_name in files:
                file_path = os.path.join(root, file_name)
                executor.submit(copy_file, file_path, target_dir)

            
            for dir_name in dirs:
                subdir_path = os.path.join(root, dir_name)
                executor.submit(process_directory, subdir_path, target_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort and copy files by extension.")
    parser.add_argument("source_dir", type=str, help="Path to the source directory.")
    parser.add_argument("target_dir", type=str, nargs='?', default="dist", help="Path to the target directory. Default is 'dist'.")
    args = parser.parse_args()

    source_dir = args.source_dir
    target_dir = args.target_dir

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        exit(1)

    os.makedirs(target_dir, exist_ok=True)

    process_directory(source_dir, target_dir)
    print(f"Files have been sorted and copied to '{target_dir}'.")