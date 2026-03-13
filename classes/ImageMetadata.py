from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import piexif

# Metadata constants
SECTION = "0th"
MAKE_INDEX = 271
MODEL_INDEX = 272
DATE_INDEX = 306
DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

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
        make = cls.get_string( image_metadata, SECTION, MAKE_INDEX )
        model = cls.get_string( image_metadata, SECTION, MODEL_INDEX )
        date = cls.get_date( cls.get_string( image_metadata, SECTION, DATE_INDEX ) )

        # Call the class constructor with this data.
        return cls( make, model, date )
        
    @staticmethod
    def get_string( metadata_dict: dict[str, any], section: str, index: int ) -> str:
        value = None
        if( metadata_dict 
            and section in metadata_dict 
            and type(metadata_dict[section]) is list 
            and len( metadata_dict[section] ) > index ):
            value = metadata_dict[section][index]
        if( type(value) is bytes ):
            value = value.decode('ascii')
        return value

    @staticmethod
    def get_date( metadata_string: str ) -> datetime:
        value = None
        if( metadata_string ):
            value = datetime.strptime( metadata_string, DATE_FORMAT )
        return value
