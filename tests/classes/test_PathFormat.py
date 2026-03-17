
import pandas
import pytest

from classes.ImageCaptureType import ImageCaptureType
from classes.PathFormat import PathFormat


def test_from_dict():
    result = PathFormat.from_dict( { "owner_name": "Alice", "image_capture_type": "Digital", "template": r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" } )
    assert result.owner_name == "Alice"
    assert result.image_capture_type == ImageCaptureType.Digital
    assert result.template ==  r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}"

def test_dataframe_to_list():
    data = {
        "owner_name": [ "Alice", "Bob", "Carol" ],
        "image_capture_type": [ "Digital", "Film", float('nan') ],
        "template": [ "atemplate", "btemplate", "ctemplate"]
    }
    data_frame = pandas.DataFrame( data )
    assert PathFormat.dataframe_to_list( data_frame ) == [
        PathFormat( "Alice", ImageCaptureType.Digital, "atemplate" ),
        PathFormat( "Bob", ImageCaptureType.Film, "btemplate" ),
        PathFormat( "Carol", None, "ctemplate" )
    ]

test_validate_image_capture_type_data = [
    ( [ { "image_capture_type": "Film" }, None ], { "image_capture_type": "Film" } ),
    ( [ { "image_capture_type": "Film" }, "unknown" ], { "image_capture_type": "Film" } ),
    ( [ { "image_capture_type": "Film" }, "image_capture_type" ], { "image_capture_type": ImageCaptureType.Film } ),
    ( [ { "image_capture_type": "film" }, "image_capture_type" ], { "image_capture_type": "film" } ),
    ( [ { "image_capture_type": "Digital" }, "image_capture_type" ], { "image_capture_type": ImageCaptureType.Digital } ),
    ( [ { "image_capture_type": "digital" }, "image_capture_type" ], { "image_capture_type": "digital" } ),
]

@pytest.mark.parametrize( "args, expected", test_validate_image_capture_type_data )
def test_validate_image_capture_type( args, expected ):
    PathFormat.validate_image_capture_type( args[0], args[1] )
    assert args[0] == expected
