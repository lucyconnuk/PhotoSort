import argparse
from pathlib import Path

from classes.AppConfig import appConfig
from classes.AppLogger import logger
from classes.File import File
from classes.Image import Image
from classes.ImageFile import ImageFile

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


def main():

    # Get arguments from the default values, the command line, or the user.
    args = get_command_line_args()
    logger.info( f"Args are: {args}" )
    path_str = args.path if args.path else input( "Enter path to the root image directory: " ).strip()
    path = Path( path_str )

    # Check that the root image directory path points to a valid directory.
    (valid, message) = File.check_valid_path( path )
    if valid:
        logger.info( message )

        logger.debug( "Cameras are: ")
        for camera in appConfig.cameras: logger.debug( camera )
        logger.debug( "Owners are: ")
        for owner in appConfig.owners: logger.debug( owner )
        logger.debug( "Path Formats are: ")
        for path_format in appConfig.path_formats: logger.debug( path_format )

        # Find all the files in the directory.
        files_and_dirs = path.rglob("*")
        file_paths = File.get_files( files_and_dirs )
        
        # Find all the image files in the set.
        image_paths = File.get_image_files( file_paths )
        logger.info( f"Found {len(image_paths)} images." )
        logger.debug( "Images are: ")
        for image_path in image_paths: logger.debug( image_path.relative_to( path ) )

        # # Find all the XMP files in the set.
        # xmp_file_paths = File.get_xmp_files( file_paths )
        # logger.info( f"Found {len(xmp_file_paths)} xmp files." )
        # logger.debug( "XMP files are: ")
        # for xmp_file_path in xmp_file_paths: logger.debug( xmp_file_path.relative_to( path ) )

        # Create Images, with their metadata, from image Paths
        images = []
        for image_path in image_paths:
            image = Image( ImageFile( image_path ) )
            image.get_metadata()
            images.append( image )

        logger.info( f"Created {len(images)} Image objects." )
        logger.info ( images[0] )

    else:
        logger.warning( message )

if __name__ == "__main__":
    main()