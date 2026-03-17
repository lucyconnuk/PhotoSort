
import pandas

from classes.Owner import Owner


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
