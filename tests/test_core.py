from myfind import core
import pytest


def test_find_matched_paths(tmp_path):
    PATTERNS = ['apple/*', 'banana/*.py', 'orange/**/*.html', 'orange/**/*.css', 'orange/**/*.js']
    work_dir = tmp_path
    (apple := work_dir / "apple").mkdir(exist_ok=True)
    (banana := work_dir / "banana").mkdir(exist_ok=True)
    sub = work_dir / "orange" / "subfolder"
    sub.mkdir(exist_ok=True, parents=True)

    c = ['.html', '.css', '.js']
    for i in range(3):
        (apple / f'file{i}').write_text(f'a{i}')
        (banana / f'file{i}.py' if i % 2 == 0 else banana / f'file{i}.other').write_text(f'b{i}')
        (sub / ('file'+ c[i])).write_text(f'o{i}')


    result = core.find_matched_file_paths(PATTERNS,
                                work_dir=tmp_path,
                                )
    assert set(result) == {'apple/file0', 'apple/file1', 'apple/file2',
                         'banana/file0.py', 'banana/file2.py',
                      'orange/subfolder/file.html', 'orange/subfolder/file.css', 'orange/subfolder/file.js'}

@pytest.fixture
def tree(tmp_path):
    work_dir = tmp_path
    (apple := work_dir / "apple").mkdir(exist_ok=True)
    (banana := work_dir / "banana").mkdir(exist_ok=True)
    sub = work_dir / "orange" / "subfolder"
    sub.mkdir(exist_ok=True, parents=True)

    c = ['.html', '.css', '.js']
    for i in range(3):
        (apple / f'file{i}').write_text(f'a{i}')
        (banana / f'file{i}.py' if i % 2 == 0 else banana / f'file{i}.other').write_text(f'b{i}')
        (sub / ('file'+ c[i])).write_text(f'o{i}')
    return tmp_path

@pytest.mark.parametrize("pattern, expected", [
    ('apple/*',     {'apple/file0', 'apple/file1', 'apple/file2'}), 
    ('banana/*.py', {'banana/file0.py', 'banana/file2.py'}),
    ('orange/**/*.html', {'orange/subfolder/file.html'}),
    ('orange/**/*.css',  {'orange/subfolder/file.css'}),
    ('orange/**/*.js',   {'orange/subfolder/file.js'}),
    ])
def test_each_pattern(tree, pattern, expected):
    result = core.find_matched_file_paths(
            [pattern], work_dir=tree)
    assert set(result) == expected
