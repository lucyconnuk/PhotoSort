from dataclasses import dataclass
from pathlib import Path

import pandas


# For additional coding notes, see Camera.py
@dataclass( frozen=True, slots=True )
class Owner:
    """
    A person who owns a Camera and the Images which it took.
    Has a Name, and a Directory where their Images are stored.
    """
    
    name: str
    directory: str

    @classmethod
    def from_dict( cls, data: dict ) -> Owner:
        """
        Create Owner from dictionary of values
        """
        return cls(**data)

    @staticmethod
    def dataframe_to_list( owners_df: pandas.DataFrame ) -> list[Owner]:
        """
        Convert Owner data from dataframe to list of Owners.
        """
        owners_df = owners_df.replace( { float('nan'): None } )
        owners_ld = owners_df.to_dict( orient="records" )
        return [ Owner.from_dict( record ) for record in owners_ld ]

    @staticmethod
    def get_all( file_path: str ) -> list[Owner]:
        """
        Given a path to a csv file containing Owner data, return a list of Owners.
        """
        owner_data_file = Path( file_path )
        owners_df = Owner.load_all( owner_data_file )
        return Owner.dataframe_to_list( owners_df )
    
    @staticmethod
    def load_all( owner_data_file: Path ) -> pandas.DataFrame:
        """
        Get Owner data from csv file.
        """
        return pandas.read_csv( 
            owner_data_file
        )
