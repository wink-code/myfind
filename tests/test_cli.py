from myfind.cli import main
from pytest import fixture


@fixture
def tree(tmp_path):
    work_dir = tmp_path
    (apple := work_dir / "apple").mkdir(exist_ok=True)
    (banana := work_dir / "banana").mkdir(exist_ok=True)
    sub = work_dir / "orange" / "subfolder"
    sub.mkdir(exist_ok=True, parents=True)

    pattern_path = work_dir / '.patterns'
    patterns = ['*.py', '*.js', '*.css', '*.html', 'apple/*']
    pattern_path.write_text('\n'.join(patterns))

    c = ['.html', '.css', '.js']
    for i in range(3):
        (apple / f'file{i}').write_text(f'a{i}')
        (banana / f'file{i}.py' if i % 2 == 0 else banana / f'file{i}.other').write_text(f'b{i}')
        (sub / ('file'+ c[i])).write_text(f'o{i}')
    return tmp_path

def test_cli(tree, monkeypatch, capsys):
    monkeypatch.chdir(tree)

    exit_code = main([
        '--pattern-file=.patterns',
        '--work-dir=.']
         )
    # from pathlib import Path
    # print(Path('.patterns').read_text())
    # print(list(Path.cwd().iterdir()))
    assert exit_code == 0
    # assert set(file_list) == {'apple/file0', 'apple/file1', 'apple/file2',
    #                      'banana/file0.py', 'banana/file2.py',
    #                   'orange/subfolder/file.html', 'orange/subfolder/file.css', 'orange/subfolder/file.js'}
    out = capsys.readouterr().out
    assert set(out.splitlines()) ==  {'apple/file0', 'apple/file1', 'apple/file2',
                         'banana/file0.py', 'banana/file2.py',
                      'orange/subfolder/file.html', 'orange/subfolder/file.css', 'orange/subfolder/file.js'}
 
