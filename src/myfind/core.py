# core.py
"""
From a selected root and the rules, return a list of relative file paths.
"""
from ._meta import *
from pathlib import Path
import logging
from collections.abc import Iterable


logger = logging.getLogger(__name__)


def find_matched_file_paths(patterns:Iterable[str], 
                           *, 
                           work_dir:Path|None=None
                           )->list[str]:
    """
    patterns: list of patterns, if recursive, use `**`.
    work_dir: `Path` of the root directory.
    """
    if work_dir is None:
        work_dir = Path.cwd()

    if not work_dir.exists():
        logger.warning("Path '%s' doesn't exists.", work_dir)
        return []

    matched_file_paths = []
    for pattern in patterns:
        for path in work_dir.glob(pattern):
            # logger.info("%s matched", path)
            matched_file_paths.append(str(path.relative_to(work_dir)))

    return matched_file_paths
