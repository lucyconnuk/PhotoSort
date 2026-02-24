from classes.Camera import Camera
from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

@dataclass(frozen=True)
class Image:
    
    image_filename: Path
    sidecar_filename: Optional[Path] = None
    camera: Optional[Camera] = None
    taken_date: Optional[datetime] = None
    owner: Optional[Owner] = None
    initial_capture: Optional[ImageCaptureType] = None

    def __post_init__(self):

        if self.sidecar_filename and self.sidecar_filename.suffix != ".xmp":
            raise ValueError("Sidecar file must be an .xmp file")
        
        if self.camera and not self.initial_capture:
            # Set image initial capture method to camera image capture type
            self.initial_capture = self.camera.image_capture_type