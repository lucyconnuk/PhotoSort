from datetime import datetime

from classes.Camera import Camera
from classes.Image import Image
from classes.ImageCaptureType import ImageCaptureType
from classes.ImageFile import ImageFile
from classes.ImageMetadata import ImageMetadata
from classes.Owner import Owner
from classes.PathFormat import PathFormat


class TestData:

    ## Owners used in tests

    o_alice = Owner( "Alice", "Alice-photos" )
    o_bob = Owner( "Bob", "Bob-pics" )
    o_carol = Owner( "Carol", "CarolImages" )

    owner_list = [
        o_alice,
        o_bob,
        o_carol
    ]

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

    # Path Formats used in tests
    pf_none = None
    pf_empty = PathFormat( None, None, None )
    pf_alice_digital = PathFormat( o_alice.name, ImageCaptureType.Digital, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )
    pf_alice_film = PathFormat( o_alice.name, ImageCaptureType.Film, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )
    pf_bob_digital = PathFormat( o_bob.name, ImageCaptureType.Digital, r"{ict}\{directory}\{yyyy}\{yyyy-mm}\{yyyy-mm-dd}" )

    pf_list = [
        pf_none,
        pf_empty,
        pf_alice_digital,
        pf_alice_film,
        pf_bob_digital
    ]

    ic_canon100 = Image( ImageFile( metadata = ImageMetadata( "Canon", "100", None ) ), camera = c_canon100 )
