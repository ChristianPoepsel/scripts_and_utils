import exiftool
from pathlib import Path


def read_meta_data(file):
    #    with file.open('rb') as f:
    #        tags = exifread.process_file(f, details=False)
    #    return tags
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(str(file))
        return metadata


path = Path('./example_files')

for file in path.rglob("*"):

    dict = read_meta_data(file)
    # Iterate over key/value pairs in dict and print them
    for key, value in dict.items():
        print(key, ':', value)
