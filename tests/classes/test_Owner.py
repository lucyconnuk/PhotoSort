
import pandas
import pytest

from classes.Owner import Owner
from tests.data.TestData import TestData

test_modify_path_data = [
    ( TestData.o_alice, "asdf/Alice-photos/hjkl" ),
    ( TestData.o_bob, "asdf/Bob-pics/hjkl" ),
    ( TestData.o_empty, "asdf/UnknownOwner/hjkl" ),
]

@pytest.mark.parametrize( "args, expected", test_modify_path_data )
def test_modify_path( args, expected ):
    assert args.modify_path( r"asdf/{directory}/hjkl" ) == expected

def test_from_dict():
    result = Owner.from_dict( { "name": "Alice", "directory": "AlicePics" } )
    assert result.name == "Alice"
    assert result.directory == "AlicePics"

def test_dataframe_to_list():
    data = {
        "name": [ "Alice", "Bob", "Carol" ],
        "directory": [ "AlicePics", "BobPhotos", float('nan') ]
    }
    data_frame = pandas.DataFrame( data )
    assert Owner.dataframe_to_list( data_frame ) == [
        Owner( "Alice", "AlicePics" ),
        Owner( "Bob", "BobPhotos" ),
        Owner( "Carol", None ),
    ]
