from pathlib import Path
import shutil
import exiftool
import sys



def read_meta_data(file):
    with exiftool.ExifToolHelper() as et:
        complete_metadata = et.get_metadata(str(file))
        return complete_metadata[0]


def create_path_and_copy(file, target_path, condensed_metadata):
    if condensed_metadata["FileType"] == "JPEG":
        path = Path(str(target_path) + "/Photos" + "/" +
                    condensed_metadata["Date"] + "/" + condensed_metadata["CameraModel"] + "/" + "JPEG")
        path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(file), str(path))

    if condensed_metadata["FileType"] == "DNG":
        path = Path(str(target_path) + "/Photos" + "/" +
                    condensed_metadata["Date"] + "/" + condensed_metadata["CameraModel"] + "/" + "DNG")
        path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(file), str(path))

    if condensed_metadata["FileType"] == "RAF":
        path = Path(str(target_path) + "/Photos" + "/" +
                    condensed_metadata["Date"] + "/" + condensed_metadata["CameraModel"] + "/" + "RAW")
        path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(file), str(path))

    if condensed_metadata["FileType"] == "MOV" or condensed_metadata["FileType"] == "MP4":
        path = Path(str(target_path) + "/Videos" + "/" +
                    condensed_metadata["Date"] + "/" + condensed_metadata["CameraModel"])
        path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(file), str(path))


path_choice = ""
unknown_input = True

while unknown_input == True:

    source_path = Path(f"{sys.argv[1]}")
    target_path = Path(f"{sys.argv[2]}")

    print(f"""
        Standard source path: {source_path}
        Standard target path: {target_path}
        """)
    path_choice = input(
        "Do you want to use the Standard paths (S) or custom paths (C) or enter the values again (A):")

    if path_choice == "C" or path_choice == "c":
        print("Remember to add a '/' at the end of your custom path!")
        source_path = Path(input("Custom Source Path: "))
        target_path = Path(input("Custom Target Path: "))
        unknown_input = False
    elif path_choice == "S" or path_choice == "s":
        unknown_input = False
    elif path_choice == "A" or path_choice == "a":
        unknown_input = True
    else:
        print("Please select either 'S' for standard path or 'C' for custom path")
        unknown_input = True

for file in source_path.rglob("*"):
    print(str(file))
    condensed_metadata = {}
    orig_extension = file.suffix
    orig_name = file.stem
    if file.suffix == ".JPG" or file.suffix == ".RAF" or file.suffix == ".MOV" or file.suffix == ".DNG":
        condensed_metadata = {
            "CameraModel": read_meta_data(file)["EXIF:Model"],
            "Date": str(read_meta_data(file)["EXIF:DateTimeOriginal"])[0:10].replace(":", "-"),
            "Time": str(read_meta_data(file)["EXIF:DateTimeOriginal"])[11:],
            "FileType": read_meta_data(file)["File:FileType"],
            "FileName": read_meta_data(file)["File:FileName"]}
        create_path_and_copy(file, target_path, condensed_metadata)

    if file.suffix == ".MP4" or file.suffix == ".360":
        condensed_metadata = {
            "CameraModel": read_meta_data(file)["QuickTime:Model"],
            "Date": str(read_meta_data(file)["QuickTime:CreateDate"])[0:10].replace(":", "-"),
            "Time": str(read_meta_data(file)["QuickTime:CreateDate"])[11:],
            "FileType": read_meta_data(file)["File:FileType"],
            "FileName": read_meta_data(file)["File:FileName"]}
        create_path_and_copy(file, target_path, condensed_metadata)
