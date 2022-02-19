import re
import typer

from typing import Optional
from pathlib import Path

from .utils import process_directory, get_matches, report_matches, DEFAULT_SAVE_FILE

prefix_extractor = re.compile(r'/.*$')


def scan_directory(
    target: str,
    directory: Optional[str],
    dir_only: bool,
    no_symlinks: bool,
    save_list: bool,
    save_path: str,
    verbose: bool = False
):
    dir_path = process_directory(directory)

    if verbose:
        typer.secho(f'Looking for {target} inside \"{dir_path}\"\n', fg=typer.colors.BRIGHT_BLACK)

    matches = get_matches(target, dir_path, dir_only, no_symlinks)

    report_matches(matches, target, dir_path, dir_only, no_symlinks)

    if save_list:
        save_path = Path(save_path)
        if verbose:
            typer.echo(f'\nSaving list to "{save_path}" for further use')

        if save_path.is_dir():
            if verbose:
                typer.echo(f"Current save path is directory, let's create a file")
            save_path = save_path / DEFAULT_SAVE_FILE

        with open(save_path, 'w') as out_file:
            for match in matches:
                out_file.write(str(match) + '\n')

        typer.secho(f'Successfully saved list to "{save_path}"', fg=typer.colors.GREEN)
