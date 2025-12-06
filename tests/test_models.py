from app.models import Country

def test_model_flattens_api_response(raw_api_data):
    """Test if nested API JSON is flattened correctly."""
    country = Country(**raw_api_data)

    assert country.name == "India"
    assert country.official_name == "Republic of India"
    assert country.capital == "New Delhi"
    assert country.currencies == "Indian rupee (INR)"
    assert "Hindi" in country.languages
    assert country.timezone == "UTC+05:30"

def test_model_handles_flat_db_data():
    """Test that the model accepts already flattened data (DB Scenario)."""
    # This simulates data coming from SQLite (already strings)
    db_row = {
        "code": "IN",
        "name": "India",
        "official_name": "Republic of India",
        "capital": "New Delhi",
        "region": "Asia",
        "population": 1400000000,
        "currencies": "Indian rupee (INR)",
        "languages": "English, Hindi",
        "timezone": "UTC+05:30"
    }
    
    country = Country(**db_row)
    assert country.name == "India"
    assert country.currencies == "Indian rupee (INR)" 

def test_model_defaults_missing_data():
    """Test if defaults ('N/A') work when fields are missing."""
    empty_data = {
        "cca2": "XX",
        "name": {"common": "Unknown"},
        # Missing capital, currencies, etc.
        "region": "Nowhere",
        "population": 0
    }
    
    country = Country(**empty_data)
    assert country.capital == "N/A"
    assert country.currencies == "N/A"
    assert country.timezone == "UTC"