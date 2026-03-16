
import pytest

from tests.data.TestData import TestData

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
    assert args[0].get_matching_cameras( args[1] ) == expected
