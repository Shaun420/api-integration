import pytest
from app.database import CountryStorage

@pytest.mark.asyncio
async def test_save_and_get_country(country_obj):
    # Use :memory: for a temporary RAM database
    async with CountryStorage(":memory:") as db:
        
        # 1. Save
        await db.save_countries([country_obj])
        
        # 2. Retrieve
        results = await db.get_countries("India")
        
        assert len(results) == 1
        assert results[0].code == "IN"
        assert results[0].name == "India"

@pytest.mark.asyncio
async def test_upsert_logic(country_obj):
    """Test that saving the same country twice updates it, doesn't duplicate."""
    async with CountryStorage(":memory:") as db:
        
        # Save first time
        await db.save_countries([country_obj])
        
        # Change population and save again
        country_obj.population = 999
        await db.save_countries([country_obj])
        
        # Check count is still 1, but data changed
        results = await db.get_countries("India")
        assert len(results) == 1
        assert results[0].population == 999