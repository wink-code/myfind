# cli.py
"""
Parse argv, capture exceptions.
"""
from .core import VERSION, MATCHED_FILE_NAME, find_matched_file_paths
from argparse import ArgumentParser
from pathlib import Path
import logging
import sys



def main(argv:list[str]|None=None):
    help_msg = f'''
    --pattern-file, the file that contains the patterns, default as {MATCHED_FILE_NAME!r}. \n
    For example, the content is like `a/**/*.py`.
    '''
    argparser = ArgumentParser('my_cli')
    argparser.add_argument('-V', '--version', action='version', version=VERSION)
    argparser.add_argument('-v', '--verbose', action='store_true')
    argparser.add_argument('--pattern-file', help=help_msg)
    argparser.add_argument('--work-dir', type=Path, default=Path('.'), help='default as \'.\'')
    
    args = argparser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if args.pattern_file is None:
        args.pattern_file = args.work_dir / MATCHED_FILE_NAME

    file_path = Path(args.pattern_file)
    try:
        content = file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"pattern file not found: {file_path}.")
        return 2
    except OSError as e:
        print(f"cannot read pattern file {file_path}: {e}", file=sys.stderr)
        return 2
    
    patterns = [line for line in content.splitlines() 
                if line and not line.startswith('#')
                ]
    try:
        for path in find_matched_file_paths(patterns, work_dir=args.work_dir):
            print(path)
    except NotADirectoryError as e:
        print(f"--work-dir is expected to be a Directory, get {args.work_dir}.")
        return 1

    return 0
