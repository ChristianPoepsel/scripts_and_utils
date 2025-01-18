import os
import argparse


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
        is_last_item = index == len(items) - 1
        connector = "└── " if is_last_item else "├── "

        if os.path.isdir(path):
            lines.append(prefix + connector + item + "/")
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
            if not exts:  # If no extensions specified, collect all files
                collected_files.append(os.path.join(dirpath, filename))
            else:
                # Otherwise, only collect if extension matches
                if any(filename.endswith(ext) for ext in exts):
                    full_path = os.path.join(dirpath, filename)
                    collected_files.append(full_path)
    return collected_files


def write_tree_and_files_to_text(root_directory, files, output_file):
    """
    1) Write the directory tree to the output text file
    2) Then write each file's path and contents to the output text file
       with double lines of # as delimiters.
    """
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

    print(f"Done! Files have been written to '{output_file}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a directory tree of specified root directory and gather the contents of files matching given extensions."
    )
    # Positional argument for the root directory
    parser.add_argument(
        "root_directory",
        nargs="?",
        help="Path to the root directory.",
    )
    # Optional argument for extensions
    parser.add_argument(
        "--extensions",
        default=".dart",
        help="Space-separated extensions with leading dot (e.g. '.py .dart'). Defaults to '.dart'.",
    )
    # Optional argument for the output file
    parser.add_argument(
        "--output",
        default="context.txt",
        help="Name of the output text file. Defaults to 'context.txt'.",
    )

    args = parser.parse_args()

    # Split extension string if provided
    exts = args.extensions.split() if args.extensions else []

    files = gather_files(args.root_directory, exts)
    write_tree_and_files_to_text(args.root_directory, files, args.output)


if __name__ == "__main__":
    main()
