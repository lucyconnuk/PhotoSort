from pathlib import Path

def path_is_valid( path: Path ):
    path_is_valid = False;

    if path.exists():
        if path.is_dir():
            print( f"{path} is a directory" )
            path_is_valid = True;
        elif path.is_file():
            print( f"{path} is a file" )
        else:
            print( f"{path} exists but is not a directory or a file" )
    else:
        print( f"{path} does not exist" )

    return path_is_valid

def main():
    path_str = input( "Enter directory path: " ).strip()
    path = Path( path_str )
    path_is_valid( path )

if __name__ == "__main__":
    main()