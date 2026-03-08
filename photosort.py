import argparse
from classes.Camera import Camera
from classes.File import File
#from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from classes.PathFormat import PathFormat

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
        file_paths = File.get_files( files_and_dirs )
        
        # Find all the image files in the set.
        print( "Images are: ")
        image_paths = File.get_image_files( file_paths )
        for image_path in image_paths: print( image_path.name )

        # Find all the XMP files in the set.
        print( "XMP files are: ")
        xmp_file_paths = File.get_xmp_files( file_paths )
        for xmp_file_path in xmp_file_paths: print( xmp_file_path.name )

    cameras = Camera.get_all( r'./data/cameras.csv' )
    # for camera in cameras: print( camera )

    owners = Owner.get_all( r'./data/owners.csv' )
    # for owner in owners: print( owner )

    path_formats = PathFormat.get_all( r'./data/path_formats.csv' )
    # for path_format in path_formats: print( path_format )

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