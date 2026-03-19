
from pathlib import Path

import pytest

from classes.AppLogger import logger
from classes.Image import Image
from classes.PathFormat import PathFormat
from tests.data.TestData import TestData

test_get_expected_path_data = [
    ### TODO get rid of dependency on ROOT_DIR
    ( TestData.i2_canon100, Path( r"C:/Users/Public/Pictures/PhotoOrganizer/Digital/Alice-photos/UnknownYearMonthDay/testpath" ) ),
    ( TestData.i2_nikon2, Path( r"C:/Users/Public/Pictures/PhotoOrganizer/Digital/Bob-pics/UnknownYearMonthDay/testpath" ) ),
    ( TestData.i2_canon500_teens, Path( r"C:/Users/Public/Pictures/PhotoOrganizer/Digital/Alice-photos/2011-01-01/testpath" ) ),
    ( TestData.i2_canon500_twenties, Path( r"C:/Users/Public/Pictures/PhotoOrganizer/Digital/Bob-pics/2021-01-01/testpath" ) ),
    ( TestData.i2_filmscan6, Path( r"C:/Users/Public/Pictures/PhotoOrganizer/Film/Alice-photos/UnknownYearMonthDay/testpath" ) ),
]

@pytest.mark.parametrize( "args, expected", test_get_expected_path_data )
def test_get_expected_path( args, expected ):
    test_image: Image = args
    test_path_format = PathFormat( None, None, r"{ict}\{directory}\{yyyy-mm-dd}" )
    actual = test_image.get_expected_path( test_path_format )
    assert actual == expected

test_get_matching_cameras_data = [

    ## Test cases for image metadata or camera list not present

    # Image.metadata = None and cameras = []
    ( [ TestData.i_no_metadata, [] ], [] ),

    # Image.metadata = None 
    ( [ TestData.i_no_metadata, TestData.camera_list ], [] ),

    # cameras = []
    ( [ TestData.i_all_metadata, [] ], [] ),

    # Image.metadata.camera_make = None
    ( [ TestData.i_no_camera_make, TestData.camera_list ], [] ),

    # Image.metadata.camera_model = None 
    ( [ TestData.i_no_camera_model, TestData.camera_list ], [] ),

    # Image.metadata.date_taken = None 
    ( [ TestData.i_no_date_taken, TestData.camera_list ], [] ),

    ## Test cases for image metadata and camera list present

    # 1 matching camera
    ( [ TestData.i_canon100, TestData.camera_list ], [ TestData.c_canon100 ] ),
    ( [ TestData.i_nikon2, TestData.camera_list ], [ TestData.c_nikon2 ] ),

    # 2 matching cameras as taken date is unknown
    ( [ TestData.i_canon300, TestData.camera_list ], [ TestData.c_canon300_unknown_a, TestData.c_canon300_unknown_b ] ),

    # 2 matching cameras as cameras owned at same time
    ( [ TestData.i_nikon4_noughties, TestData.camera_list ], [ TestData.c_nikon4_noughties_a, TestData.c_nikon4_noughties_b ] ),

    # 1 matching camera as taken date is known
    ( [ TestData.i_canon500_teens, TestData.camera_list ], [ TestData.c_canon500_teens ] ),
    ( [ TestData.i_canon500_twenties, TestData.camera_list ], [ TestData.c_canon500_twenties ] ),

    # 1 matching Film camera
    ( [ TestData.i_filmscan6, TestData.camera_list ], [ TestData.c_filmscan6 ] ),

]

@pytest.mark.parametrize( "args, expected", test_get_matching_cameras_data )
def test_get_matching_cameras( args, expected ):
    test_image: Image = args[0]
    assert test_image.get_matching_cameras( args[1] ) == expected

def test_get_path_format_no_match( mocker ):
    
    # Create new test Image from Image File and Camera (in case we modify it)
    test_image: Image = Image( TestData.if_canon100, TestData.c_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Camera.Camera.get_matching_path_formats", return_value = [] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    actual = test_image.get_path_format()

    # Check that the following functions were called and path format was NOT set
    test_image.camera.get_matching_path_formats.assert_called_once()
    logger.warning.assert_called_once_with( "Found 0 possible path formats for Alice Digital" )
    assert actual == None

def test_get_path_format_1_match( mocker ):
    
    # Create new test Image from Image File and Camera (in case we modify it)
    test_image: Image = Image( TestData.if_canon100, TestData.c_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Camera.Camera.get_matching_path_formats", return_value = [ TestData.pf_alice_digital ] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    actual = test_image.get_path_format()

    # Check that the following functions were called (or not) and path format was set
    test_image.camera.get_matching_path_formats.assert_called_once()
    logger.warning.assert_not_called()
    assert actual == TestData.pf_alice_digital

def test_get_path_format_2_matches( mocker ):
    
    # Create new test Image from Image File and Camera (in case we modify it)
    test_image: Image = Image( TestData.if_canon100, TestData.c_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Camera.Camera.get_matching_path_formats", 
        return_value = [ TestData.pf_alice_digital, TestData.pf_alice_digital ] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    actual = test_image.get_path_format()

    # Check that the following functions were called and path format was NOT set
    test_image.camera.get_matching_path_formats.assert_called_once()
    logger.warning.assert_called_once_with( "Found 2 possible path formats for Alice Digital" )
    assert actual == None

def test_load(mocker):
    
    # Create new test Image from Image File (in case we modify it)
    test_image: Image = Image( TestData.if_all_metadata )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.ImageFile.ImageFile.load_metadata" )
    mocker.patch( "classes.Image.Image.load_camera" )
    mocker.patch( "classes.Image.Image.load_image_expected_path" )

    # Call the function under test
    test_image.load()

    # Check that the following functions were each called once
    test_image.image_file.load_metadata.assert_called_once()
    test_image.load_camera.assert_called_once()
    test_image.load_image_expected_path.assert_called_once()

test_load_camera_no_match_data = [
    ( TestData.if_no_camera_make, "Found 0 possible cameras for None b 2001-01-01 00:00:00" ),
    ( TestData.if_no_camera_model, "Found 0 possible cameras for a None 2001-01-01 00:00:00" ),
    ( TestData.if_no_date_taken, "Found 0 possible cameras for a b None" ),
    ( TestData.if_all_metadata, "Found 0 possible cameras for a b 2001-01-01 00:00:00" ),
]

@pytest.mark.parametrize( "args, expected", test_load_camera_no_match_data )
def test_load_camera_no_match( mocker, args, expected ):
    
    # Create new test Image from Image File (in case we modify it)
    test_image: Image = Image( args )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_matching_cameras", return_value = [] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    test_image.load_camera()

    # Check that the following functions were called and camera was NOT set
    test_image.get_matching_cameras.assert_called_once()
    logger.warning.assert_called_once_with( expected )
    assert test_image.camera == None

def test_load_camera_1_match( mocker ):
    
    # Create new test Image from Image File (in case we modify it)
    test_image: Image = Image( TestData.if_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_matching_cameras", return_value = [ TestData.c_canon100 ] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    test_image.load_camera()

    # Check that the following functions were called and camera was set
    test_image.get_matching_cameras.assert_called_once()
    logger.warning.assert_not_called()
    assert test_image.camera == TestData.c_canon100

def test_load_camera_2_matches( mocker ):
    
    # Create new test Image from Image File (in case we modify it)
    test_image: Image = Image( TestData.if_nikon4_noughties )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_matching_cameras", 
        return_value = [ TestData.c_nikon4_noughties_a, TestData.c_nikon4_noughties_b ] )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    test_image.load_camera()

    # Check that the following functions were called and camera was NOT set
    test_image.get_matching_cameras.assert_called_once()
    logger.warning.assert_called_once_with( "Found 2 possible cameras for Nikon 4 2001-01-01 00:00:00" )
    assert test_image.camera == None

def test_load_image_expected_path_no_camera(mocker):
    
    # Create new test Image from Image File (in case we modify it)
    test_image: Image = Image( TestData.if_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_path_format" )
    mocker.patch( "classes.Image.Image.get_expected_path" )
    mocker.patch( "classes.AppLogger.logger.info" )

    # Call the function under test
    test_image.load_image_expected_path()

    # Check that the following functions were called (or not) and expected_path was set (or not)
    test_image.get_path_format.assert_not_called()
    test_image.get_expected_path.assert_not_called()
    logger.info.assert_not_called()
    assert test_image.expected_path == None

def test_load_image_expected_path_no_path_format(mocker):
    
    # Create new test Image from Image File and Camera (in case we modify it)
    test_image: Image = Image( TestData.if_canon100, TestData.c_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_path_format", return_value = None )
    mocker.patch( "classes.Image.Image.get_expected_path" )
    mocker.patch( "classes.AppLogger.logger.info" )

    # Call the function under test
    test_image.load_image_expected_path()

    # Check that the following functions were called (or not) and expected_path was set (or not)
    test_image.get_path_format.assert_called_once()
    test_image.get_expected_path.assert_not_called()
    logger.info.assert_not_called()
    assert test_image.expected_path == None

def test_load_image_expected_path(mocker):
    
    # Create new test Image from Image File and Camera (in case we modify it)
    test_image: Image = Image( TestData.if_canon100, TestData.c_canon100 )

    # Patch functions which will be called by the function under test
    mocker.patch( "classes.Image.Image.get_path_format", return_value = "valid_path_format" )
    mocker.patch( "classes.Image.Image.get_expected_path", return_value = "valid_expected_path" )
    mocker.patch( "classes.AppLogger.logger.info" )

    # Call the function under test
    test_image.load_image_expected_path()

    # Check that the following functions were called (or not) and expected_path was set (or not)
    test_image.get_path_format.assert_called_once()
    test_image.get_expected_path.assert_called_once_with( "valid_path_format" )
    logger.info.assert_has_calls( [
        mocker.call("Expected path: valid_expected_path"), 
        mocker.call("Expected path == Actual path: False")
    ] )
    assert test_image.expected_path == "valid_expected_path"
