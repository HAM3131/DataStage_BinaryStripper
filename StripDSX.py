# StripDSX
# Purpose: Program to strip compiled segment from DataStage `.dsx` files
# Author: Henry Manning
# Version: 1.0

import argparse
import os

def strip_file(path, delimiter):
    # Ensure file exists
    if os.path.isfile(path):
        # Take file contents
        with open(path, 'r') as f:
            file_contents = f.read()

        # If file contains delimiter, remove everything after the first instance
        if delimiter in file_contents:
            with open(path, 'w') as f:
                f.write(file_contents.split(delimiter)[0])

    else:
        print(f'{path} is not a file')

def strip_dir(path, delimiter):
    # Ensure directory exists
    if os.path.isdir(path):
        # Recurse through files and subdirectories
        for x in os.listdir(path):
            # Calculate new path
            subpath = os.path.join(path, x)

            # Strip files
            if os.path.isfile(subpath):
                strip_file(subpath, delimiter)

            # Strip subdirectories
            elif os.path.isdir(os.path.join(subpath, x)):
                strip_dir(subpath, delimiter)
    else:
        print(f'{path} is not a directory. Use `-r` to use recursive mode')

def parse_args():
    # Define the argparser
    parser = argparse.ArgumentParser(
                    prog='StripDSX',
                    description='This program strips the compiled section of a DataStage `.dsx` file.',
                    epilog='Contact Henry Manning for suggestions. [henry_manning@cinfin.com]')
    
    # Add arguments to the parser
    parser.add_argument('-r',
                        '--recursive',
                        action='store_true',
                        dest='recursive',
                        help='Set this flag to strip directories and their contents recursively')
    
    parser.add_argument('-d',
                        '--delimiter',
                        dest='delimiter',
                        default='BEGIN DSEXECJOB',
                        type=str,
                        help='Everything after the first instance of the delimiter in a target file will be removed')
    
    parser.add_argument('filename',
                        type=str,
                        help='The path of the file to target')

    # Parse
    parsed_args = parser.parse_args()
    
    return parsed_args

def main():
    status = 0

    # Parse command line arguments
    args = parse_args()

    # Strip based on arguments
    try:
        if args.recursive:
            strip_dir(args.filename, args.delimiter)
        else:
            strip_file(args.filename, args.delimiter)
    except:
        # Return a failure if there was an exception
        status = 1

    return status

if __name__ == '__main__':
    main()