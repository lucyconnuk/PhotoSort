from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from classes.ImageMetadata import ImageMetadata


# For additional coding notes, see Camera.py
@dataclass( frozen=False, slots=True )
class ImageFile:
    """
    An image file object. Has a Path, and Metadata.
    """    
    
    path: Optional[Path] = None
    metadata: Optional[ImageMetadata] = None

    # instance method
    def set_metadata(self):

        # Get image metadata from image file
        self.metadata = ImageMetadata.from_path( self.path )
