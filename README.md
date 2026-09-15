# MyFind
MyFind finds files under a working directory whose relative paths match the given glob patterns.
It can be used as a CLI or as a Python library.

## Requirements
- Python3.10+

## Install
With `uv` in a project.
```bash
uv add myfind
```
Or install it into the current environment.
```bash
uv pip install myfind
```
If you are developing Myfind locally, use:
```bash
uv add .
# or
uv pip install -e .
```

## CLI Usage
```shell
uv run python -m myfind [--pattern-file <file-storing-the-patterns>] --work-dir <work-directory>
```

Options:
| Option | Default | Description |
| --- | --- | --- |
|`--pattern-file`|`<work-dir>/.patterns`|File containing glob patterns, one per line.|
|`--work-dir`|`.`| Root directory to search |
|`-v`, `--verbose`| off | Print each matched path to the log.|
|`-V`, `--version`| |Print version and exit.|


When `--pattern-file` is omitted, MyFind looks for `.patterns` inside `--work-dir`.
When given explicitly, the path is resolved relative to the current working directory.

Matched paths are printed one per line, relative to `--work-dir`.

Example output:
```text
a/index.html
a/css/style.css
a/js/app.js
```


## Pattern File Format
By default, MyFind reads patterns from `.patterns`.
- Each non-empty line is one glob pattern.
- Lines starting with # are comments.
- Patterns are matched against paths relative to `work_dir`.
- Use `/` as the path separator in patterns, even on Windows.
- `*` matches within one path segment.
- `**` matches across directories.
- `Path.glob` semantics apply: `*` and `**` do not match entries whose name starts with `.`.

Example `.patterns`:
```text
# Front-end assets
a/**/*.js
a/**/*.css
a/**/*.html
```
This matches `.js`, `.css` and `.html` files under `a/`.

## Python API
```python
from pathlib import Path
from myfind.core import find_matched_file_paths

paths = find_matched_file_paths(
        ["a/**/*.py", "a/**/*.css"], 
        work_dir=Path(".")
        )
for path in paths:
    print(path)

```
Function signature:
```python
from pathlib import Path
from typing import Iterable

def find_matched_file_paths(
    patterns: Iterable[str],
    *,
    work_dir: Path|None = None
    )-> list[str]:
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
```
## Behavior Notes
- Only files are returned; directories are not returned. 
- Symbolic links to files are followed and may be returned.
- If no files match, an empty list or empty output is returned.
<!-- - Invalid patterns raise `ValueError`. -->
- Empty lines and `#` comment lines in the pattern file are ignored.
- Hidden files and symbolic links follow the behavior of the underlying glob implementation.


## Development
```bash
uv sync 
uv run pytest
```

## LICENSE
MIT. See [LICENSE](LICENSE).

