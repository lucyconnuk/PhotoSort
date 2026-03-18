from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

import pandas
from dateutil.relativedelta import relativedelta

from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from classes.PathFormat import PathFormat
from classes.PathModifier import PathModifier

DATA_FILE_DATE_COLUMNS = [ "to_date", "from_date" ]
DATA_FILE_DATE_FORMAT = "yyyy-MM-dd"
PARSE_DATE_FORMAT = r"%Y-%m-%d"
PARSE_DATE_FORMAT_SHORT = r"%Y-%m"
ICT_PATH_TOKEN = r"{ict}"
ICT_PATH_DEFAULT = "UnknownICT"


# Make this class type-safe and memory-efficient, using frozen and slots parameters.
# See https://docs.python.org/3/library/dataclasses.html#frozen-instances
# and https://github.com/orgs/community/discussions/168147 
@dataclass( frozen=True, slots=True )
class Camera(PathModifier):
    """
    A physical device which captures Images. 
    Image Capture Type can be straight to Digital, or scanned from Film.
    Identifiable by its Make and Model, and if necessary an Instance no.
    Has an Owner and optional usage From and To Dates.
    """
    make: str
    model: str
    image_capture_type: ImageCaptureType
    owner: Owner
    instance: Optional[int] = 0
    from_date: Optional[date] = None
    to_date: Optional[date] = None

    # Coding notes: 
    # @classmethod - See https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-a-beginner 
    # cls means "this class" - See https://realpython.com/ref/glossary/cls/
    @classmethod
    def from_dict( cls, data: dict, owners: list[Owner] ) -> Camera: # pragma: no cover
        """
        Create Camera from dictionary of values
        """

        ImageCaptureType.validate_from_dict_field( data, "image_capture_type" )
        Camera.validate_owner( data, "owner", owners )
        Camera.validate_int( data, "instance" )
        Camera.validate_date( data, "from_date" )
        Camera.validate_date( data, "to_date", True )

        # Coding note: **data means "all the values in data"
        # So here we are passing ALL of the values in the data dict, including the ones we've just validated, to the cls() method
        # and returning the return value.
        return cls(**data)

    # instance method
    def get_matching_path_formats( self, path_formats: list[PathFormat] ) -> list[PathFormat]:
        """
        Get path_formats which match owner and image_capture_type from a list of path_formats
        """
        possible_path_formats = []
        # Filter by owner and image_capture_type
        possible_path_formats = [ 
            pf for pf in path_formats
            if pf != None
            and pf.owner_name == self.owner.name
            and pf.image_capture_type == self.image_capture_type
        ]
        return possible_path_formats

    # instance method
    def modify_path( self, template: str ) -> str:
        replacement_string = ICT_PATH_DEFAULT
        try:
            replacement_string = self.image_capture_type.value
        except:
            # Could log here if required
            pass
        return template.replace( ICT_PATH_TOKEN, replacement_string )

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
    def get_all( file_path: str, owners: list[Owner] ) -> list[Camera]: # pragma: no cover
        """
        Given a path to a csv file containing Camera data, return a list of Cameras.
        """
        camera_data_file = Path( file_path )
        cameras_df = Camera.load_all( camera_data_file )
        return Camera.dataframe_to_list( cameras_df, owners )
    
    @staticmethod
    def load_all( camera_data_file: Path ) -> pandas.DataFrame: # pragma: no cover
        """
        Get Camera data from csv file.
        """
        return pandas.read_csv( 
            camera_data_file,
            parse_dates = DATA_FILE_DATE_COLUMNS,
            date_format = DATA_FILE_DATE_FORMAT
        )

    @staticmethod
    def parse_date( date_str: str, end_of_month: bool = False ) -> Optional[date]:
        """
        Parse a date string, which can be in year-month-day or year-month format,
        and return a valid date, or None.
        """
        result = None
        try:
            result = date.strptime( date_str, PARSE_DATE_FORMAT ) 
        except ValueError:
            try:
                result = date.strptime( date_str, PARSE_DATE_FORMAT_SHORT ) 
            except ValueError:
                result = None
            else:
                if end_of_month:
                    result = result + relativedelta( months = 1 )
                    result = result + relativedelta( days = -1 )

        return result

    @staticmethod
    def validate_date( data: dict, field_name: str, end_of_month: bool = False ):
        if data.get( field_name ) is not None:
            data[field_name] = Camera.parse_date( data[field_name], end_of_month )

    @staticmethod
    def validate_int( data: dict, field_name: str ):
        if data.get( field_name ) is not None:
            data[field_name] = int( data[field_name] )

    @staticmethod
    def validate_owner( data: dict, field_name: str, owners: list[Owner] ):
        if data.get( field_name ):
            try:
                data[field_name] = [ owner for owner in owners if owner.name == data[field_name].strip() ][0]
            except:
                pass
