import datetime
import logging
from dataclasses import dataclass
from datetime import datetime


@dataclass( frozen=False, slots=True )
class AppLogger:

    @staticmethod
    def setup_logging_to_console():
        console = logging.StreamHandler()
        console.setLevel( logging.DEBUG )
        # set a format which is simpler for console use
        formatter = logging.Formatter( '%(levelname)-8s: %(message)s' )
        # tell the handler to use this format
        console.setFormatter( formatter )
        # add the handler to the root logger
        logger.addHandler( console )

    @staticmethod
    def setup_logging_to_file():
        # Define handler which writes INFO messages or higher to the console.
        # See https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
        start_time = datetime.now()
        start_time_text = start_time.strftime("%Y%m%dT%H%M%S")
        logging.basicConfig( 
            filename = fr'logs\photosort-{start_time_text}.log', 
            level = logging.INFO,
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%y-%m-%d %H:%M:%S'
        )
        
# Create singleton instance of logging.Logger
logger = logging.getLogger(__name__)
AppLogger.setup_logging_to_file()
AppLogger.setup_logging_to_console()
