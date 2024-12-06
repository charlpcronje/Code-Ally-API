import os
import re

def parse_markdown_for_files(input_file):
    """
    Parse the given markdown file and extract code blocks along with their target filenames.
    This function assumes a pattern like:
    ## filename.ext
    ```language
    ... code ...
    ```
    """
    files_content = {}
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filename_pattern = re.compile(r"^##\s+(.*)$")
    code_block_start_pattern = re.compile(r"^```")
    
    current_filename = None
    capturing = False
    code_lines = []

    for line in lines:
        line_stripped = line.rstrip("\n")

        if not capturing:
            # Look for filename line
            match = filename_pattern.match(line_stripped)
            if match:
                current_filename = match.group(1).strip()
                code_lines = []  # Reset code lines for this file
                continue

            # If we have a current_filename and we find a code block start:
            if current_filename and code_block_start_pattern.match(line_stripped):
                # Start capturing code lines
                capturing = True
                continue
        else:
            # We are capturing code until we hit a code_block end
            if code_block_start_pattern.match(line_stripped):
                # End of code block
                capturing = False
                # Store the captured lines into the dictionary
                files_content[current_filename] = "\n".join(code_lines) + "\n"
                current_filename = None
                code_lines = []
            else:
                code_lines.append(line_stripped)

    return files_content

def create_files_from_markdown(input_file):
    files_content = parse_markdown_for_files(input_file)
    for fname, content in files_content.items():
        # Ensure directory structure if any
        dir_name = os.path.dirname(fname)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Created {len(files_content)} files.")

if __name__ == "__main__":
    create_files_from_markdown("all.md")