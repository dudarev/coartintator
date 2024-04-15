"""
This Python script is designed to traverse a directory structure, 
find all Python files, 
and combine their contents into a single text file.
"""

import os
from pathlib import Path

DIR = Path(__file__).parent.parent / "coartintator"


def combine_files(start_dir) -> str:
    print(f"Combining files in {start_dir}")
    combined_text = ""
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file)) as infile:
                    relative_path = os.path.relpath(
                        os.path.join(root, file), start=str(DIR.parent)
                    )
                    combined_text += f"# File: {relative_path}\n"
                    combined_text += infile.read()
                    combined_text += "\n\n"
        for dir in dirs:
            combined_text += combine_files(os.path.join(root, dir))
    return combined_text


combined_text = combine_files(DIR)

with open("combined.txt", "w") as f:
    f.write(combined_text)
