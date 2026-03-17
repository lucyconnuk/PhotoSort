from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import piexif

from classes.PathModifier import PathModifier

# Metadata constants
SECTION = "0th"
MAKE_KEY = "Make"
MODEL_KEY = "Model"
DATETIME_KEY = "DateTime"
DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

PATH_TOKENS = {
    r"{year}":          [ r"%Y", "Year"],
    r"{yyyy}":          [ r"%Y", "Year"],
    r"{yy}":            [ r"%Y", "Year"],
    r"{month}":         [ r"%m", "Month"],
    r"{mm}":            [ r"%m", "Month"],
    r"{day}":           [ r"%d", "Day"],
    r"{dd}":            [ r"%d", "Day"],
    r"{yyyy-mm}":       [ r"%Y-%m", "YearMonth"],
    r"{yyyy-mm-dd}":    [ r"%Y-%m-%d", "YearMonthDay"],
}

PATH_DEFAULT_PREFIX = "Unknown"

@dataclass( frozen=True, slots=True )
class ImageMetadata(PathModifier):
    """
    (Some of) the metadata associated with an image. 
    The only metadata we are interested in here is camera make and model and date taken.
    """

    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    date_taken: Optional[datetime] = None

    @classmethod
    def from_path( cls, image_path: Path ):

        # Get image metadata using piexif.
        image_metadata = piexif.load( str( image_path ), True )

        # Get camera make and model and date image taken from the metadata.
        make = ImageMetadata.get_string( image_metadata, SECTION, MAKE_KEY )
        model = ImageMetadata.get_string( image_metadata, SECTION, MODEL_KEY )
        date = ImageMetadata.get_date( cls.get_string( image_metadata, SECTION, DATETIME_KEY ) )

        # Call the class constructor with this data.
        return cls( make, model, date )
        
    # instance method
    def modify_path( self, template: str ) -> str:

        result = template

        for token in PATH_TOKENS:
            search_string = token
            if( self.date_taken ):
                replacement_string = datetime.strftime( self.date_taken, PATH_TOKENS[token][0] )
            else:
                replacement_string = PATH_DEFAULT_PREFIX + PATH_TOKENS[token][1]
            result = result.replace( search_string, replacement_string )

        return result       

    @staticmethod
    def get_string( metadata_dict: dict[str, any], section: str, key: str ) -> str:
        value = None
        if( metadata_dict 
            and metadata_dict[section]
            and metadata_dict[section][key] ):
            value = metadata_dict[section][key]
        if( type(value) is bytes ):
            value = value.decode('ascii')
        return value

    @staticmethod
    def get_date( metadata_string: str ) -> datetime:
        value = None
        if( metadata_string ):
            value = datetime.strptime( metadata_string, DATE_FORMAT )
        return value
