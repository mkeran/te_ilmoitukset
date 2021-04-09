import pytest

from te_palvelut import xml_file_to_list


def test_xml_file_to_list_success():
    a = xml_file_to_list("tests/tyopaikat.xml")
    assert len(a[0]) == 183
    for x in a[0]:
        assert isinstance(x, dict)


def test_xml_file_to_list_file_not_found():
    with pytest.raises(FileNotFoundError):
        a = xml_file_to_list("tests/not_found.xml")

