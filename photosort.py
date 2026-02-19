import argparse
from pathlib import Path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def check_valid_path( path: Path ):
    path_is_valid = False
    message = ''

    if path.exists():
        if path.is_dir():
            path_is_valid = True
            message = f"Directory is: {path}"
        elif path.is_file():
            message = f"{path} is a file"
        else:
            message = f"{path} exists but is not a directory or a file"
    else:
        message = f"{path} does not exist"

    return path_is_valid, message

def get_command_line_args():
    parser = argparse.ArgumentParser(
        description = "List all image files in a directory and its subdirectories."
    )
    parser.add_argument(
        "-path",
        "-p",
        help = "Path to the root image directory",

        # TODO Remove this test default setting
        default = r'C:\Users\Public\Pictures\PhotoOrganizer\Digital\Mary\2006'
    )
    return parser.parse_args()

def get_files( files_and_dirs: list[Path] ):
    files = []
    for file_or_dir in files_and_dirs:
        if file_or_dir.is_file():
            files.append( file_or_dir )
    return files

def get_image_files( files: list[Path] ):
    images = []
    for file in files:
        if file.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(file)
    return images

def main():
    args = get_command_line_args()
    path_str = args.path if args.path else input( "Enter path to the root image directory: " ).strip()
    path = Path( path_str )
    (valid, message) = check_valid_path( path )
    print( message )
    if valid:
        print( "Images are: ")
        files_and_dirs = path.rglob("*")
        files = get_files( files_and_dirs )
        images = get_image_files( files )
        for image in images:
            print( image.name )

if __name__ == "__main__":
    main()