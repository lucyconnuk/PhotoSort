from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

import pandas

from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner

DATA_FILE_DATE_COLUMNS = [ "to_date", "from_date" ]
DATA_FILE_DATE_FORMAT = "yyyy-MM-dd"
PARSE_DATE_FORMAT = r"%Y-%m-%d"
PARSE_DATE_FORMAT_SHORT = r"%Y-%m"

# Make this class type-safe and memory-efficient, using frozen and slots parameters.
# See https://docs.python.org/3/library/dataclasses.html#frozen-instances
# and https://github.com/orgs/community/discussions/168147 
@dataclass( frozen=True, slots=True )
class Camera:
    """
    A physical device which captures Images. 
    Image Capture Type can be straight to Digital, or scanned from Film.
    Identifiable by its Make and Model, and if necessary an Instance no.
    Has an Owner and optional usage From and To Dates.
    """
    make: str
    model: str
    image_capture_type: ImageCaptureType
    owner: Owner = None
    instance: Optional[int] = 0
    from_date: Optional[date] = None
    to_date: Optional[date] = None

    # Coding notes: 
    # @classmethod - See https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-a-beginner 
    # cls means "this class" - See https://realpython.com/ref/glossary/cls/
    @classmethod
    def from_dict( cls, data: dict, owners: list[Owner] ) -> Camera:
        """
        Create Camera from dictionary of values
        """

        Camera.validate_image_capture_type( data, "image_capture_type" )
        Camera.validate_owner( data, "owner", owners )
        Camera.validate_int( data, "instance" )
        Camera.validate_date( data, "from_date" )
        Camera.validate_date( data, "to_date" )

        # Coding note: **data means "all the values in data"
        # So here we are passing ALL of the values in the data dict, including the ones we've just validated, to the cls() method
        # and returning the return value.
        return cls(**data)

    @staticmethod
    def dataframe_to_list( cameras_df: pandas.DataFrame, owners: list[Owner] ) -> list[Camera]:
        """
        Convert Camera data from dataframe to list of Cameras.
        """

        # Pandas fills empty spaces in the dataframe with the floating point value 'nan'.
        # Replace these with None, using pandas.DataFrame.replace.
        # See https://stackoverflow.com/a/54403705 
        cameras_df = cameras_df.replace( { float('nan'): None } )

        # Convert dataframe into list of records, where each record is a dictionary of key-value pairs,
        # using pandas.DataFrame.to_dict( orient="records" ).
        cameras_ld = cameras_df.to_dict( orient="records" )

        # Convert list of records into list of Camera objects, using a list comprehension,
        # and return the list.
        # See https://realpython.com/list-comprehension-python/ 
        return [ Camera.from_dict( record, owners ) for record in cameras_ld ]

    @staticmethod
    def get_all( file_path: str, owners: list[Owner] ) -> list[Camera]:
        """
        Given a path to a csv file containing Camera data, return a list of Cameras.
        """
        camera_data_file = Path( file_path )
        cameras_df = Camera.load_all( camera_data_file )
        return Camera.dataframe_to_list( cameras_df, owners )
    
    @staticmethod
    def load_all( camera_data_file: Path ) -> pandas.DataFrame:
        """
        Get Camera data from csv file.
        """
        return pandas.read_csv( 
            camera_data_file,
            parse_dates = DATA_FILE_DATE_COLUMNS,
            date_format = DATA_FILE_DATE_FORMAT
        )

    @staticmethod
    def parse_date( date_str: str ) -> Optional[date]:
        """
        Parse a date string, which can be in year-month-day or year-month format,
        and return a valid date, or None.
        """
        camera_date = None
        try:
            camera_date = date.strptime( date_str, PARSE_DATE_FORMAT ) 
        except ValueError:
            try:
                camera_date = date.strptime( date_str, PARSE_DATE_FORMAT_SHORT ) 
            except ValueError:
                camera_date = None
        return camera_date

    @staticmethod
    def validate_date( data: dict, field_name: str ):
        if data.get( field_name ) is not None:
            data[field_name] = Camera.parse_date( data[field_name] )

    @staticmethod
    def validate_image_capture_type( data: dict, field_name: str ):
        if data.get( field_name ) is not None:
            data[field_name] = ImageCaptureType( data[field_name] )

    @staticmethod
    def validate_int( data: dict, field_name: str ):
        if data.get( field_name ) is not None:
            data[field_name] = int( data[field_name] )

    @staticmethod
    def validate_owner( data: dict, field_name: str, owners: list[Owner] ):
        if data.get( field_name ):
            data[field_name] = [ owner for owner in owners if owner.name == data[field_name].strip() ][0]
