# cli.py
"""
Parse argv, capture exceptions.
"""
from .core import VERSION, MATCHED_FILE_NAME, find_matched_file_paths
from argparse import ArgumentParser
from pathlib import Path



def main(argv:list[str]|None=None):
    help_msg = f'''
    --pattern-file, the file that contains the patterns, default as {MATCHED_FILE_NAME!r}. \n
    For example, the content is like `a/**/*.py`.
    '''
    argparser = ArgumentParser('my_cli')
    argparser.add_argument('-V', '--version', action='version', version=VERSION)
    argparser.add_argument('-v', '--verbose', action='store_true')
    argparser.add_argument('--pattern-file', help=help_msg, default=MATCHED_FILE_NAME)
    argparser.add_argument('--work-dir', default='.', help='default as \'.\'')

    args = argparser.parse_args(argv)
    file_path = Path(args.pattern_file)
    patterns = [line for line in file_path.read_text().splitlines() if line]

    for path in find_matched_file_paths(patterns, work_dir=Path(args.work_dir)):
        print(path)

    return 0
