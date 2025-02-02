import os
import shutil

def move_files():
    # Define source directory (current directory) and destination directory
    source_dir = os.getcwd()
    destination_dir = os.path.join(source_dir, "fixed")
    
    # Create 'fixed' directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate through all files in the current directory
    for file in os.listdir(source_dir):
        if os.path.isfile(file):
            # Extract filename without extension
            name_without_ext, _ = os.path.splitext(file)
            
            # Check if the filename ends with 'a', 'b', or 'c'
            if name_without_ext[-1].lower() in {'a', 'b', 'c'}:
                # Move file to 'fixed' folder
                shutil.move(file, os.path.join(destination_dir, file))
                print(f"Moved: {file}")

if __name__ == "__main__":
    move_files()
