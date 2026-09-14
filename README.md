# MyFind
According the given pattern, match the relative file paths that content the patterns.

## Install
```shell
uv add myfind
uv pip install myfind
```

## Usage
```shell
uv run python -m myfind --pattern-file <file-storing-the-patterns> --work-dir <work-directory>
```

The it will print the matched files.

Moreover, the way to use this package is more likely to embed it into the python codes.
```python
from myfind.core import find_matched_file_paths

```

Below is about the definition of the function:
```python
def find_matched_file_paths(patterns:Iterable[str]=MATCHED_FILE_NAME, 
                           *, 
                           work_dir:Path|None=None
                           )->list[str]:
    """
    patterns: list of patterns, if recursive, use `**`.
    work_dir: `Path` of the root directory.
    """
```

## LICENSE
MIT. See [LICENSE](LICENSE).

