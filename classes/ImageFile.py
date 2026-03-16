from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from classes.ImageMetadata import ImageMetadata


@dataclass( frozen=False, slots=True )
class ImageFile:
    
    path: Optional[Path] = None
    metadata: Optional[ImageMetadata] = None

    def get_metadata(self):

        # Get image metadata from image file
        self.metadata = ImageMetadata().from_path( self.path )
