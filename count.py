import os

def count_lines_of_code(directory="."):
    total_lines = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)

    return total_lines

if __name__ == "__main__":
    current_directory = os.getcwd()
    lines_of_code = count_lines_of_code(current_directory)
    print(f"Total lines of code in .py files in {current_directory} and its subdirectories: {lines_of_code}")
