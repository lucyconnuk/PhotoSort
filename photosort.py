import argparse
from pathlib import Path

from classes.AppConfig import appConfig
from classes.AppLogger import logger
from classes.File import File
from classes.Image import Image
from classes.ImageFile import ImageFile


def get_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "List all image files in a directory and its subdirectories."
    )
    parser.add_argument(
        "-source",
        "-s",
        help = "Path to the source image directory",
    )
    parser.add_argument(
        "-dest",
        "-d",
        help = "Path to the destination image directory - if different from source",
    )
    return parser.parse_args()

def list_settings():
    logger.debug( "Cameras are: ")
    for camera in appConfig.cameras: logger.debug( camera )
    logger.debug( "Owners are: ")
    for owner in appConfig.owners: logger.debug( owner )
    logger.debug( "Path Formats are: ")
    for path_format in appConfig.path_formats: logger.debug( path_format )

def list_image_files( source_dir, image_paths ):
    logger.info( f"Found {len(image_paths)} images." )
    logger.debug( "Images are: ")
    for image_path in image_paths: logger.debug( image_path.relative_to( source_dir ) )

def main():

    # Get arguments from the default values, the command line, or the user.
    args = get_command_line_args()
    logger.info( f"Args are: {args}" )

    source_dir_str = args.source if args.source else input( "Enter path to the source image directory: " ).strip()
    source_dir = Path( source_dir_str )

    destination_dir_str = args.dest if args.dest else input( "(Optional) Enter path to the destination image directory: " ).strip()
    if destination_dir_str == "":
        destination_dir = source_dir
    else:
        destination_dir = Path( destination_dir_str )

    # Check that the source directory path points to a valid directory.
    (valid, message) = File.check_valid_path( "Source", source_dir )
    if not valid:
        logger.warning( message )
        exit
    logger.info( message )

    # Check that the destination directory path points to a valid directory.
    (valid, message) = File.check_valid_path( "Destination", destination_dir )
    if not valid:
        logger.warning( message )
        exit
    logger.info( message )

    list_settings()

    # Find all the files in the directory.
    files_and_dirs = source_dir.rglob("*")
    file_paths = File.get_files( files_and_dirs )
    
    # Find all the image files in the set.
    image_paths = File.get_image_files( file_paths )
    list_image_files( source_dir, file_paths )

    # Create Images, with their metadata, from image Paths
    images = []
    for image_path in image_paths:
        image = Image( ImageFile( image_path ) )
        image.load( destination_dir )
        images.append( image )

    logger.info( f"Created {len(images)} Image objects." )
    logger.info ( images[0] )

    # Determine which images are in the wrong place by comparing image_path with expected_path
    image: Image
    # TODO: Do filename better
    report_file = open( "move_files.bat", "a" )
    for image in images:
        if image.image_file.path != image.expected_path:
            logger.warning( f"Image {image.image_file.path} should be at {image.expected_path}" )
            print( f"move \"{image.image_file.path}\" \"{image.expected_path}\"", file = report_file )
    report_file.close()

if __name__ == "__main__":
    main()