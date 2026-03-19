

from classes.ImageFile import ImageFile
from classes.ImageMetadata import ImageMetadata
from tests.data.TestData import TestData


def test_load_metadata(mocker):

    # Create test ImageFile
    test_if = ImageFile( TestData.testpath )

    # Patch ImageMetadata.from_path() to return the test metadata
    mocker.patch( "classes.ImageMetadata.ImageMetadata.from_path", return_value = TestData.im_all_metadata )

    # Call the function under test
    test_if.load_metadata()

    # Check that ImageMetadata.from_path() was called once with the test ImageFile path
    ImageMetadata.from_path.assert_called_once_with( test_if.path )

    # Check that the result was loaded into the ImageFile metadata
    assert test_if.metadata == TestData.im_all_metadata
