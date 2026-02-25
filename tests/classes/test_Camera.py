from classes.Camera import Camera
from datetime import date
import pytest

@pytest.mark.skip("Not written")
def test_from_dict():
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
