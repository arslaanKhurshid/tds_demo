import os

def read_python_files(src):
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"\n--- File: {file_path} ---\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Example usage:
# Replace this with your actual source directory
src_directory = 'C:\\Users\\arsla\\OneDrive\\Desktop\\collegeProj\\backend'
read_python_files(src_directory)
