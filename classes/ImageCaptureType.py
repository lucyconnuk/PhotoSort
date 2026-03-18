from enum import Enum


class ImageCaptureType(Enum):
    """
    The initial capture type of an image - on Film (and later scanned in), or direct to Digital.
    """
    Film = "Film"
    Digital = "Digital"

    @staticmethod
    def validate_from_dict_field( data: dict, field_name: str ):
        if data.get( field_name ) is not None:
            try:
                data[field_name] = ImageCaptureType( data[field_name] )
            except:
                pass
