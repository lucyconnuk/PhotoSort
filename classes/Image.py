from classes.Camera import Camera
from classes.ImageCaptureType import ImageCaptureType
from classes.Owner import Owner
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

@dataclass(frozen=True)
class Image:
    
    image_path: Path
    camera_model: Optional[Camera] = None
    date_taken: Optional[datetime] = None
    owner: Optional[Owner] = None
    initial_capture_type: Optional[ImageCaptureType] = None
    image_expected_path: Optional[Path] = None
    #sidecar_filename: Optional[Path] = None

    def __post_init__(self):

        # Set owner from camera_model and date_taken

        # Set initial_capture_type from camera_model
        if self.camera_model and not self.initial_capture_type:
            self.initial_capture_type = self.camera_model.image_capture_type

        # Set image_expected_path from date_taken, owner and initial_capture_type

        #if self.sidecar_filename and self.sidecar_filename.suffix != ".xmp":
        #    raise ValueError("Sidecar file must be an .xmp file")
        
