import typer
import click_spinner
import shutil

from pathlib import Path
from typing import Optional, List
from .utils import get_matches, process_directory, report_matches, raise_error, DEFAULT_SAVE_FILE


def remove_in_directory(
    target: str,
    directory: Optional[str],
    dir_only: bool,
    no_symlinks: bool,
    agree: bool,
    ignore_errors: bool,
    verbose: bool = False
):
    dir_path = process_directory(directory)

    if verbose:
        typer.secho(f'Looking for {target} inside \"{dir_path}\"\n', fg=typer.colors.BRIGHT_BLACK)

    matches = get_matches(target, dir_path, dir_only, no_symlinks)

    report_matches(matches, target, dir_path, dir_only, no_symlinks)
    remove_matches(matches, ignore_errors, agree, verbose)

    typer.secho('Done flawlessly!', fg=typer.colors.GREEN)


def remove_from_file(
    save_path: str,
    dir_only: bool,
    no_symlinks: bool,
    agree: bool,
    ignore_errors: bool,
    verbose: bool
):
    save_path = Path(save_path)
    if verbose:
        typer.echo(f'Looking for "{save_path}"')

    if save_path.is_dir():
        if verbose:
            typer.echo(f"Current save path is directory, looking for a file")
        save_path = save_path / DEFAULT_SAVE_FILE

    if not save_path.is_file():
        raise_error(f'There is no file with list of targets')

    with click_spinner.spinner():
        with open(save_path, 'r') as save_file:
            lines = save_file.readlines()

        matches = []
        for line in lines:
            if not line or not isinstance(line, str) or len(line) == 0:
                continue

            line = line.strip()
            path = Path(line)

            if dir_only and path.is_file():
                if verbose:
                    typer.secho(f'Skip {path} due to "dir-only=True"')
                continue

            if no_symlinks and path.is_symlink():
                if verbose:
                    typer.secho(f'Skip {path} due to "without-symlinks=True"')
                continue

            matches.append(path)

    report_matches(matches, None, None, dir_only, no_symlinks)
    remove_matches(matches, ignore_errors, agree, verbose)

    typer.secho('Done flawlessly!', fg=typer.colors.GREEN)


def remove_matches(matches: List[Path], ignore_errors: bool, agree: bool, verbose: bool):
    if agree:
        is_ready = True
    else:
        is_ready = typer.confirm("Are you sure you want to delete it?")

    if not is_ready:
        typer.echo("Ok, try next time...")
        raise typer.Abort()

    if verbose:
        typer.secho("Let's clean up this mess, shall we?\n")

    with typer.progressbar(matches) as progress:
        for match in progress:
            try:
                if match.is_file() or match.is_symlink():
                    if verbose:
                        typer.secho(f'Processing "{match}"', fg=typer.colors.BRIGHT_BLACK)
                    match.unlink(missing_ok=True)
                elif match.is_dir():
                    if verbose:
                        typer.secho(f'Processing "{match}"', fg=typer.colors.BRIGHT_BLACK)
                    shutil.rmtree(match)
                else:
                    typer.secho(f'Skip {match}')
            except OSError as e:
                if verbose or not ignore_errors:
                    typer.secho("Error: %s : %s" % (match, e.strerror), fg=typer.colors.RED)

                if not ignore_errors:
                    raise_error('\n Stop due to error')
