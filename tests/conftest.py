import pytest
from app.models import Country

@pytest.fixture
def raw_api_data():
    """Simulates the messy JSON returned by RestCountries API."""
    return {
        "cca2": "IN",
        "name": {"common": "India", "official": "Republic of India"},
        "capital": ["New Delhi"],
        "region": "Asia",
        "population": 1400000000,
        "currencies": {"INR": {"name": "Indian rupee"}},
        "languages": {"eng": "English", "hin": "Hindi"},
        "timezones": ["UTC+05:30"]
    }

@pytest.fixture
def country_obj(raw_api_data):
    """Returns a validated Country object."""
    return Country(**raw_api_data)