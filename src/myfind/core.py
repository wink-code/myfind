# core.py
"""
From a selected root and the rules, return a list of relative file paths.
"""
from ._meta import VERSION, MATCHED_FILE_NAME
from pathlib import Path
import logging
from collections.abc import Iterable


logger = logging.getLogger(__name__)


def find_matched_file_paths(patterns:Iterable[str], 
                           *, 
                           work_dir:Path|None=None
                           )->list[str]:
    """
    Return file paths matching the given glob patterns.

    Args:
        patterns: Glob patterns. Use `**` for recursive matching.
        work_dir: Root directory to saerch. Defaults to the current working directory.

    Returns:
        Sorted, de-duplicated file paths relative to `work_dir`,
        using POSIX separators. Only regular files (including symlinks to files)
        are returned. Returns an empty list if `work_dir` does no exist.
    """
    if work_dir is None:
        work_dir = Path.cwd()

    if not work_dir.exists():
        logger.warning("Path '%s' doesn't exists.", work_dir)
        return []

    if not work_dir.is_dir():
        raise NotADirectoryError(f"work_dir is not a directory: {work_dir}.")

    matched:set[str] = set()
    for pattern in patterns:
        for path in work_dir.glob(pattern):
            if path.is_file():
                logger.info("%s matched", path)
                matched.add(path.relative_to(work_dir).as_posix())

    return sorted(matched)
