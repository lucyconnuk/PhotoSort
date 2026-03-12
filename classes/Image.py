from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import piexif

from classes.AppConfig import appConfig
from classes.AppLogger import logger
from classes.Camera import Camera
from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from classes.PathFormat import PathFormat


@dataclass( frozen=False, slots=True )
class Image:
    
    image_path: Optional[Path] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    camera: Optional[Camera] = None
    date_taken: Optional[datetime] = None
    owner: Optional[Owner] = None
    initial_capture_type: Optional[ImageCaptureType] = None
    image_expected_path: Optional[Path] = None
    #sidecar_filename: Optional[Path] = None

    def getExpectedPath( cls, path_format: PathFormat) -> Path:
        path = ""
        if path_format != "" and cls.initial_capture_type and cls.owner and cls.date_taken:
            path = path_format.template
            path = path.replace( r"\{ict\}", cls.initial_capture_type.value )
            path = path.replace( r"\{directory\}", cls.owner.directory )
            path = path.replace( r"\{yyyy\}", datetime.strftime( cls.date_taken, "%Y" ) )
            path = path.replace( r"\{mm\}", datetime.strftime( cls.date_taken, "%m" ) )
            path = path.replace( r"\{dd\}", datetime.strftime( cls.date_taken, "%d" ) )
        return Path( path )

    def getMetadata(self):

        ## Get camera_make, camera_model and date_taken from metadata
        image_metadata = piexif.load( str( self.image_path ) )
        self.camera_make = image_metadata["0th"][271].decode('ascii')
        self.camera_model = image_metadata["0th"][272].decode('ascii')
        self.date_taken = datetime.strptime( image_metadata["0th"][306].decode('ascii'), "%Y:%m:%d %H:%M:%S" )

        ## Get camera from camera_make, camera_model and date_taken

        # Filter by make and model
        possible_cameras = [ camera for camera in appConfig.cameras 
            if camera.make == self.camera_make 
            and camera.model == self.camera_model
        ]
        # If this gives more than 1 possible camera, filter by date taken
        if len(possible_cameras) > 1:
            possible_cameras = [ camera for camera in possible_cameras
                if camera.from_date <= self.date_taken
                and camera.to_date >= self.date_taken
            ]
        # If there is more or less than 1, log a warning
        if len(possible_cameras) != 1:
            logger.warning( f"Found {len(possible_cameras)} possible cameras for {self.camera_make} {self.camera_model} {self.date_taken}")
        # Else set camera to this
        else:
            self.camera = possible_cameras[0]

        ## Get owner and initial_capture_type from camera
        if self.camera:
            if not self.owner:
                self.owner = self.camera.owner
            if not self.initial_capture_type:
                self.initial_capture_type = self.camera.image_capture_type

        ## Get path_format from owner and initial_capture_type
        if self.owner and self.initial_capture_type:
            path_format = ""
            possible_pfs = [ pf for pf in appConfig.path_formats 
                if pf.owner_name == self.owner.name 
                and pf.image_capture_type == self.initial_capture_type.value
            ]
            # If there is more or less than 1, log a warning
            if len(possible_pfs) != 1:
                logger.warning( f"Found {len(possible_pfs)} possible path formats for {self.owner.name} {self.initial_capture_type}")
            # Else set path_format to this
            else:
                path_format = possible_pfs[0]

        # Get image_expected_path from path_format and data
        self.image_expected_path = self.getExpectedPath( path_format )
        
