
from argparse import Namespace

import photosort
from classes.AppConfig import appConfig
from classes.AppLogger import logger


def test_main(mocker):

    # Patch functions which will be called by the function under test
    mocker.patch( "photosort.get_command_line_args", return_value = Namespace(path='C:\\Users\\lcbc\\Documents\\_Technology\\_GitRepos\\PhotoSort\\tests\\data') )
    mocker.patch( "classes.AppConfig.AppConfig.__init__" )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    photosort.main()

    # Check that...
    # logger.warning.assert_has_calls( [
    #     mocker.call(),
    #     mocker.call()
    # ] )
    appConfig.__init__.assert_called_once()
    #logger.warning.assert_called_once_with( "Image C:\\Users\\lcbc\\Documents\\_Technology\\_GitRepos\\PhotoSort\\tests\\data\\IMG_2470.JPG should be at None" )

def test_main_path_doesnt_exist(mocker):

    # Patch functions which will be called by the function under test
    mocker.patch( "photosort.get_command_line_args", return_value = Namespace(path='Z') )
    mocker.patch( "classes.AppLogger.logger.warning" )

    # Call the function under test
    photosort.main()

    # Check that the following function was called
    logger.warning.assert_called_once_with( "Z does not exist" )
