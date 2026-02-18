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

def main():
    path_str = input( "Enter directory path: " ).strip()
    path = Path( path_str )
    (valid, message) = check_valid_path( path )
    print( message )

if __name__ == "__main__":
    main()