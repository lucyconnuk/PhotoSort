from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from classes.AppConfig import appConfig
from classes.AppLogger import logger
from classes.Camera import Camera
from classes.ImageFile import ImageFile
from classes.PathFormat import PathFormat


@dataclass( frozen=False, slots=True )
class Image:
    
    image_file: Optional[ImageFile] = None
    camera: Optional[Camera] = None
    expected_path: Optional[Path] = None
    #sidecar_filename: Optional[Path] = None

    def get_expected_path( cls, path_format: PathFormat) -> Path:
        path = ""
        if path_format != "" and cls.camera.image_capture_type and cls.camera.owner and cls.image_file.metadata.date_taken:
            path = path_format.template
            path = path.replace( r"\{ict\}", cls.camera.image_capture_type.value )
            path = path.replace( r"\{directory\}", cls.camera.owner.directory )
            path = path.replace( r"\{yyyy\}", datetime.strftime( cls.image_file.metadata.date_taken, "%Y" ) )
            path = path.replace( r"\{mm\}", datetime.strftime( cls.image_file.metadata.date_taken, "%m" ) )
            path = path.replace( r"\{dd\}", datetime.strftime( cls.image_file.metadata.date_taken, "%d" ) )
        return Path( path )

    def get_matching_cameras( cls, cameras: list[Camera] ) -> list[Camera]:
        possible_cameras = []
        if( cls.image_file and cls.image_file.metadata ):
            # Filter by make and model
            possible_cameras = [ 
                camera for camera in cameras
                if camera.make == cls.image_file.metadata.camera_make 
                and camera.model == cls.image_file.metadata.camera_model
            ]
            # If this gives more than 1 possible camera, filter by date taken
            if len(possible_cameras) > 1 and cls.image_file.metadata.date_taken != None:
                possible_cameras = [ 
                    camera for camera in possible_cameras
                    if camera.from_date <= cls.image_file.metadata.date_taken
                    and camera.to_date >= cls.image_file.metadata.date_taken
                ]
        return possible_cameras

    ### TODO: Move this to Camera?
    def get_matching_path_formats( cls, path_formats: list[PathFormat] ) -> list[PathFormat]:
        possible_path_formats = []
        if( cls.camera ):
            # Filter by owner and image_capture_type
            possible_path_formats = [ 
                pf for pf in path_formats
                if pf.owner_name == cls.camera.owner.name
                and pf.image_capture_type == cls.camera.image_capture_type
            ]
        return possible_path_formats

    # TODO rename
    def get_metadata(self):

        ## Get metadata
        self.image_file.get_metadata()

        # Get camera from image_file metadata for camera_make, camera_model and date_taken
        possible_cameras = self.get_matching_cameras( appConfig.cameras )
        # If there is more or less than 1, log a warning
        if len(possible_cameras) != 1:
            logger.warning( f"Found {len(possible_cameras)} possible cameras for {self.image_file.metadata.camera_make} {self.image_file.metadata.camera_model} {self.image_file.metadata.date_taken}")
        # Else set camera to this one
        else:
            self.camera = possible_cameras[0]

        ## Get path_format from owner and initial_capture_type
        path_format = None
        if self.camera and self.camera.owner and self.camera.image_capture_type:
            possible_pfs = self.get_matching_path_formats( appConfig.path_formats )

            # If there is more or less than 1, log a warning
            if len(possible_pfs) != 1:
                logger.warning( f"Found {len(possible_pfs)} possible path formats for {self.camera.owner.name} {self.camera.image_capture_type.value}")
            # Else set path_format to this
            else:
                path_format = possible_pfs[0]

        # Get image_expected_path from path_format and data
        if( path_format ):
            self.expected_path = self.get_expected_path( path_format )
        
