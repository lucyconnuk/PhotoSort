from dataclasses import dataclass

from classes.Camera import Camera
from classes.Owner import Owner
from classes.PathFormat import PathFormat


@dataclass( frozen=False, slots=True )
class AppConfig:

    owners: list[Owner]
    cameras: list[Camera]
    path_formats: list[PathFormat]

    def __init__(self):
        
        self.owners = Owner.get_all( r'./data/owners.csv' )
        self.cameras = Camera.get_all( r'./data/cameras.csv', self.owners )
        self.path_formats = PathFormat.get_all( r'./data/path_formats.csv' )

# Create singleton instance of AppConfig
appConfig = AppConfig()
