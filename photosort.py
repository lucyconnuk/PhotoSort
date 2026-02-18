from pathlib import Path

def check_directory_exists( directory ):
    directory_exists = False;

    if directory.exists():
        if directory.is_dir():
            print( f"{directory} is a directory" )
            directory_exists = False;
        elif directory.is_file():
            print( f"{directory} is a file" )
        else:
            print( f"{directory} exists but is not a directory or a file" )
    else:
        print( f"{directory} does not exist" )

    return directory_exists

def main():
    directory_path = input( "Enter directory path: " ).strip()
    directory = Path( directory_path )
    check_directory_exists( directory )

if __name__ == "__main__":
    main()