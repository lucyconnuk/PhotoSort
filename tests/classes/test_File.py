from pathlib import Path

import pytest

from classes.File import File

test_check_valid_path_data = [

    # Path() returns the current directory.
    ( Path(), [True, "Directory is: ."] ),

    # Path(__file__) returns the current file.
    ( Path(__file__), [False, f"{__file__} is a file"] ),

    # randomfilepath198hco8c3hr8hf98hr984h9h9438h should not exist.
    ( Path("randomfilepath198hco8c3hr8hf98hr984h9h9438h"), [False, "randomfilepath198hco8c3hr8hf98hr984h9h9438h does not exist"] ),
]

@pytest.mark.parametrize( "args, expected", test_check_valid_path_data )
def test_check_valid_path( args, expected ):
    (valid, message) = File.check_valid_path( args )
    assert valid == expected[0]
    assert message == expected[1]

def test_check_valid_path_unknown_type( mocker ):

    # Create a mock_path, and patch its methods so that it looks like
    # an object which exists but is not a directory or a file.
    mock_path = Path()
    mocker.patch( "pathlib.Path.exists", return_value = True )
    mocker.patch( "pathlib.Path.is_dir", return_value = False )
    mocker.patch( "pathlib.Path.is_file", return_value = False )

    # Call the function under test with mock_path
    (valid, message) = File.check_valid_path( mock_path )

    # Check that mock_path functions were called once
    mock_path.exists.assert_called_once()
    mock_path.is_dir.assert_called_once()
    mock_path.is_file.assert_called_once()

    # Check that it returned the correct result
    assert valid == False
    assert message == f"{mock_path} exists but is not a directory or a file"

def test_get_files():
    current_directory = Path()
    current_file = Path(__file__)
    paths = [ current_directory, current_file ]
    assert File.get_files( paths ) == [ current_file ]

def test_get_image_files():
    current_directory = Path()
    current_file = Path(__file__)
    image_file_1 = Path( "test.jpg" )
    image_file_2 = Path( "test.tiff" )
    paths = [ current_directory, current_file, image_file_1, image_file_2 ]
    assert File.get_image_files( paths ) == [ image_file_1, image_file_2 ]

def test_get_xmp_files():
    current_directory = Path()
    current_file = Path(__file__)
    xmp_file_1 = Path( "test.jpg.xmp" )
    xmp_file_2 = Path( "test.tiff.xmp" )
    paths = [ current_directory, current_file, xmp_file_1, xmp_file_2 ]
    assert File.get_xmp_files( paths ) == [ xmp_file_1, xmp_file_2 ]
