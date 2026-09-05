#!/bin/env python3
# licenseadder - A program for adding license text to project sourcecode
# Copyright (C) 2026 Johan Henriksson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.
#

import argparse
import sys
import os
import glob
import shutil
from datetime import datetime


# C/C++ source and header file extensions
TARGET_EXTENSIONS = {".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"}

def load_license_template(template_path, params) -> str:
    """Reads a license header template file and substitutes dynamic variables."""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            raw_template = f.read()
    except Exception as e:
        print(f"Error reading template file '{template_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Perform placeholders substitution
    formatted_template = raw_template.format(**params)

    # Ensure the header is properly wrapped in a C block comment if not already
    header = formatted_template.strip()
    if not header.startswith("/*"):
        header = f"/*\n{header}"
    if not header.endswith("*/"):
        header = f"{header}\n */"

    return header + "\n"



def add_license_header(file_path: str, header_text: str) -> None:
    """Prepends the license header to the file if it doesn't already contain it."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"[SKIP] Could not read non-UTF-8 file: {file_path}")
        return
    except Exception as e:
        print(f"[SKIP] Could not read file {file_path}: {e}")
        return

    # Check for existing license mention to avoid double insertion
    if "Copyright" in content:
        print(f"[EXISTS] License already present in {file_path}")
        return

    # Prepend header to existing content
    new_content = header_text + ("\n" if content else "") + content
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[ADDED] License header added to {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not write to file {file_path}: {e}")

def process_directory(directory: str, header_text: str) -> None:
    """Recursively processes all C/C++ files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in TARGET_EXTENSIONS:
                file_path = os.path.join(root, file)
                add_license_header(file_path, header_text)

def get_license_list():
    files = glob.glob(f"licenses/*-header.txt")
    name_list = [  ]
    for file in files:
        name = file[len("licenses/"):-len("-header.txt")]
        name_list += [ name ]
    
    return sorted(name_list)

def copy_license_file(src_path, dst_path, params):
    """Copy a license file and substitute words in it"""
    
    try:
        with open(src_path, "r", encoding="utf-8") as f:
            raw_template = f.read()
    except Exception as e:
        print(f"Error reading file '{src_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Perform placeholders substitution
    formatted_template = raw_template.format(**params)
    
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(formatted_template)



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively prepend LGPL-3.0 license header to C/C++ source and header files."
    )
    parser.add_argument(
        "-p", "--project", required=True, help="Name of the project"
    )
    parser.add_argument(
        "-d", "--dir", required=True, help="Target directory to scan"
    )
    parser.add_argument(
        "-a", "--author", required=True, help="Name of the developer/author"
    )
    license_list_text = ','.join(get_license_list())
    parser.add_argument(
        "-l", "--license", required=True, help=f"The name of the license ({license_list_text})"
    )
    parser.add_argument(
        "-n", "--name", default="This program", help="The name of the program"
    )
    parser.add_argument(
        "--program-desc", default="", help="A short description of what the program does"
    )

    args = parser.parse_args()

    params = {}
    params["project"]  = args.project
    params["year"]  = str(datetime.now().year)
    params["author_name"]  = args.author
    params["program_name"]  = args.name
    params["program_desc"]  = args.program_desc
    
    # Get the license header file
    license_name = args.license.lower()
    if license_name not in get_license_list():
        print(f"Error: Unknown license '{args.license}'")
        sys.exit(1)
    template = f"licenses/{license_name}-header.txt"
    
    if not os.path.exists(args.dir) or not os.path.isdir(args.dir):
        print(f"Error: The directory path '{args.dir}' is not valid.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(template) or not os.path.isfile(template):
        print(f"Error: The template path '{template}' is not a valid file.", file=sys.stderr)
        sys.exit(1)

    # 
    files = glob.glob(f"licenses/{license_name}-file-*")
    for src_file in files:
        dst_file = args.dir + "/" + src_file[len(f"licenses/{license_name}-file-"):]
        print(f"Copying {src_file} to {dst_file}")
        if os.path.exists(dst_file):
            print(f"[EXISTS] File '{dst_file}' already exists. Skipping copy.")
        else:
            copy_license_file(src_file, dst_file, params)

    header_text = load_license_template(template, params)
    process_directory(args.dir, header_text)

if __name__ == "__main__":
    main()
    
