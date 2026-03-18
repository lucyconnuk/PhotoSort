from datetime import datetime
from pathlib import Path

from classes.Camera import Camera
from classes.Image import Image
from classes.ImageCaptureType import ImageCaptureType
from classes.ImageFile import ImageFile
from classes.ImageMetadata import ImageMetadata
from classes.Owner import Owner
from classes.PathFormat import PathFormat


class TestData:

    ### Owners used in tests

    ## Empty object
    o_empty = Owner( None, None )

    ## Filled objects
    o_alice = Owner( "Alice", "Alice-photos" )
    o_bob = Owner( "Bob", "Bob-pics" )
    o_carol = Owner( "Carol", "CarolImages" )

    ## Full list
    owner_list = [
        o_empty,
        o_alice,
        o_bob,
        o_carol
    ]


    ### Cameras used in tests

    ## Empty object
    c_empty = Camera( None, None, None, None )

    ## Filled objects

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

    ## Full list
    camera_list = [ 
        c_empty,
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


    ### Path Formats used in tests

    ## Empty objects
    pf_none = None
    pf_empty = PathFormat( None, None, None )

    ## Filled objects
    pf_alice_digital = PathFormat( o_alice.name, ImageCaptureType.Digital, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )
    pf_alice_film = PathFormat( o_alice.name, ImageCaptureType.Film, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )
    pf_bob_digital = PathFormat( o_bob.name, ImageCaptureType.Digital, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )

    ## Full list
    pf_list = [
        pf_none,
        pf_empty,
        pf_alice_digital,
        pf_alice_film,
        pf_bob_digital
    ]


    ### Image Metadata used in tests

    ## Filled objects
    im_no_camera_make = ImageMetadata( None, "b", datetime( 2001, 1, 1 ) )
    im_no_camera_model = ImageMetadata( "a", None, datetime( 2001, 1, 1 ) )
    im_no_date_taken = ImageMetadata( "a", "b", None )
    im_all_metadata = ImageMetadata( "a", "b", datetime( 2001, 1, 1 ) )
    im_canon100 = ImageMetadata( "Canon", "100", None )
    im_nikon2 = ImageMetadata( "Nikon", "2", None )
    im_canon300 = ImageMetadata( "Canon", "300", None )
    im_nikon4_noughties = ImageMetadata( "Nikon", "4", datetime( 2001, 1, 1 ) )
    im_canon500_teens = ImageMetadata( "Canon", "500", datetime( 2011, 1, 1 ) )
    im_canon500_twenties = ImageMetadata( "Canon", "500", datetime( 2021, 1, 1 ) )
    im_filmscan6 = ImageMetadata( "FilmScan", "6", None )
    

    ### Image Files used in tests

    testpath: Path = Path( "testpath" )

    ## Filled objects
    if_no_camera_make = ImageFile( testpath, im_no_camera_make )
    if_no_camera_model = ImageFile( testpath, im_no_camera_model )
    if_no_date_taken = ImageFile( testpath, im_no_date_taken )
    if_all_metadata = ImageFile( testpath, im_all_metadata )
    if_canon100 = ImageFile( testpath, im_canon100 )
    if_nikon2 = ImageFile( testpath, im_nikon2 )
    if_canon300 = ImageFile( testpath, im_canon300 )
    if_nikon4_noughties = ImageFile( testpath, im_nikon4_noughties )
    if_canon500_teens = ImageFile( testpath, im_canon500_teens )
    if_canon500_twenties = ImageFile( testpath, im_canon500_twenties )
    if_filmscan6 = ImageFile( testpath, im_filmscan6 )


    ### Images used in tests

    ## Empty object
    i_no_metadata =     Image( None )

    ## Partially filled objects - image_file set, camera and expected_path not yet set
    i_no_camera_make =  Image( if_no_camera_make )
    i_no_camera_model = Image( if_no_camera_model )
    i_no_date_taken =   Image( if_no_date_taken )
    i_all_metadata =    Image( if_all_metadata )
    i_canon100 = Image( if_canon100 )
    i_nikon2 = Image( if_nikon2 )
    i_canon300 = Image( if_canon300 )
    i_nikon4_noughties = Image( if_nikon4_noughties )
    i_canon500_teens = Image( if_canon500_teens )
    i_canon500_twenties = Image( if_canon500_twenties )
    i_filmscan6 = Image( if_filmscan6 )

    ## Partially filled objects - image_file and camera set, expected_path not yet set
    # Note that these are the images above where the camera is uniquely identifiable 
    # from make, model and date taken.
    i2_canon100 = Image( if_canon100, c_canon100 )
    i2_nikon2 = Image( if_nikon2, c_nikon2 )
    i2_canon500_teens = Image( if_canon500_teens, c_canon500_teens )
    i2_canon500_twenties = Image( if_canon500_twenties, c_canon500_twenties )
    i2_filmscan6 = Image( if_filmscan6, c_filmscan6 )
