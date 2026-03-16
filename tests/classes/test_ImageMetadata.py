from datetime import datetime

import piexif
import pytest

from classes.ImageMetadata import ImageMetadata


def test_from_path(mocker):

    # Create mock metadata to return from piexif.load()
    metadata_0th = [None] * 307
    metadata_0th[271] = b"Canon"
    metadata_0th[272] = b"EOS Rebel T6"
    metadata_0th[306] = b"2021:02:03 04:05:06"
    metadata = {
        "0th": metadata_0th
    }

    # Patch piexif.load() to return the mock metadata
    mocker.patch( "piexif.load", return_value = metadata )

    # Call the function under test with a dummy path
    im = ImageMetadata()
    result = im.from_path( "dummy" )

    # Check that piexif.load() was called once with the dummy path
    piexif.load.assert_called_once_with( "dummy" )

    # Check that it returned the correct result
    assert result.camera_make == "Canon"
    assert result.camera_model == "EOS Rebel T6"
    assert result.date_taken == datetime( 2021, 2, 3, 4, 5, 6 )

im_not_dict =                   ""
im_empty_dict =                 dict()
im_dict_with_undefined_section: dict[str, any] = { "section": None }
im_dict_with_empty_section:     dict[str, any] = { "section": [] }
im_dict_with_str_data:          dict[str, any] = { "section": [ "string data" ] }
im_dict_with_byte_data:         dict[str, any] = { "section": [ b"byte data" ] }

test_get_string_data = [

    # image_metadata is None
    ( [ None, None, None ], None ),

    # image_metadata is not a dictionary
    ( [ im_not_dict, None, None ], None ),
    
    # image_metadata is an empty dictionary
    ( [ im_empty_dict, None, None ], None ),
    
    # image_metadata has section but section is undefined
    ( [ im_dict_with_undefined_section, "section", 0 ], None ),
    
    # image_metadata has section but section is empty
    ( [ im_dict_with_empty_section, "section", 0 ], None ),

    # image_metadata has section with enough data
    ( [ im_dict_with_str_data, "section", 0 ], "string data" ),
    ( [ im_dict_with_byte_data, "section", 0 ], "byte data" ),

    # image_metadata has section with not enough data
    ( [ im_dict_with_str_data, "section", 1 ], None ),
]

@pytest.mark.parametrize( "args, expected", test_get_string_data )
def test_get_string( args, expected ):
    assert ImageMetadata.get_string( *args ) == expected

test_get_date_data = [
    ( None, None ),
    ( "", None ),
    ( "2021:02:03 04:05:06", datetime( 2021, 2, 3, 4, 5, 6 ) ),
]

@pytest.mark.parametrize( "args, expected", test_get_date_data )
def test_get_date( args, expected ):
    assert ImageMetadata.get_date( args ) == expected
