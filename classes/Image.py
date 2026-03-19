from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from classes.AppConfig import appConfig
from classes.AppLogger import logger
from classes.Camera import Camera
from classes.ImageFile import ImageFile
from classes.PathFormat import PathFormat
from classes.PathModifier import PathModifier

### TODO: Move to a config file
ROOT_DIR = "C:\\Users\\Public\\Pictures\\PhotoOrganizer\\"

@dataclass( frozen=False, slots=True )
class Image:
    
    image_file: ImageFile
    camera: Optional[Camera] = None
    expected_path: Optional[Path] = None
    #sidecar_filename: Optional[Path] = None

    # instance method
    def get_expected_path( self, path_format: PathFormat) -> Path:
        """
        Get expected_path from path_format and data
        """
        path = path_format.template
        
        path_modifiers: list[PathModifier] = [
            self.camera,
            self.camera.owner,
            self.image_file.metadata
        ]

        for path_modifier in path_modifiers:
            path = path_modifier.modify_path( path )

        return Path( ROOT_DIR ).joinpath( path ).joinpath( self.image_file.path.name )

    # instance method
    def get_matching_cameras( self, cameras: list[Camera] ) -> list[Camera]:
        """
        Get cameras, which match image_file metadata for camera_make, camera_model and date_taken, from a list of cameras
        """
        possible_cameras = []
        if( self.image_file and self.image_file.metadata ):
            # Filter by make and model
            possible_cameras = [ 
                camera for camera in cameras
                if camera.make == self.image_file.metadata.camera_make 
                and camera.model == self.image_file.metadata.camera_model
            ]
            # If this gives more than 1 possible camera, filter by date taken
            if len(possible_cameras) > 1 and self.image_file.metadata.date_taken != None:
                possible_cameras = [ 
                    camera for camera in possible_cameras
                    if camera.from_date <= self.image_file.metadata.date_taken
                    and camera.to_date >= self.image_file.metadata.date_taken
                ]
        return possible_cameras

    # instance method
    def get_path_format(self):
        """
        Get single path_format, which matches camera owner name and image capture type, from a list of path_formats
        """
        path_format = None
        possible_pfs = self.camera.get_matching_path_formats( appConfig.path_formats )

        # If there is more or less than 1, log a warning
        if len(possible_pfs) != 1:
            logger.warning( f"Found {len(possible_pfs)} possible path formats for {self.camera.owner.name} {self.camera.image_capture_type.value}")
        # Else set path_format to this one
        else:
            path_format = possible_pfs[0]

        return path_format

    # instance method
    def load(self):
        """
        Load composite parts
        """
        self.image_file.load_metadata()
        self.load_camera()
        self.load_image_expected_path()

    # instance method
    def load_camera(self):
        """
        Load camera
        """
        possible_cameras = self.get_matching_cameras( appConfig.cameras )

        # If there is more or less than 1, log a warning
        if len(possible_cameras) != 1:
            logger.warning( f"Found {len(possible_cameras)} possible cameras for {self.image_file.metadata.camera_make} {self.image_file.metadata.camera_model} {self.image_file.metadata.date_taken}")
        # Else set camera to this one
        else:
            self.camera = possible_cameras[0]

    # instance method
    def load_image_expected_path(self):
        """
        Load image expected path
        """
        path_format = None

        # If camera found, get path_format, if possible
        if self.camera:
            path_format = self.get_path_format()

        ## If path_format found, get image_expected_path
        if path_format:
            self.expected_path = self.get_expected_path( path_format )
            logger.info( f"Expected path: {self.expected_path}")
            logger.info( f"Expected path == Actual path: {self.expected_path == self.image_file.path}")
