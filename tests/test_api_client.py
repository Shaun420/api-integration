import pytest
import aiohttp
from aioresponses import aioresponses
from app.api_client import CountryAPI

@pytest.mark.asyncio
async def test_fetch_success(raw_api_data):
    """Test a successful 200 OK response."""
    endpoint = "name"
    query = "india"
    url = f"https://restcountries.com/v3.1/{endpoint}/{query}"

    with aioresponses() as m:
        # Mock the URL to return our list of data
        m.get(url, payload=[raw_api_data], status=200)

        async with aiohttp.ClientSession() as session:
            api = CountryAPI(session)
            results = await api.fetch(endpoint, query)
            
            assert len(results) == 1
            assert results[0].name == "India"

@pytest.mark.asyncio
async def test_fetch_404_not_found():
    """Test that 404 returns an empty list, not an error."""
    url = "https://restcountries.com/v3.1/name/atlantis"

    with aioresponses() as m:
        m.get(url, status=404)

        async with aiohttp.ClientSession() as session:
            api = CountryAPI(session)
            results = await api.fetch("name", "atlantis")
            
            assert results == []