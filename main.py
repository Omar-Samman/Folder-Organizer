from pathlib import Path
import os

Categories = {
    ".jpg": "Images",
    ".png": "Images",
    ".jpeg": "Images",

    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",

    ".mp3": "Music",
    ".wav": "Music",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",

    ".zip": "Compressed",
    ".rar": "Compressed",

    ".c": "Code",
    ".cpp": "Code",
    ".py": "Code",
    ".js": "Code",
    ".java": "Code",
    ".css": "Code",
    ".dart": "Code",
}

# print("" \
# "put the path" \
# "")
# fullFilePath = input()
# file_ext = Path(fullFilePath).suffix.lower()
# category = Categories.get(file_ext,"Other")
# print(category)

print("\n\nput the folder path here\n\n")

inputpath = input()
print("You entered : ", inputpath)

targetFolder = Path(inputpath)

if not targetFolder.exists() or not targetFolder.is_dir():
    print("wrong path")
else:
    print("Folder is correct!")

    for item in targetFolder.iterdir():

        if item.is_file():

            file_ext = item.suffix.lower()
            category = Categories.get(file_ext, "Other")

            category_folder = targetFolder / category

            if not category_folder.exists():
                category_folder.mkdir()

            des = category_folder / item.name

            item.rename(des)