# TIF to PNG Image Converter

## Introduction

This Python script converts TIF images to PNG format. It allows for resizing the images to various predefined sizes (Original, 4K, 2K) and works either on a directory or individual files. It also allows for renaming the converted files based on a regex pattern extracted from the original file name.

## Requirements

- Python 3.5+
- PIL (Pillow) library

## Development

`poetry` is used to manage dependencies and virtual environments.
`GitHub Actions` is used for CI/CD, with a trusted publishing connection to PyPi.

## Installation

Install the convert-tif-to-png tool via pip:

```bash
pip install convert-tif-to-png
```

Also, ensure you have the required Pillow library:

```bash
pip install Pillow
```

## Usage

### Command Line Options

| Option | Description |
| --- | --- |
| `--dir` | Path to directory containing TIF files to convert. |
| `--file` | Path to individual TIF file(s) to convert. |
| `--pattern` | Regex pattern to name converted files, extracted from the original file name.
| `--size` | Resize images to one of the following sizes: `original`, `4k`, `2k`. |
| `--log` | Log output to file. Defaults to `./.log.txt` |

### Examples

*Note: You can use Python's `-m` flag to run a Module as a script. Module names use underscores instead of hyphens.*

To process a directory:

```bash
python3 -m convert_tif_to_png --dir /path/to/directory --pattern 'some-regex-pattern' --size 4k
```

To process individual files:

```bash
python3 -m convert_tif_to_png --file /path/to/file1.tif /path/to/file2.tif --pattern 'some-regex-pattern' --size 4k
```

#### Regex Pattern

Regular expressions (regex) are patterns used to match and manipulate strings in text. Use [RegExr](https://regexr.com/) to learn about, build, and test your patterns in a UI. ChatGPT is another great resource for learning Regex and building complex patterns with natural language.

The `--pattern` option renames converted files based on a regex pattern extracted from the original file name, excluding the file extension and preceding path information.

As an example, if you have the following files:

```text
CANON1234.tif
CANON5678.tif
CANON8149-ENHANCED-NR.tif
CANON9322-ENHANCED-NR.tif
CANON9322-ENHANCED-NR (copy 1).tif
```

Use the following regex pattern to extract the file name CANON followed by a series of numbers:

```bash
--pattern 'CANON\d+'
```

This will result in the following file names:

```text
CANON1234.png
CANON5678.png
CANON8149.png
CANON9322.png
CANON9322.png
```

*Note that if there is a mismatch with the pattern, the original file name will be used.*

### Integration: MacOS Automator

#### Prerequisites

Before integrating this script into MacOS Automator, make sure you have the following prerequisites installed and configured:

1. `pyenv`: A Python version management tool, used to set the Python version for the script.
    - Installation: Use Homebrew by running `brew install pyenv` in your terminal.
    - Setting up: Add `pyenv init` to your shell to enable shims and autocompletion. [See official documentation for more details](https://github.com/pyenv/pyenv#installation).

2. Python Path: You'll need the full path to your Python interpreter.
    - Finding Python Path: Run `which python` or `which python3` in your terminal to get the full path.

#### Integration

To integrate this script into macOS Automator for automated file processing:

1. Open Automator and create a new "Folder Action."
2. Set the "Folder Action receives files and folders added to" to your desired directory.
3. Set "Pass input" to "as arguments."
4. Add a "Run Shell Script" action.
5. Enter the full path to your Python interpreter and script, along with any command line arguments, like so:

```bash
/full/path/to/python3 -m convert_tif_to_png --size 4k --pattern 'some-regex-pattern' --file "$@"
```

Make sure you replace `/full/path/to/python3` with the actual path on your system.
The `"$@"` parameter in Automator references file(s) added to the folder.

Any new TIF files added to the specified folder will automatically be converted to PNG.
