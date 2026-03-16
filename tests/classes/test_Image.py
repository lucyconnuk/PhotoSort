from datetime import datetime

import pytest

from classes.Camera import Camera
from classes.Image import Image
from classes.ImageCaptureType import ImageCaptureType
from classes.ImageFile import ImageFile
from classes.ImageMetadata import ImageMetadata
from classes.Owner import Owner

## Owners used in tests

o_alice = Owner( "Alice", "Alice-photos" )
o_bob = Owner( "Bob", "Bob-pics" )

## Cameras used in tests

# Type of camera only owned by Alice
c_canon100 = Camera( "Canon", "100", ImageCaptureType.Digital, o_alice )

# Type of camera only owned by Bob
c_nikon2 = Camera( "Nikon", "2", ImageCaptureType.Digital, o_bob )

# Same type of camera owned by both, times unknown
c_canon300_unknown_a = Camera( "Canon", "300", ImageCaptureType.Digital, o_alice )
c_canon300_unknown_b = Camera( "Canon", "300", ImageCaptureType.Digital, o_bob )

# Same type of camera owned by both at same time
c_nikon4_noughties_a = Camera( "Nikon", "4", ImageCaptureType.Digital, o_alice, 1, datetime( 2000, 1, 1 ), datetime( 2009, 12, 31) )
c_nikon4_noughties_b = Camera( "Nikon", "4", ImageCaptureType.Digital, o_bob, 1, datetime( 2000, 1, 1 ), datetime( 2009, 12, 31) )

# Same type of camera owned by both at different times
c_canon500_teens = Camera( "Canon", "500", ImageCaptureType.Digital, o_alice, 1, datetime( 2010, 1, 1 ), datetime( 2019, 12, 31) )
c_canon500_twenties = Camera( "Canon", "500", ImageCaptureType.Digital, o_bob, 1, datetime( 2020, 1, 1 ), datetime( 2029, 12, 31) )

# Film scanner
c_filmscan6 = Camera( "FilmScan", "6", ImageCaptureType.Film, o_alice )

camera_list = [ 
    c_canon100, 
    c_nikon2, 
    c_canon300_unknown_a, 
    c_canon300_unknown_b, 
    c_nikon4_noughties_a, 
    c_nikon4_noughties_b,
    c_canon500_teens,
    c_canon500_twenties,
    c_filmscan6
]

## Images used in tests

i_no_metadata =     Image()
i_no_camera_make =  Image( ImageFile( metadata = ImageMetadata( None, "b", datetime( 2001, 1, 1 ) ) ) )
i_no_camera_model = Image( ImageFile( metadata = ImageMetadata( "a", None, datetime( 2001, 1, 1 ) ) ) )
i_no_date_taken =   Image( ImageFile( metadata = ImageMetadata( "a", "b", None ) ) )
i_all_metadata =    Image( ImageFile( metadata = ImageMetadata( "a", "b", datetime( 2001, 1, 1 ) ) ) )

i_canon100 = Image( ImageFile( metadata = ImageMetadata( "Canon", "100", None ) ) )
i_nikon2 = Image( ImageFile( metadata = ImageMetadata( "Nikon", "2", None ) ) )
i_canon300 = Image( ImageFile( metadata = ImageMetadata( "Canon", "300", None ) ) )
i_nikon4_noughties = Image( ImageFile( metadata = ImageMetadata( "Nikon", "4", datetime( 2001, 1, 1 ) ) ) )
i_canon500_teens = Image( ImageFile( metadata = ImageMetadata( "Canon", "500", datetime( 2011, 1, 1 ) ) ) )
i_canon500_twenties = Image( ImageFile( metadata = ImageMetadata( "Canon", "500", datetime( 2021, 1, 1 ) ) ) )
i_filmscan6 = Image( ImageFile( metadata = ImageMetadata( "FilmScan", "6", None ) ) )

test_get_matching_cameras_data = [

    ## Test cases for image metadata or camera list not present

    # Image.metadata = None and cameras = []
    ( [ i_no_metadata, [] ], [] ),

    # Image.metadata = None 
    ( [ i_no_metadata, camera_list ], [] ),

    # cameras = []
    ( [ i_all_metadata, [] ], [] ),

    # Image.metadata.camera_make = None
    ( [ i_no_camera_make, camera_list ], [] ),

    # Image.metadata.camera_model = None 
    ( [ i_no_camera_model, camera_list ], [] ),

    # Image.metadata.date_taken = None 
    ( [ i_no_date_taken, camera_list ], [] ),

    ## Test cases for image metadata and camera list present

    # 1 matching camera
    ( [ i_canon100, camera_list ], [ c_canon100 ] ),
    ( [ i_nikon2, camera_list ], [ c_nikon2 ] ),

    # 2 matching cameras as taken date is unknown
    ( [ i_canon300, camera_list ], [ c_canon300_unknown_a, c_canon300_unknown_b ] ),

    # 2 matching cameras as cameras owned at same time
    ( [ i_nikon4_noughties, camera_list ], [ c_nikon4_noughties_a, c_nikon4_noughties_b ] ),

    # 1 matching camera as taken date is known
    ( [ i_canon500_teens, camera_list ], [ c_canon500_teens ] ),
    ( [ i_canon500_twenties, camera_list ], [ c_canon500_twenties ] ),

    # 1 matching Film camera
    ( [ i_filmscan6, camera_list ], [ c_filmscan6 ] ),

]

@pytest.mark.parametrize( "args, expected", test_get_matching_cameras_data )
def test_get_matching_cameras( args, expected ):
    assert args[0].get_matching_cameras( args[1] ) == expected
