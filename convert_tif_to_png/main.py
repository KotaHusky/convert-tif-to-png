import os
import glob
import re
import argparse
from datetime import datetime
from enum import Enum
from typing import Optional, List
from PIL import Image

class ImageSize(Enum):
    ORIGINAL = 'original'
    FOUR_K = '4k'
    TWO_K = '2k'

def log_message(message: str, logfile: Optional[str] = None) -> None:
    """Logs a message to the console and optionally to a file."""
    print(message)
    if logfile:
        # Make sure the log file exists
        if not os.path.exists(logfile):
            open(logfile, 'a').close()
        with open(logfile, 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def resize_image(image_path: str, base_width: int) -> Image.Image:
    """Resizes an image maintaining aspect ratio."""
    img = Image.open(image_path)
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), Image.LANCZOS)
    return img

def process_directory(directory_path: str, pattern: Optional[str], size: ImageSize, log_file: Optional[str]) -> None:
    """Processes all TIF files in a directory."""
    files = glob.glob(os.path.join(directory_path, '*.tif'))
    process_files(files, pattern, size, log_file)

def process_files(files: List[str], pattern: Optional[str], size: ImageSize, log_file: Optional[str]) -> None:
    """Processes a list of files."""
    filtered_files = [f for f in files if not os.path.basename(f).startswith('.') and f.lower().endswith('.tif')]
    log_message(f"Found {len(filtered_files)} eligible files to process.", log_file)
    log_message("\n".join(filtered_files), log_file)

    for i, filename in enumerate(filtered_files):
        # Extract the shortname from the filename, removing the extension
        shortname = os.path.splitext(os.path.basename(filename))[0]
        
        # If a pattern was specified, extract the shortname from the filename using the pattern.
        # If the pattern does not match, use the original shortname.
        if pattern:
            match = re.search(pattern, shortname)
            if match:
                shortname = match.group(0)
                
        log_message(f"Processing file {i + 1} of {len(filtered_files)}: {shortname}.tif", log_file)
        process_file(filename, shortname, size, log_file)

def process_file(filename: str, file_shortname: str, size: ImageSize, log_file: Optional[str]) -> None:
    """Processes a single file."""
    log_message(f"\tConverting file...", log_file)
    base_width = {'4k': 3840, '2k': 2048, 'original': None}[size.value]
    temp_output_path = os.path.join(os.path.dirname(filename), f".{file_shortname}.png")
    output_path = os.path.join(os.path.dirname(filename), f"{file_shortname}.png")
    if base_width:
        resized_img = resize_image(filename, base_width)
    else:
        resized_img = Image.open(filename)
    resized_img.save(temp_output_path)
    os.rename(temp_output_path, output_path)
    log_message(f"\tFile converted to png: {file_shortname}.png", log_file)

def main() -> None:
    try:
        parser = argparse.ArgumentParser(description='Convert TIF images to PNG to preserve quality while reducing file size for use in social media.')
        parser.add_argument('--dir', help='Directory to scan for TIF files.')
        parser.add_argument('--file', nargs='+', help='File paths to convert. Separate multiple files with spaces.')
        parser.add_argument('--pattern', help='Regex pattern to name converted files, extracted from the original file name.')
        parser.add_argument('--size', choices=[e.value for e in ImageSize], default='original', help='Output image size.')
        parser.add_argument('--log', default=None, nargs='?', const='.', help='Enable log output at .log.txt; specify log directory or leave empty for current directory.')

        args = parser.parse_args()

        log_file = None
        if args.log is not None:
            log_path = args.log if args.log != '.' else '.log.txt'
            log_file = open(log_path, 'a')

        if args.dir and args.file:
            log_message("Specify either --dir or --file, not both.", log_file)
            return

        size = ImageSize(args.size)
        
        if args.dir:
            process_directory(args.dir, args.pattern, size, log_file)
        elif args.file:
            process_files(args.file, args.pattern, size, log_file)
        else:
            log_message("Either --dir or --file must be specified.", log_file)

        if log_file:
            log_file.close()

    except Exception as e:
        if log_file:
            log_message(f"An error occurred: {str(e)}", log_file)
        else:
            print(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    main()
