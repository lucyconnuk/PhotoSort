from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import Optional
from pathlib import Path
import pandas

# TODO: 
# - review comments
# - write tests

# Coding note: frozen and slots used to make class more type-safe and memory-efficient.
# See https://docs.python.org/3/library/dataclasses.html#frozen-instances
# and https://github.com/orgs/community/discussions/168147 
@dataclass( frozen=True, slots=True )
class Camera:
    make: str
    model: str
    image_capture_type: ImageCaptureType
    instance: Optional[int] = 0
    owner: Optional[Owner] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None

    # Coding note: cls means "this class"
    # See https://realpython.com/ref/glossary/cls/
    @classmethod
    def from_dict( cls, data: dict ) -> Camera:
        if data.get( "image_capture_type" ) is not None:
            data["image_capture_type"] = ImageCaptureType( data["image_capture_type"] )

        if data.get( "instance" ) is not None:
            data["instance"] = int( data["instance"] )

        if data.get( "owner" ):
            data["owner"] = Owner( name=data["owner"].strip() )

        if data.get( "from_date" ) is not None:
            data["from_date"] = cls.parse_date( data["from_date"] )

        if data.get( "to_date" ) is not None:
            data["to_date"] = cls.parse_date( data["to_date"] )

        # Coding note: **data means "all the values in data"
        # So here we are passing the values in the data dict to the cls() method
        # and returning the return value.
        return cls(**data)

    @staticmethod
    def load_all( camera_data_file: Path ) -> list[Camera]:
        """
        Load all Camera data from a csv file and return a list of Cameras.

        Parameters:
            camera_data_file (Path): Path to camera data file

        Returns:
            list[Camera]: list of Cameras.
        """

        # Get data from csv file into dataframe, using pandas.read_csv.
        cameras_df = pandas.read_csv( 
            camera_data_file,
            parse_dates=[ "to_date", "from_date" ],
            date_format="yyyy-MM-dd"
        )

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
        return [ Camera.from_dict( record ) for record in cameras_ld ]

    @staticmethod
    def parse_date( date_str: str ) -> Optional[date]:
        camera_date = None
        try:
            camera_date = date.strptime( date_str, "%Y-%m-%d" ) 
        except ValueError:
            try:
                camera_date = date.strptime( date_str, "%Y-%m" ) 
            except ValueError:
                camera_date = None
        return camera_date
