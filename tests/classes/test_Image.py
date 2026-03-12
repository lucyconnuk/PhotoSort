import pytest
from datetime import datetime
from pathlib import Path
from classes.Image import Image
from classes.Owner import Owner
from classes.ImageCaptureType import ImageCaptureType
from classes.PathFormat import PathFormat


@pytest.mark.parametrize(
    "initial_capture_type, owner, date_taken, template, expected",
    [
        # --- Valid case ---
        (
            ImageCaptureType("Digital"),
            Owner("OwnerName", "OwnerDir"),
            datetime(2006, 10, 1, 12, 57, 44),
            r"\{ict\}-\{directory\}-\{yyyy\}-\{mm\}-\{dd\}",
            Path("Digital-OwnerDir-2006-10-01"),
        ),

        # --- Missing initial_capture_type ---
        (
            None,
            Owner("OwnerName", "OwnerDir"),
            datetime(2006, 10, 1),
            r"\{ict\}-\{directory\}-\{yyyy\}-\{mm\}-\{dd\}",
            Path(""),
        ),

        # # --- Missing owner ---
        # (
        #     ImageCaptureType("Digital"),
        #     None,
        #     datetime(2006, 10, 1),
        #     r"\{ict\}-\{directory\}-\{yyyy\}-\{mm\}-\{dd\}",
        #     Path(""),
        # ),

        # --- Missing date_taken ---
        (
            ImageCaptureType("Digital"),
            Owner("OwnerName", "OwnerDir"),
            None,
            r"\{ict\}-\{directory\}-\{yyyy\}-\{mm\}-\{dd\}",
            Path(""),
        ),

        # --- Empty template ---
        (
            ImageCaptureType("Digital"),
            Owner("OwnerName", "OwnerDir"),
            datetime(2006, 10, 1),
            "",
            Path(""),
        ),
    ]
)
def test_get_expected_path(initial_capture_type, owner, date_taken, template, expected):
    img = Image()
    img.initial_capture_type = initial_capture_type
    img.owner = owner
    img.date_taken = date_taken

    path_format = PathFormat( owner.name, initial_capture_type, template)

    result = img.getExpectedPath(path_format)
    assert result == expected