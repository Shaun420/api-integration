from pydantic import BaseModel, Field, model_validator
from typing import Any, Dict

class Country(BaseModel):
    code: str
    name: str
    official_name: str
    capital: str
    region: str
    population: int
    currencies: str
    languages: str
    timezone: str

    @model_validator(mode='before')
    @classmethod
    def flatten_api_response(cls, data: Any) -> Any:
        """
        Pre-process data.
        If data comes from API (nested), flatten it.
        If data comes from DB (flat), leave it alone.
        """
        if isinstance(data, dict):
            # Check if 'name' is a dictionary. 
            # If yes, it's Raw API Data -> We need to flatten it.
            # If no (it's a string), it's DB Data -> Skip logic.
            if isinstance(data.get('name'), dict):
                
                # 1. Handle Names
                name_obj = data.get('name', {})
                data['name'] = name_obj.get('common', 'Unknown')
                data['official_name'] = name_obj.get('official', 'Unknown')

                # 2. Handle Code
                data['code'] = data.get('cca2', 'N/A')

                # 3. Handle Capital (List -> String)
                caps = data.get('capital', [])
                if isinstance(caps, list):
                    data['capital'] = caps[0] if caps else 'N/A'

                # 4. Handle Timezone (List -> String)
                tzs = data.get('timezones', [])
                if isinstance(tzs, list):
                    data['timezone'] = tzs[0] if tzs else 'UTC'

                # 5. Handle Currencies (Dict -> String)
                curr_dict = data.get('currencies', {})
                if isinstance(curr_dict, dict):
                    curr_list = [f"{v.get('name')} ({k})" for k, v in curr_dict.items()]
                    data['currencies'] = ", ".join(curr_list) if curr_list else "N/A"

                # 6. Handle Languages (Dict -> String)
                lang_dict = data.get('languages', {})
                if isinstance(lang_dict, dict):
                    data['languages'] = ", ".join(lang_dict.values()) if lang_dict else "N/A"

        return data