import os

# Edit these variables as needed:
root_directory = "/Users/christian/Repos/guide_my_trip_mobile_app/lib/src"  # Absolute or relative path to the directory
extension_string = ".dart"  # Space-separated extensions (use a leading dot) ".py .dart"
output_file = "context.txt"  # Name of the output text file


extensions = extension_string.split() if extension_string else []


def generate_tree(root_dir, prefix="", is_last=True):
    """
    Recursively generate a list of strings representing
    the directory tree structure using ASCII connectors.
    """
    lines = []
    if prefix == "" and os.path.isdir(root_dir):
        # Print the root folder name at the top.
        lines.append(os.path.basename(root_dir) + "/")

    try:
        items = sorted(os.listdir(root_dir))
    except OSError:
        # If we can't list the directory (permission, etc.), just return
        return lines

    for index, item in enumerate(items):
        path = os.path.join(root_dir, item)
        # Determine connector: └── for the last item, ├── otherwise
        is_last_item = index == len(items) - 1
        connector = "└── " if is_last_item else "├── "

        if os.path.isdir(path):
            lines.append(prefix + connector + item + "/")
            # For children, update the prefix: add "    " if last item, else "│   "
            extension = "    " if is_last_item else "│   "
            lines.extend(generate_tree(path, prefix + extension, is_last=is_last_item))
        else:
            lines.append(prefix + connector + item)

    return lines


def gather_files(root_directory, exts=None):
    """
    Recursively gather files from root_directory.
    If exts is provided, only files with those extensions are returned.
    """
    collected_files = []
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            # If no extensions specified, collect all files
            if not exts or any(filename.endswith(ext) for ext in exts):
                full_path = os.path.join(dirpath, filename)
                collected_files.append(full_path)
    return collected_files


def write_tree_and_files_to_text(files, output_file):
    """
    1) Write the directory tree to the output text file
    2) Then write each file's path and contents to the output text file
       with double lines of # as delimiters.
    """
    # Generate the directory tree lines
    tree_lines = generate_tree(root_directory)
    with open(output_file, "w", encoding="utf-8") as out:
        # Write the tree structure first
        out.write("DIRECTORY STRUCTURE:\n")
        out.write("----------------------------------------\n")
        for line in tree_lines:
            out.write(line + "\n")
        out.write("----------------------------------------\n\n")

        # Now write all file contents
        for file_path in files:
            base_name = os.path.basename(file_path)

            # START of file block
            out.write(
                "########################################################################################################################\n"
            )
            out.write(
                "########################################################################################################################\n"
            )
            out.write(f"START OF FILE: {base_name}\n")
            out.write(f"PATH: {file_path}\n")
            out.write(
                "########################################################################################################################\n"
            )
            out.write(
                "########################################################################################################################\n\n"
            )

            # File content
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                content = f"<Could not read file: {e}>"

            out.write(content)
            out.write("\n\n")


files = gather_files(root_directory, extensions)
write_tree_and_files_to_text(files, output_file)
print(f"Done! Files have been written to '{output_file}'.")
