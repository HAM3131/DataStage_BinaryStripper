# StripDSX
# Purpose: Program to strip compiled segment from DataStage `.dsx` files
# Author: Henry Manning
# Version: 1.0

import argparse
import os

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def strip_file(args):
    # Alias args
    path = args.filename
    delimiter = args.delimiter
    strip_file = args.force

    # Ensure file exists
    if os.path.isfile(path):
        is_dsx = path.split('.')[-1] == 'dsx'
        if not is_dsx:
            return
        
        if not strip_file:
            strip_file = query_yes_no(f'Strip `{path}`?')

        # Take file contents
        with open(path, 'r') as f:
            file_contents = f.read()

        # If file contains delimiter, remove everything after the first instance
        if delimiter in file_contents:
            with open(path, 'w') as f:
                f.write(file_contents.split(delimiter)[0])

    else:
        print(f'{path} is not a file. Use `-r` to use recursive mode')

def strip_dir(args):
    # Alias args
    path = args.filename
    strip = args.force

    # Ensure directory exists
    if os.path.isdir(path):
        # Recurse through files and subdirectories
        for x in os.listdir(path):
            # Calculate new path
            subpath = os.path.join(path, x)
            args.filename = subpath

            # Strip files
            if os.path.isfile(subpath):
                strip_file(args)

            # Strip subdirectories
            elif os.path.isdir(subpath):
                if not strip:
                    strip = query_yes_no(f'Strip files in `{subpath}`?')
                
                if strip:
                    strip_dir(args)
    else:
        print(f'{path} is not a directory')

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
    
    parser.add_argument('-f',
                        '--force',
                        action='store_true',
                        dest='force',
                        help='Set this flag to force all changes and ignore confirmation messages')
    
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

    print(args)
    # Strip based on arguments
    try:
        if args.recursive:
            strip_dir(args)
        else:
            strip_file(args)
    except:
        # Return a failure if there was an exception
        print('unknown error')
        status = 1

    return status

if __name__ == '__main__':
    main()