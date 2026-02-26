from dataclasses import dataclass
from pathlib import Path

# TODO:
# - use list comprehension where appropriate

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

@dataclass( frozen=True, slots=True )
class File:
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
        files = []
        for file_or_dir in files_and_dirs:
            if file_or_dir.is_file():
                files.append( file_or_dir )
        return files

    @staticmethod
    def get_image_files( files: list[Path] ) -> list[Path]:
        images = []
        for file in files:
            if file.suffix.lower() in IMAGE_EXTENSIONS:
                images.append(file)
        return images

    @staticmethod
    def get_xmp_files( files: list[Path] ) -> list[Path]:
        xmp_files = []
        for file in files:
            if file.suffix.lower() == ".xmp":
                xmp_files.append(file)
        return xmp_files