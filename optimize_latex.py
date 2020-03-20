"""
Top level program which parses a latex project directory and makes optimisations in place
"""
import argparse
import os
from glob import glob
import json

from tools import imgProcess as imgProc
from tools import texProcess as texProc

# Files we can optimise:
OPTIMISABLE_IMAGES = ['.png', '.jpg', '.jpeg']
OPTIMISABLE_FILES = ['.tex']

def read_config(config_path):
    """
    Reads the config json file

    @param config_path: path to the config json file
    @returns config parameters as a dictionary
    """
    with open(config_path, 'r') as fp:
        config_dict = json.load(fp)
    return config_dict

def list_files(dir_path):
    """
    Returns a list of files' full paths in a directory tree

    @param dir_path: path to the directory to parse
    """
    file_list = os.listdir(dir_path)
    all_files = []

    for f in file_list:
        file_path = os.path.join(dir_path, f)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(file_path):
            all_files = all_files + list_files(file_path)
        else:
            all_files.append(file_path)
                
    return all_files

def optimise_image(image_path, config):
    """
    Applies image optimisations based on config

    @param image_path: the path to the image file
    @param config: the config parameters for this file
    """
    file_size = os.path.getsize(image_path)
    if config['compress_images'] or config['resize_images']:
        img = imgProc.load_image(image_path)
        if config['resize_images']:
            img = imgProc.resize(img, config['largest_size'], config['image_resize_dimension'])
        
        if config['compress_images']:
            imgProc.save_compressed(img, image_path, 
                                    quality=config['compression_quality'], 
                                    optimize=config['optimize_compression'])
        else: # override quality to 100%
            imgProc.save_compressed(img, image_path, 
                                    quality=100,
                                    optimize=config['optimize_compression'])
    
    print("Original file size (mb):", file_size / 1000000)
    new_size = os.path.getsize(image_path)
    print("Optimised file size (mb):", new_size / 1000000)

    return file_size - new_size

def optimise_file(file_path, config):
    """
    Applies file optimisations based on config

    @param file_path: the path to the text file
    @param config: the config parameters for this file
    """
    if config['remove_comments']:
        file_lines = texProc.load_file_lines(file_path)
        clean_lines = texProc.comment_cleaner(file_lines)
        texProc.save_file_lines(clean_lines, file_path)

def match_filename(referenced_files, file_path):
    """
    Attemps to see if the file_path or name is in the referenced files
    """
    for rf in referenced_files:
        if os.path.basename(file_path) in rf:
            return True

    return False
 
def folder_parser(tex_dir, config):
    """
    Parses each file in latex project directory and applies optimisations in place.

    @param config: config parameters as a dictionary
    @param tex_dir: path to the directory to parse
    """
    all_files = list_files(tex_dir)
    referenced_files = []
    bytes_saved = 0

    for file_path in all_files:
        ext = os.path.splitext(file_path)[-1]

        # If it is a tex file track the referenced files
        if ext == '.tex':
            file_lines = texProc.load_file_lines(file_path)
            referenced_files.extend(texProc.get_referenced_files(file_lines))

        if ext in config["ignore_filetypes"]:
            print("Skipping based on filetype:", file_path)
            continue

        if file_path in config["ignore_files"] or os.path.basename(file_path) in config["ignore_files"]:
            print("Skipping based on specific filename:", file_path)
            continue
        
        if file_path in config["special_cases"].keys():
            print("Applying file specific parameters:", file_path)
            file_optimisation_parameters = config["special_cases"][file_path]

        elif os.path.basename(file_path) in config["special_cases"].keys():
            print("Applying file specific parameters:", file_path)
            file_optimisation_parameters = config["special_cases"][os.path.basename(file_path)]
        
        else:
            # Same keys exist at the top level so just pass config
            file_optimisation_parameters = config
        
        # If image we can process file as an image
        if ext.lower() in OPTIMISABLE_IMAGES:
            print("Optimising image file:", file_path)
            reduction_in_filesize = optimise_image(file_path, file_optimisation_parameters)
            bytes_saved += reduction_in_filesize
        
        # If file we can process process as a file
        elif ext.lower() in OPTIMISABLE_FILES:
            print("Optimising text file:", file_path)
            optimise_file(file_path, file_optimisation_parameters)

        # else ignore the file
        else:
            print("Skipping unknown file/filetype:", file_path)

        # Add blank space between files
        print('\n')
    
    print("\n\nChecking for unused files")
    # Second pass through project to check on missing files
    unused_files = 0
    unused_images = []
    for file_path in all_files:
        if not match_filename(referenced_files, file_path):
            print(file_path)
            unused_files += 1
            if file_path.endswith('.png') or file_path.endswith('.jpg'):
                unused_images.append(file_path)
    
    print("Done.")
    print(unused_files, "potentially unused files.")
    print(bytes_saved / 1000000, "Mb saved by optimising images.")

    choice = input("Warning IRREVERSIBLE: Remove potentially unused image files ('.png' and '.jpg')?\n'y' or 'n': ")
    if choice == 'y':
        for file_path in unused_images:
            os.remove(file_path)

# =========================================================================
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex_dir", type=str, help="Path to the directory of the latex project", required=True)
    parser.add_argument("--config", type=str, help="Path to the optimisation parameters", required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    config = read_config(args.config)
    folder_parser(args.tex_dir, config)
