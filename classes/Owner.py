from dataclasses import dataclass
from pathlib import Path
import pandas

@dataclass(frozen=True)
class Owner:
    
    name: str
    directory: str

    # Coding note: cls means "this class"
    # See https://realpython.com/ref/glossary/cls/
    @classmethod
    def from_dict( cls, data: dict ) -> Owner:
        return cls(**data)

    @staticmethod
    def dataframe_to_list( owners_df: pandas.DataFrame ) -> list[Owner]:
        """
        Convert Owner data from dataframe to list of Owners.
        """

        # Pandas fills empty spaces in the dataframe with the floating point value 'nan'.
        # Replace these with None, using pandas.DataFrame.replace.
        # See https://stackoverflow.com/a/54403705 
        owners_df = owners_df.replace( { float('nan'): None } )

        # Convert dataframe into list of records, where each record is a dictionary of key-value pairs,
        # using pandas.DataFrame.to_dict( orient="records" ).
        owners_ld = owners_df.to_dict( orient="records" )

        # Convert list of records into list of Owner objects, using a list comprehension,
        # and return the list.
        # See https://realpython.com/list-comprehension-python/ 
        return [ Owner.from_dict( record ) for record in owners_ld ]

    @staticmethod
    def get_all( file_path: str ) -> list[Owner]:
        owner_data_file = Path( file_path )
        owners_df = Owner.load_all( owner_data_file )
        return Owner.dataframe_to_list( owners_df )
    
    @staticmethod
    def load_all( owner_data_file: Path ) -> pandas.DataFrame:
        """
        Get all Owner data from csv file owner_data_file.
        """
        return pandas.read_csv( 
            owner_data_file
        )
