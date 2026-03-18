from datetime import date

import pandas
import pytest

from classes.Camera import Camera
from classes.ImageCaptureType import ImageCaptureType
from tests.data.TestData import TestData

test_get_matching_path_formats_data = [
    ( [ TestData.c_canon100, TestData.pf_list ], [ TestData.pf_alice_digital ] ),
    ( [ TestData.c_filmscan6, TestData.pf_list ], [ TestData.pf_alice_film ] ),
    ( [ TestData.c_nikon2, TestData.pf_list ], [ TestData.pf_bob_digital ] ),
]

@pytest.mark.parametrize( "args, expected", test_get_matching_path_formats_data )
def test_get_matching_path_formats( args, expected ):
    assert args[0].get_matching_path_formats( args[1] ) == expected

test_modify_path_data = [
    ( TestData.c_canon100, "asdf/Digital/hjkl" ),
    ( TestData.c_filmscan6, "asdf/Film/hjkl" ),
    ( TestData.c_empty, "asdf/UnknownICT/hjkl" ),
]

@pytest.mark.parametrize( "args, expected", test_modify_path_data )
def test_modify_path( args, expected ):
    assert args.modify_path( r"asdf/{ict}/hjkl" ) == expected

def test_dataframe_to_list():
    data = {
        "make": [ "Canon", "Nikon", "FilmScan" ],
        "model": [ "100", "2", "6" ],
        "image_capture_type": [ "Digital", "Digital", "Film" ],
        "owner": [ "Alice", "Bob", "Carol" ],
        "instance": [ "1", float('nan'), float('nan') ],
        "from_date": [ "2001-02", "2001-02-03", float('nan') ],
        "to_date": [ "2011-02", "2011-02-03", float('nan') ],
    }
    data_frame = pandas.DataFrame( data )
    assert Camera.dataframe_to_list( data_frame, TestData.owner_list ) == [
        Camera( "Canon", "100", ImageCaptureType.Digital, TestData.o_alice, 1, date( 2001, 2, 1 ) , date( 2011, 2, 1 ) ), ### TODO - should probably return last day of month
        Camera( "Nikon", "2", ImageCaptureType.Digital, TestData.o_bob, None, date( 2001, 2, 3 ), date( 2011, 2, 3 ) ),
        Camera( "FilmScan", "6", ImageCaptureType.Film, TestData.o_carol, None, None, None ),
    ]

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

test_validate_date_data = [
    ( [ { "from_date": "1994-05" }, None ], { "from_date": "1994-05" } ),
    ( [ { "from_date": "1994-05" }, "unknown" ], { "from_date": "1994-05" } ),
    ( [ { "from_date": "1994-05" }, "from_date" ], { "from_date": date( 1994, 5, 1 ) } ),
    ( [ { "from_date": "1969-08-31" }, "from_date" ], { "from_date": date( 1969, 8, 31 ) } ),
    ( [ { "from_date": "1969-08-31xxx" }, "from_date" ], { "from_date": None } ),
]

@pytest.mark.parametrize( "args, expected", test_validate_date_data )
def test_validate_date( args, expected ):
    if len(args) < 3:
        Camera.validate_date( args[0], args[1] )
    else:
        Camera.validate_date( args[0], args[1], args[2] )
    assert args[0] == expected

test_validate_int_data = [
    ( [ { "instance": "1" }, None ], { "instance": "1" } ),
    ( [ { "instance": "1" }, "unknown" ], { "instance": "1" } ),
    ( [ { "instance": "1" }, "instance" ], { "instance": 1 } ),
    ( [ { "instance": "0" }, "instance" ], { "instance": 0 } ),
    ( [ { "instance": "-1" }, "instance" ], { "instance": -1 } ),
]

@pytest.mark.parametrize( "args, expected", test_validate_int_data )
def test_validate_int( args, expected ):
    Camera.validate_int( args[0], args[1] )
    assert args[0] == expected

test_validate_owner_data = [
    ( [ { "owner": "Alice" }, None ], { "owner": "Alice" } ),
    ( [ { "owner": "Alice" }, "unknown" ], { "owner": "Alice" } ),
    ( [ { "owner": "Alice" }, "owner" ], { "owner": TestData.o_alice } ),
    ( [ { "owner": "alice" }, "owner" ], { "owner": "alice" } ),
    ( [ { "owner": "Bob" }, "owner" ], { "owner": TestData.o_bob } ),
    ( [ { "owner": "bob" }, "owner" ], { "owner": "bob" } ),
]

@pytest.mark.parametrize( "args, expected", test_validate_owner_data )
def test_validate_owner( args, expected ):
    Camera.validate_owner( args[0], args[1], TestData.owner_list )
    assert args[0] == expected
