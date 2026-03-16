from dataclasses import dataclass
from pathlib import Path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

# For additional coding notes, see Camera.py
@dataclass( frozen=True, slots=True )
class File:
    """
    A file object. Has a Path.
    """
    
    file_path: Path

    @staticmethod
    def check_valid_path( path: Path ) -> tuple[ bool, str ]:
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

    @staticmethod
    def get_files( files_and_dirs: list[Path] ) -> list[Path]:
        return [ file_or_dir for file_or_dir in files_and_dirs if file_or_dir.is_file() ]

    @staticmethod
    def get_image_files( files: list[Path] ) -> list[Path]:
        return [ file for file in files if file.suffix.lower() in IMAGE_EXTENSIONS ]

    @staticmethod
    def get_xmp_files( files: list[Path] ) -> list[Path]:
        return [ file for file in files if file.suffix.lower() == ".xmp" ]
