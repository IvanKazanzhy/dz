import pytest
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.openweathermap.org/data/2.5/weather")



@pytest.fixture
def api_key():
    if not API_KEY:
        pytest.skip("Set API_KEY in .env to run API tests")
    return API_KEY


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.mark.parametrize("city", ["London", "New York", "Tokyo"])
def test_valid_city(api_key, base_url, city):
    response = requests.get(base_url, params={"q": city, "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_missing_api_key(base_url):
    response = requests.get(base_url, params={"q": "London"}, timeout=10)
    assert response.status_code == 401


def test_missing_city(base_url, api_key):
    response = requests.get(base_url, params={"appid": api_key}, timeout=10)
    assert response.status_code == 400


def test_invalid_api_key(base_url):
    response = requests.get(base_url, params={"q": "London", "appid": "invalidkey"}, timeout=10)
    assert response.status_code == 401


def test_valid_city_and_country(api_key, base_url):
    response = requests.get(base_url, params={"q": "London,uk", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_valid_zip_code(api_key, base_url):
    response = requests.get(base_url, params={"zip": "10001,us", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_invalid_zip_code(api_key, base_url):
    response = requests.get(base_url, params={"zip": "00000,us", "appid": api_key}, timeout=10)
    assert response.status_code == 404


def test_valid_coordinates(api_key, base_url):
    response = requests.get(base_url, params={"lat": "35", "lon": "139", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_valid_city_and_state(api_key, base_url):
    response = requests.get(base_url, params={"q": "New York,NY,US", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_invalid_city_and_country(api_key, base_url):
    response = requests.get(base_url, params={"q": "NonExistingCity,NonExistingState", "appid": api_key}, timeout=10)
    assert response.status_code == 404


def test_valid_language(api_key, base_url):
    response = requests.get(base_url, params={"q": "Tokyo", "lang": "ja", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_valid_city_and_state_code(api_key, base_url):
    response = requests.get(base_url, params={"q": "Los Angeles,CA,US", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_invalid_city_and_country_code_other(api_key, base_url):
    response = requests.get(base_url, params={"q": "NonExistingCity,XY", "appid": api_key}, timeout=10)
    assert response.status_code == 404


def test_valid_city_and_country_code(api_key, base_url):
    response = requests.get(base_url, params={"q": "Berlin,DE", "appid": api_key}, timeout=10)
    assert response.status_code == 200
    assert "main" in response.json()
    assert "temp" in response.json()["main"]


def test_invalid_city_and_country_code(api_key, base_url):
    response = requests.get(base_url, params={"q": "NonExistingCity,XX", "appid": api_key}, timeout=10)
    assert response.status_code == 404