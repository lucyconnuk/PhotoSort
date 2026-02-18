import argparse
from pathlib import Path

def check_valid_path( path: Path ):
    path_is_valid = False
    message = ''

    if path.exists():
        if path.is_dir():
            path_is_valid = True
            message = f"{path} is a directory"
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
        "-directory",
        "-d",
        help = "Path to the root image directory"
    )
    return parser.parse_args()
   
def main():
    args = get_command_line_args()
    if args.directory:
        path_str = args.directory
    else:
        path_str = input( "Enter directory path: " ).strip()
    path = Path( path_str )
    (valid, message) = check_valid_path( path )
    print( message )

if __name__ == "__main__":
    main()