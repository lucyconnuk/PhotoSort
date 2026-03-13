from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import piexif


@dataclass( frozen=False, slots=True )
class ImageMetadata:

    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    date_taken: Optional[datetime] = None

    @classmethod
    def from_path( cls, image_path: Path ):

        # Get image metadata using piexif.
        image_metadata = piexif.load( str( image_path ) )

        # Get camera make and model and date image taken from the metadata.
        make = cls.get_camera_make( image_metadata )
        model = cls.get_camera_model( image_metadata )
        date = cls.get_date_taken( image_metadata )

        # Call the class constructor with this data.
        return cls( make, model, date )
        
    @staticmethod
    def get_camera_make( image_metadata: dict[str, any] ) -> str:
        return image_metadata["0th"][271].decode('ascii')

    @staticmethod
    def get_camera_model( image_metadata: dict[str, any] ) -> str:
        return image_metadata["0th"][272].decode('ascii')

    @staticmethod
    def get_date_taken( image_metadata: dict[str, any] ) -> datetime:
        return datetime.strptime( image_metadata["0th"][306].decode('ascii'), "%Y:%m:%d %H:%M:%S" )
