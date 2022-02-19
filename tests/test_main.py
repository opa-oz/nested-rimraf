import subprocess

from pathlib import Path
from typer.testing import CliRunner
from nested_rimraf.main import app
from nested_rimraf.utils import DEFAULT_SAVE_FILE

runner = CliRunner()


def update_subject():
    process = subprocess.Popen("make fill", shell=True, stdout=subprocess.PIPE)
    process.wait()


# region "scan"
def test_scan_default():
    output = ['Files and directories (include symlinks):',
              '→ subject/node_modules',
              '→ subject/symlink/node_modules',
              '→ subject/file/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules', ]
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])


def test_scan_only_directories():
    output = ['Directories (include symlinks):',
              '→ subject/node_modules',
              '→ subject/symlink/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules', ]
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--dir-only'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])

    result = runner.invoke(app, ['scan', '-d', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])


def test_scan_without_symlinks():
    output = ['Files and directories (exclude symlinks):',
              '→ subject/node_modules',
              '→ subject/file/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules']
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--without-symlinks'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])

    result = runner.invoke(app, ['scan', '-s', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])


def test_scan_only_directories_without_symlinks():
    output = ['Directories (exclude symlinks):',
              '→ subject/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules']
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--without-symlinks', '--dir-only'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])

    result = runner.invoke(app, ['scan', '-ds', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])


def test_save_to_default_file():
    output = 'Successfully saved list to ".nr-todo"'
    file = [
        'subject/node_modules',
        'subject/symlink/node_modules',
        'subject/file/node_modules',
        'subject/sub/node_modules',
        'subject/sub/3/node_modules',
        'subject/sub/2/1/4/node_modules',
        'subject/sub2/node_modules',
    ]
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--save-list'])

    assert result.exit_code == 0
    assert output in result.stdout

    result = runner.invoke(app, ['scan', '-L', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert output in result.stdout

    path_to_file = Path(f'./{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    with open(path_to_file, 'r') as f:
        text = f.read()

    assert all([f in text for f in file])


def test_save_to_custom_file():
    output = 'Successfully saved list to "subject/.nr-todo"'
    file = [
        'subject/node_modules',
        'subject/symlink/node_modules',
        'subject/file/node_modules',
        'subject/sub/node_modules',
        'subject/sub/3/node_modules',
        'subject/sub/2/1/4/node_modules',
        'subject/sub2/node_modules',
    ]
    update_subject()
    result = runner.invoke(app,
                           ['scan', 'node_modules', './subject', '--save-list', '--save-path', './subject/.nr-todo'])

    assert result.exit_code == 0
    assert output in result.stdout
    path_to_file = Path(f'./subject/{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    result = runner.invoke(app, ['scan', '-L', 'node_modules', './subject', '--save-path', './subject/.nr-todo'])

    assert result.exit_code == 0
    assert output in result.stdout

    path_to_file = Path(f'./subject/{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    with open(path_to_file, 'r') as f:
        text = f.read()

    assert all([f in text for f in file])


def test_save_to_custom_directory():
    output = 'Successfully saved list to "subject/.nr-todo"'
    file = [
        'subject/node_modules',
        'subject/symlink/node_modules',
        'subject/file/node_modules',
        'subject/sub/node_modules',
        'subject/sub/3/node_modules',
        'subject/sub/2/1/4/node_modules',
        'subject/sub2/node_modules',
    ]
    update_subject()
    result = runner.invoke(app,
                           ['scan', 'node_modules', './subject', '--save-list', '--save-path', './subject'])

    assert result.exit_code == 0
    assert output in result.stdout
    path_to_file = Path(f'./subject/{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    result = runner.invoke(app, ['scan', '-L', 'node_modules', './subject', '--save-path', './subject'])

    assert result.exit_code == 0
    assert output in result.stdout

    path_to_file = Path(f'./subject/{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    with open(path_to_file, 'r') as f:
        text = f.read()

    assert all([f in text for f in file])


# endregion

# region "rm"
def test_rm_default():
    output = ['Files and directories (include symlinks):',
              '→ subject/node_modules',
              '→ subject/symlink/node_modules',
              '→ subject/file/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules', ]
    update_subject()
    result = runner.invoke(app, ['rm', '-y', 'node_modules', './subject'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])
    assert 'Done flawlessly!' in result.stdout

    result = runner.invoke(app, ['scan', 'node_modules', './subject'])
    assert result.exit_code == 1
    assert 'Congrats' in result.stdout


def test_rm_only_directories():
    output = ['Directories (include symlinks):',
              '→ subject/node_modules',
              '→ subject/symlink/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules', ]
    update_subject()
    result = runner.invoke(app, ['rm', '-y', 'node_modules', './subject', '--dir-only'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])
    assert 'Done flawlessly!' in result.stdout

    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--dir-only'])
    assert result.exit_code == 1
    assert 'Congrats' in result.stdout


def test_rm_without_symlinks():
    output = ['Files and directories (exclude symlinks):',
              '→ subject/node_modules',
              '→ subject/file/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules']
    update_subject()
    result = runner.invoke(app, ['rm', '-y', 'node_modules', './subject', '--without-symlinks'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])
    assert 'Done flawlessly!' in result.stdout

    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--without-symlinks'])
    assert result.exit_code == 1
    assert 'Congrats' in result.stdout


def test_rm_only_directories_without_symlinks():
    output = ['Directories (exclude symlinks):',
              '→ subject/node_modules',
              '→ subject/sub/node_modules',
              '→ subject/sub/3/node_modules',
              '→ subject/sub/2/1/4/node_modules',
              '→ subject/sub2/node_modules']
    update_subject()
    result = runner.invoke(app, ['rm', '-y', 'node_modules', './subject', '--without-symlinks', '--dir-only'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in output])
    assert 'Done flawlessly!' in result.stdout

    result = runner.invoke(app, ['scan', '-ds', 'node_modules', './subject'])
    assert result.exit_code == 1
    assert 'Congrats' in result.stdout


# endregion

def test_remove_from_default_file():
    output = 'Successfully saved list to ".nr-todo"'
    file = [
        'subject/node_modules',
        'subject/symlink/node_modules',
        'subject/file/node_modules',
        'subject/sub/node_modules',
        'subject/sub/3/node_modules',
        'subject/sub/2/1/4/node_modules',
        'subject/sub2/node_modules',
    ]
    update_subject()
    result = runner.invoke(app, ['scan', 'node_modules', './subject', '--save-list'])

    assert result.exit_code == 0
    assert output in result.stdout

    path_to_file = Path(f'./{DEFAULT_SAVE_FILE}')
    assert path_to_file.is_file()

    with open(path_to_file, 'r') as f:
        text = f.read()

    assert all([f in text for f in file])

    result = runner.invoke(app, ['rmf', '-y'])

    assert result.exit_code == 0
    assert all([p in result.stdout for p in file])
    assert 'Done flawlessly!' in result.stdout

    result = runner.invoke(app, ['scan', 'node_modules', './subject'])
    assert result.exit_code == 1
    assert 'Congrats' in result.stdout
