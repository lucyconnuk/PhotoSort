import photosort
import pytest
from pathlib import Path

test_check_valid_path_data = [

    # Path() returns the current directory.
    ( Path(), [True, ". is a directory"] ),

    # Path(__file__) returns the current file.
    ( Path(__file__), [False, f"{__file__} is a file"] ),

    # No easy way to return something which exists but is not a directory or a 
    # file, so we're not testing that.
    
    # randomfilepath198hco8c3hr8hf98hr984h9h9438h should not exist.
    ( Path("randomfilepath198hco8c3hr8hf98hr984h9h9438h"), [False, "randomfilepath198hco8c3hr8hf98hr984h9h9438h does not exist"] ),
]

@pytest.mark.parametrize( "args, expected", test_check_valid_path_data )
def test_check_valid_path( args, expected ):
    (valid, message) = photosort.check_valid_path( args )
    assert valid == expected[0]
    assert message == expected[1]
