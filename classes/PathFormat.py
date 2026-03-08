from classes.ImageCaptureType import ImageCaptureType
from dataclasses import dataclass
from pathlib import Path
import pandas

@dataclass(frozen=True)
class PathFormat:
    
    owner_name: str
    image_capture_type: ImageCaptureType
    path_format: str

    # Coding note: cls means "this class"
    # See https://realpython.com/ref/glossary/cls/
    @classmethod
    def from_dict( cls, data: dict ) -> PathFormat:
        return cls(**data)

    @staticmethod
    def dataframe_to_list( path_formats_df: pandas.DataFrame ) -> list[PathFormat]:
        """
        Convert PathFormat data from dataframe to list of PathFormats.
        """

        # Pandas fills empty spaces in the dataframe with the floating point value 'nan'.
        # Replace these with None, using pandas.DataFrame.replace.
        # See https://stackoverflow.com/a/54403705 
        path_formats_df = path_formats_df.replace( { float('nan'): None } )

        # Convert dataframe into list of records, where each record is a dictionary of key-value pairs,
        # using pandas.DataFrame.to_dict( orient="records" ).
        path_formats_ld = path_formats_df.to_dict( orient="records" )

        # Convert list of records into list of PathFormat objects, using a list comprehension,
        # and return the list.
        # See https://realpython.com/list-comprehension-python/ 
        return [ PathFormat.from_dict( record ) for record in path_formats_ld ]

    @staticmethod
    def get_all( file_path: str ) -> list[PathFormat]:
        path_format_data_file = Path( file_path )
        path_formats_df = PathFormat.load_all( path_format_data_file )
        return PathFormat.dataframe_to_list( path_formats_df )
    
    @staticmethod
    def load_all( path_format_data_file: Path ) -> pandas.DataFrame:
        """
        Get all PathFormat data from csv file path_format_data_file.
        """
        return pandas.read_csv( 
            path_format_data_file
        )

    # @staticmethod
    # def get_matching( owner_name: str, image_capture_type: ImageCaptureType ) -> str:
    #     for pf in PathFormat.get_all():
    #         if pf.owner_name == owner_name and pf.image_capture_type == image_capture_type:
    #             return pf.path_format
    #         return None
