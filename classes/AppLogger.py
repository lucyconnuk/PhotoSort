import datetime
import logging
from dataclasses import dataclass
from datetime import datetime


@dataclass( frozen=False, slots=True )
class AppLogger:
    """
    Used to set up a singleton instance of logging.Logger.
    """

    @staticmethod
    def setup_logging_to_console():
        console = logging.StreamHandler()
        console.setLevel( logging.DEBUG )
        # set a format which is simpler for console use
        #formatter = logging.Formatter( '%(levelname)-8s: %(message)s' )
        # tell the handler to use this format
        #console.setFormatter( formatter )
        # add the handler to the root logger
        logging.basicConfig( 
            #filename = fr'logs\photosort-{start_time_text}.log', 
            level = logging.DEBUG,
            #format = '%(asctime)s %(levelname)s: %(message)s',
            #datefmt = '%y-%m-%d %H:%M:%S'
        )
        logger.addHandler( console )

    @staticmethod
    def setup_logging_to_file():
        # Define handler which writes INFO messages or higher to the console.
        # See https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
        start_time = datetime.now()
        start_time_text = start_time.strftime("%Y%m%dT%H%M%S")

        ### TODO - this is being shared, sort it out
        ### TODO - logs dir needs to exist!!!
        logging.basicConfig( 
            filename = fr'logs\photosort-{start_time_text}.log', 
            level = logging.DEBUG,
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%y-%m-%d %H:%M:%S'
        )

    
        
# Create singleton instance of logging.Logger
#logger = logging.getLogger(__name__)

# Configure root logger
# logging.basicConfig( 
#     level = logging.DEBUG,
#     datefmt = '%y-%m-%d %H:%M:%S'
# )


# Get start time
start_time = datetime.now()
start_time_text = start_time.strftime("%Y%m%dT%H%M%S")

# Set up handler to send INFO and above messages to console
console_formatter = logging.Formatter( '%(levelname)-8s: %(message)s' )
console_handler = logging.StreamHandler()
console_handler.setFormatter( console_formatter )
console_handler.setLevel( logging.INFO )

# Set up handler to write DEBUG and above (i.e. all) messages to file
file_formatter = logging.Formatter( '%(levelname)-8s: %(message)s' )
file_handler = logging.FileHandler( fr'logs\photosort-{start_time_text}.log' )
file_handler.setFormatter( file_formatter )
file_handler.setLevel( logging.DEBUG )

# Set up logger to send messages to console and file
logger = logging.getLogger(__name__)
AppLogger.setup_logging_to_file()
AppLogger.setup_logging_to_console()
