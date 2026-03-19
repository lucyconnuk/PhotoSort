from dataclasses import dataclass
from pathlib import Path

from classes.Camera import Camera
from classes.Owner import Owner
from classes.PathFormat import PathFormat


@dataclass( frozen=False, slots=True )
class AppConfig:

    owners: list[Owner]
    path_formats: list[PathFormat]
    cameras: list[Camera]
    root_image_dir: Path

    def __init__(self):
        
        self.owners = Owner.get_all( r'./data/owners.csv' )
        self.path_formats = PathFormat.get_all( r'./data/path_formats.csv' )
        self.cameras = Camera.get_all( r'./data/cameras.csv', self.owners )


# Create singleton instance of AppConfig
appConfig = AppConfig()
