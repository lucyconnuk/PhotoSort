from datetime import date

import pytest

from classes.Camera import Camera
from tests.data.TestData import TestData


@pytest.mark.skip("Not written")
def test_from_dict():
    pass

test_get_matching_path_formats_data = [
    ( [ TestData.c_canon100, TestData.pf_list ], [ TestData.pf_canon100 ] ),
]

@pytest.mark.parametrize( "args, expected", test_get_matching_path_formats_data )
def test_get_matching_path_formats( args, expected ):
    assert args[0].get_matching_path_formats( args[1] ) == expected

@pytest.mark.skip("Not written")
def test_dataframe_to_list():
    pass

@pytest.mark.skip("Not written")
def test_get_all():
    pass

@pytest.mark.skip("Not written")
def test_load_all():
    pass

test_parse_date_data = [

    # date_str is empty
    ( "", None ),

    # date_str is a valid year-month date
    ( "1994-05", date( 1994, 5, 1 ) ),
    
    # date_str is a valid year-month-day date
    ( "1969-08-31", date( 1969, 8, 31 ) ),

    # date_str is not a valid date
    ( "1969-08-31xxx", None ),
]

@pytest.mark.parametrize( "args, expected", test_parse_date_data )
def test_parse_date( args, expected ):
    assert Camera.parse_date( args ) == expected

@pytest.mark.skip("Not written")
def test_validate_date():
    pass

@pytest.mark.skip("Not written")
def test_validate_image_capture_type():
    pass

@pytest.mark.skip("Not written")
def test_validate_int():
    pass

@pytest.mark.skip("Not written")
def test_validate_owner():
    pass
