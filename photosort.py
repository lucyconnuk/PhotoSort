import argparse
from classes.Camera import Camera
from classes.File import File
from classes.Image import Image
#from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from classes.PathFormat import PathFormat
import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# TODO:
# - develop main

def get_command_line_args():
    parser = argparse.ArgumentParser(
        description = "List all image files in a directory and its subdirectories."
    )
    parser.add_argument(
        "-path",
        "-p",
        help = "Path to the root image directory",

        # TODO Remove this test default setting
        default = r'C:\Users\Public\Pictures\PhotoOrganizer\Digital\Mary\2006\2006-03\2006-03-06'
    )
    return parser.parse_args()

def setup_logging_to_console():
    console = logging.StreamHandler()
    console.setLevel( logging.INFO )
    # set a format which is simpler for console use
    formatter = logging.Formatter( '%(levelname)-8s: %(message)s' )
    # tell the handler to use this format
    console.setFormatter( formatter )
    # add the handler to the root logger
    logger.addHandler( console )

def setup_logging_to_file():
    # Define handler which writes INFO messages or higher to the console.
    # See https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
    start_time = datetime.datetime.now()
    start_time_text = start_time.strftime("%Y%m%dT%H%M%S")
    logging.basicConfig( 
        filename = fr'logs\photosort-{start_time_text}.log', 
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )

def main():

    # Setup logging
    setup_logging_to_file()
    setup_logging_to_console()

    # Get arguments from the default values, the command line, or the user.
    args = get_command_line_args()
    logger.debug( f"Args are: {args}" )
    path_str = args.path if args.path else input( "Enter path to the root image directory: " ).strip()
    path = Path( path_str )

    # Check that the root image directory path points to a valid directory.
    (valid, message) = File.check_valid_path( path )
    if valid:
        logger.info( message )

        # Find all the files in the directory.
        files_and_dirs = path.rglob("*")
        file_paths = File.get_files( files_and_dirs )
        
        # Find all the image files in the set.
        image_paths = File.get_image_files( file_paths )
        logger.info( f"Found {len(image_paths)} images." )
        logger.debug( "Images are: ")
        for image_path in image_paths: logger.debug( image_path.relative_to( path ) )

        # Find all the XMP files in the set.
        xmp_file_paths = File.get_xmp_files( file_paths )
        logger.info( f"Found {len(xmp_file_paths)} xmp files." )
        logger.debug( "XMP files are: ")
        for xmp_file_path in xmp_file_paths: logger.debug( xmp_file_path.relative_to( path ) )

        # Create Images from image Paths
        images = [ Image( image_path ) for image_path in image_paths ]
        logger.info( f"Created {len(images)} Image objects." )
    else:
        logger.warning( message )

    cameras = Camera.get_all( r'./data/cameras.csv' )
    logger.debug( "Cameras are: ")
    for camera in cameras: logger.debug( camera )

    owners = Owner.get_all( r'./data/owners.csv' )
    logger.debug( "Owners are: ")
    for owner in owners: logger.debug( owner )

    path_formats = PathFormat.get_all( r'./data/path_formats.csv' )
    logger.debug( "Path Formats are: ")
    for path_format in path_formats: logger.debug( path_format )

    # matching_pfs = [ pf
    #     for pf in path_formats 
    #     if pf.owner_name == "Mary"
    #     and pf.image_capture_type == ImageCaptureType.Film.value
    # ]
    # print("***************************************")
    # for matching_pf in matching_pfs: print( matching_pf )


    # image = new Image(...);
    # camera = image.get_camera( cameras )
    # owner = camera.Owner
    # image.Owner = camera.Owner
    # image.Initialcapture = camera.InitialCapture
    # image.actual_path # where file is now
    # image.expected_path # where file should be - depends on image_capture_type, owner and date_taken


if __name__ == "__main__":
    main()