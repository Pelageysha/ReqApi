import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEMA

BASE_URL = 'https://reqres.in/'
LIST_RESOURCE = 'api/unknown'
SINGLE_RESOURCE = LIST_RESOURCE + '/2'
RESOURCE_NOT_FOUND = LIST_RESOURCE + '/23'
MIN_ENTER_YEAR = 2000
COLOR_FIRST_SYMBOL = '#'


def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE)
    assert response.status_code == 200

    resource_data = response.json()['data']
    for item in resource_data:
        validate(item, RESOURCE_DATA_SCHEMA)
        assert item['year'] >= MIN_ENTER_YEAR
        assert item['color'].startswith(COLOR_FIRST_SYMBOL)


def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200

    resource_data = response.json()['data']
    validate(resource_data, RESOURCE_DATA_SCHEMA)
    assert resource_data['id'] == 2
    assert resource_data['year'] % 10 == 1


def test_resource_not_found():
    response = httpx.get(BASE_URL + RESOURCE_NOT_FOUND)
    assert response.status_code == 404
