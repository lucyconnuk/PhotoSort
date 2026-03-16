from enum import Enum


class ImageCaptureType(Enum):
    """
    The initial capture type of an image - on Film (and later scanned in), or direct to Digital.
    """
    Film = "Film"
    Digital = "Digital"