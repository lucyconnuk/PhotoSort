
import pytest

from classes.ImageCaptureType import ImageCaptureType

test_validate_from_dict_field_data = [
    ( [ { "image_capture_type": "Film" }, None ], { "image_capture_type": "Film" } ),
    ( [ { "image_capture_type": "Film" }, "unknown" ], { "image_capture_type": "Film" } ),
    ( [ { "image_capture_type": "Film" }, "image_capture_type" ], { "image_capture_type": ImageCaptureType.Film } ),
    ( [ { "image_capture_type": "film" }, "image_capture_type" ], { "image_capture_type": "film" } ),
    ( [ { "image_capture_type": "Digital" }, "image_capture_type" ], { "image_capture_type": ImageCaptureType.Digital } ),
    ( [ { "image_capture_type": "digital" }, "image_capture_type" ], { "image_capture_type": "digital" } ),
]

@pytest.mark.parametrize( "args, expected", test_validate_from_dict_field_data )
def test_validate_from_dict_field( args, expected ):
    ImageCaptureType.validate_from_dict_field( args[0], args[1] )
    assert args[0] == expected
