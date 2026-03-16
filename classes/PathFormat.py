from dataclasses import dataclass
from pathlib import Path

import pandas

from classes.ImageCaptureType import ImageCaptureType


# For additional coding notes, see Camera.py
@dataclass(frozen=True)
class PathFormat:
    """
    A format for Image Expected Paths.
    Contains tokens which can be replaced by Owner, Camera or Image data to get the Expected Path for an Image.
    """
    
    owner_name: str
    image_capture_type: ImageCaptureType
    template: str

    @classmethod
    def from_dict( cls, data: dict ) -> PathFormat:
        """
        Create PathFormat from dictionary of values
        """
        return cls(**data)

    @staticmethod
    def dataframe_to_list( path_formats_df: pandas.DataFrame ) -> list[PathFormat]:
        """
        Convert PathFormat data from dataframe to list of PathFormats.
        """
        path_formats_df = path_formats_df.replace( { float('nan'): None } )
        path_formats_ld = path_formats_df.to_dict( orient="records" )
        return [ PathFormat.from_dict( record ) for record in path_formats_ld ]

    @staticmethod
    def get_all( file_path: str ) -> list[PathFormat]:
        """
        Given a path to a csv file containing PathFormat data, return a list of PathFormats.
        """
        path_format_data_file = Path( file_path )
        path_formats_df = PathFormat.load_all( path_format_data_file )
        return PathFormat.dataframe_to_list( path_formats_df )
    
    @staticmethod
    def load_all( path_format_data_file: Path ) -> pandas.DataFrame:
        """
        Get PathFormat data from csv file.
        """
        return pandas.read_csv( 
            path_format_data_file
        )
