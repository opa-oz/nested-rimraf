# `nested-rimraf`

Nested rimraf CLI app.

Use it to clear your junk in nested directories
Looking for target file/directory through specified tree and then remove everything

## Practice

**Imaginary folder structure:**

```bash
/subject
  → /file
    → /node_modules // file, not directory
  → /node_modules
    → /enemy.txt
  → /sub
    → /2
      → /1
        → /4
          → /node_modules
            → /enemy.txt
    → /3
      → /node_modules
        → /enemy.txt
  → /sub2
    → /node_modules
      → /enemy.txt
  → /symlink
    → /example
      → /enemy.txt
    → /node_modules // symlink to /subject/symlink/example
```

**Tasks:**

1. Find all `node_modules`
2. Find and remove all `node_modules`
3. Find and remove all **directories** named `node_modules`
4. Find and remove all `node_modules`, but do not remove symlinks
5. `[Ultimate]` Find all `node_modules`, except files and symlinks, save them to file, correct file and remove the
   remaining

### 1. Find all `node_modules`

We need to run `scan` command with `target=node_modules` and `directory=./subject`

```bash
$> nested-rimraf scan node_modules ./subject

Files and directories (include symlinks):
        → subject/node_modules
        → subject/symlink/node_modules
        → subject/file/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules

```

### 2. Find and remove all `node_modules`

As easy, as previous one. Just use `rm` instead of `scan`
```bash
$> nested-rimraf rm node_modules ./subject

Files and directories (include symlinks):
        → subject/node_modules
        → subject/symlink/node_modules
        → subject/file/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Are you sure you want to delete it? [y/N]: y
Done flawlessly!
```

_Note:_ Question `Are you sure you want to delete it? [y/N]: y` may be avoided with `--agree/-y` option. Like that:
```bash
$> nested-rimraf rm -y node_modules ./subject

Files and directories (include symlinks):
        → subject/node_modules
        → subject/symlink/node_modules
        → subject/file/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Done flawlessly!
```

### 3. Find and remove all **directories** named `node_modules`

Ok, lets add option `--dir-only/-d`

```bash
$> nested-rimraf rm -y node_modules ./subject --dir-only 

Directories (include symlinks):
        → subject/node_modules
        → subject/symlink/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Done flawlessly!
```

As you can see, there is no `subject/file/node_modules` in the list (because it's file, not a directory).

Let's run something similar

### 4. Find and remove all `node_modules`, but do not remove symlinks

Same pattern:

```bash
$> nested-rimraf rm -y node_modules ./subject --without-symlinks

Directories (include symlinks):
        → subject/node_modules
        → subject/file/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Done flawlessly!
```

Let's try the hardest one, shall we?

### 5. `[Ultimate]` Find all `node_modules`, except files and symlinks, save them to file, correct file and remove the
   remaining

Human control, eh?

```bash
$>  nested-rimraf scan -dsL node_modules ./subject --save-path ./subject/to_correct.txt 
Directories (exclude symlinks):
        → subject/node_modules
        → subject/sub/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Successfully saved list to "subject/to_correct.txt"
```

A lot of params:
- `-d` - same as `--dir-only`. Includes only directories
- `-s` - same as `--without-symlinks`.  Excludes symlinks
- `-L` - same as `--save-list`. Saves list of matches to file
- `--save-path` - path to save matches

What does this file contain? Nothing special, just list of files
```bash
$> cat ./subject/to_correct.txt

subject/node_modules
subject/sub/node_modules
subject/sub/3/node_modules
subject/sub/2/1/4/node_modules
subject/sub2/node_modules
```

Let's take it easy and save `subject/sub/node_modules` by removing it from the file.

And, 3, 2, 1, clear!
```bash
$> nested-rimraf rmf -yds ./subject/to_correct.txt

Directories (enclude symlinks):
        → subject/node_modules
        → subject/sub/3/node_modules
        → subject/sub/2/1/4/node_modules
        → subject/sub2/node_modules
Done flawlessly!
```

Good job! 

**Usage**:

```console
$ nested-rimraf [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `rm`: Scan and remove targets inside directory and...
* `rmf`: Took file, generated by "nested-rimraf scan"...
* `scan`: Scan directory and child-directories to find...

## `nested-rimraf rm`

Scan and remove targets inside directory and sub-directories

**Usage**:

```console
$ nested-rimraf rm [OPTIONS] TARGET [DIRECTORY]
```

**Arguments**:

* `TARGET`: Target name to find inside of directory  [required]
* `[DIRECTORY]`: Directory to scan in  [default: .]

**Options**:

* `-d, --dir-only`: Target only directories  [default: False]
* `-s, --without-symlinks`: Do not process symlinks as targets  [default: False]
* `-y, --agree`: Remove without any questions  [default: False]
* `-I, --ignore-errors`: Ignore errors and delete until possible  [default: False]
* `-v, --verbose`: Talk a lot  [default: False]
* `--help`: Show this message and exit.

## `nested-rimraf rmf`

Took file, generated by "nested-rimraf scan" and remove everything from it

**Usage**:

```console
$ nested-rimraf rmf [OPTIONS] [SAVE_PATH]
```

**Arguments**:

* `[SAVE_PATH]`: Remove list from passed file or ".nr-todo" inside passed directory  [default: .nr-todo]

**Options**:

* `-d, --dir-only`: Target only directories  [default: False]
* `-s, --without-symlinks`: Do not process symlinks as targets  [default: False]
* `-y, --agree`: Remove without any questions  [default: False]
* `-I, --ignore-errors`: Ignore errors and delete until possible  [default: False]
* `-v, --verbose`: Talk a lot  [default: False]
* `--help`: Show this message and exit.

## `nested-rimraf scan`

Scan directory and child-directories to find targets

Usage:

> nested-rimraf scan <target> <directory>

**Usage**:

```console
$ nested-rimraf scan [OPTIONS] TARGET [DIRECTORY]
```

**Arguments**:

* `TARGET`: Target name to find inside of directory  [required]
* `[DIRECTORY]`: Directory to scan in  [default: .]

**Options**:

* `-d, --dir-only`: Target only directories  [default: False]
* `-s, --without-symlinks`: Do not process symlinks as targets  [default: False]
* `-L, --save-list`: Save list of targets for further use  [default: False]
* `--save-path TEXT`: File to save list of targets  [default: .nr-todo]
* `-v, --verbose`: Talk a lot  [default: False]
* `--help`: Show this message and exit.
