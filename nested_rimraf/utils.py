import typer
import click_spinner

from typing import Callable, Optional, List
from pathlib import Path

DEFAULT_SAVE_FILE: str = '.nr-todo'


def raise_error(message):
    typer.secho(message, fg=typer.colors.RED)
    raise typer.Exit()


def process_directory(directory: Optional[str]) -> Path:
    if directory == '.' or directory is None:
        dir_path = Path().cwd()
    else:
        dir_path = Path(directory)
        if not dir_path.exists():
            raise_error(f"\"{directory}\" doesn't exist")
        elif not dir_path.is_dir():
            raise_error(f"\"{directory}\" is not a directory")

    return dir_path


def get_matches(target: str, dir_path: Path, dir_only: bool, no_symlinks: bool) -> List[Path]:
    matches = []

    with click_spinner.spinner():
        matches += list(dir_path.glob(f'**/{target}'))

        if dir_only:
            directory_filter: Callable[[Path], bool] = lambda x: x.is_dir()
            matches = filter(directory_filter, matches)

        if no_symlinks:
            no_symlink_filter: Callable[[Path], bool] = lambda x: not x.is_symlink()
            matches = filter(no_symlink_filter, matches)

    return list(matches)


def report_matches(
    matches: List[Path],
    target: Optional[str],
    dir_path: Optional[Path],
    dir_only: bool,
    no_symlinks: bool
):
    if len(matches) == 0 and target:
        typer.secho(f'Congrats! There are no "{target}"s inside "{dir_path}"', fg=typer.colors.GREEN)
        raise typer.Abort()

    prefix = 'Files and directories'
    if dir_only:
        prefix = 'Directories'

    if no_symlinks:
        prefix += ' (exclude symlinks)'
    else:
        prefix += ' (include symlinks)'
    prefix += ':'

    typer.secho(prefix, bold=True)
    for match in matches:
        typer.echo(f'\t→ {match}')
