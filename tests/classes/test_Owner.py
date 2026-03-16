
import pytest

from classes.Owner import Owner


def test_from_dict():
    result = Owner.from_dict( { "name": "Alice", "directory": "AlicePics" } )
    assert result.name == "Alice"
    assert result.directory == "AlicePics"

@pytest.mark.skip("Not written")
def test_dataframe_to_list():
    pass

@pytest.mark.skip("Not written")
def test_get_all():
    pass

@pytest.mark.skip("Not written")
def test_load_all():
    pass
