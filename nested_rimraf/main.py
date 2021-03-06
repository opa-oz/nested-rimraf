import typer
from typing import Optional

from .scan_directory import scan_directory
from .remove_in_directory import remove_in_directory, remove_from_file
from .utils import DEFAULT_SAVE_FILE

app = typer.Typer(name="nested-rimraf")


@app.callback()
def callback():
    """
    Nested rimraf CLI app.

    Use it to clear your junk in nested directories
    """


@app.command("scan")
def cli_scan(
    target: str = typer.Argument(..., help="Target name to find inside of directory"),
    directory: Optional[str] = typer.Argument(default='.', help="Directory to scan in"),
    dir_only: bool = typer.Option(False, '--dir-only', '-d', help="Target only directories"),
    no_symlinks: bool = typer.Option(False, '--without-symlinks', '-s', help="Do not process symlinks as targets"),
    save_list: bool = typer.Option(False, '--save-list', '-L', help="Save list of targets for further use"),
    save_path: str = typer.Option(default=DEFAULT_SAVE_FILE, help="File to save list of targets"),
    verbose: bool = typer.Option(False, '--verbose', '-v', help="Talk a lot")
):
    """
    Scan directory and child-directories to find targets

    Usage:

    > nested-rimraf scan <target> <directory>
    """
    scan_directory(target, directory, dir_only, no_symlinks, save_list, save_path, verbose)


@app.command("rm")
def cli_remove(
    target: str = typer.Argument(..., help="Target name to find inside of directory"),
    directory: Optional[str] = typer.Argument(default='.', help="Directory to scan in"),
    dir_only: bool = typer.Option(False, '--dir-only', '-d', help="Target only directories"),
    no_symlinks: bool = typer.Option(False, '--without-symlinks', '-s', help="Do not process symlinks as targets"),
    agree: bool = typer.Option(False, '--agree', '-y', help="Remove without any questions"),
    ignore_errors: bool = typer.Option(False, '--ignore-errors', '-I', help="Ignore errors and delete until possible"),
    verbose: bool = typer.Option(False, '--verbose', '-v', help="Talk a lot")
):
    """
    Scan and remove targets inside directory and sub-directories
    """
    remove_in_directory(target, directory, dir_only, no_symlinks, agree, ignore_errors, verbose)


@app.command("rmf")
def cli_remove_from_file(
    save_path: str = typer.Argument(
        DEFAULT_SAVE_FILE,
        help=f"Remove list from passed file or \"{DEFAULT_SAVE_FILE}\" inside "
             f"passed directory"
    ),
    dir_only: bool = typer.Option(False, '--dir-only', '-d', help="Target only directories"),
    no_symlinks: bool = typer.Option(False, '--without-symlinks', '-s', help="Do not process symlinks as targets"),
    agree: bool = typer.Option(False, '--agree', '-y', help="Remove without any questions"),
    ignore_errors: bool = typer.Option(False, '--ignore-errors', '-I', help="Ignore errors and delete until possible"),
    verbose: bool = typer.Option(False, '--verbose', '-v', help="Talk a lot")
):
    """
    Took file, generated by "nested-rimraf scan" and remove everything from it
    """
    remove_from_file(save_path, dir_only, no_symlinks, agree, ignore_errors, verbose)
