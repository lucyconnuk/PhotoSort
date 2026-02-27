import argparse
from classes.Camera import Camera
from classes.File import File
from classes.Image import Image
from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from pathlib import Path

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
    path_str = args.path if args.path else input( "Enter path to the root image directory: " ).strip()
    path = Path( path_str )

    # Check that the root image directory path points to a valid directory.
    (valid, message) = File.check_valid_path( path )
    print( message )
    if valid:

        # Find all the files in the directory.
        files_and_dirs = path.rglob("*")
        files = File.get_files( files_and_dirs )
        
        # Find all the image files in the set.
        print( "Images are: ")
        images = File.get_image_files( files )
        for image in images:
            print( image.name )

        # Find all the XMP files in the set.
        print( "XMP files are: ")
        xmp_files = File.get_xmp_files( files )
        for xmp_file in xmp_files:
            print( xmp_file.name )

    else:
        my_image = Image( "test.jpg", initial_capture=ImageCaptureType.Film )
        print( my_image )

    camera_data_file = Path( r'./data/cameras.csv' )
    cameras_df = Camera.load_all( camera_data_file )
    cameras = Camera.dataframe_to_list( cameras_df )
    for camera in cameras:
        print( camera )

    owner_data_file = Path( r'./data/owners.csv' )
    owners_df = Owner.load_all( owner_data_file )
    owners = Owner.dataframe_to_list( owners_df )
    for owner in owners:
        print( owner )

if __name__ == "__main__":
    main()