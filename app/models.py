from pydantic import BaseModel, model_validator
from typing import Any

class Country(BaseModel):
    code: str          # from cca2
    name: str          # from name.common
    official_name: str # from name.official
    capital: str       # from capital[0]
    region: str        # from region
    population: int    # from population
    currencies: str    # formatted string
    languages: str     # formatted string
    timezone: str      # from timezones[0]

    @model_validator(mode='before')
    @classmethod
    def flatten_api_response(cls, data: Any) -> Any:
        """
        Pre-process the raw API JSON dictionary to match our flat fields.
        """
        if isinstance(data, dict):
            # 1. Handle Names (nested dict)
            name_obj = data.get('name', {})
            data['name'] = name_obj.get('common', 'Unknown')
            data['official_name'] = name_obj.get('official', 'Unknown')

            # 2. Handle Code
            data['code'] = data.get('cca2', 'N/A')

            # 3. Handle Capital (list -> str)
            caps = data.get('capital', [])
            data['capital'] = caps[0] if caps else 'N/A'

            # 4. Handle Timezone (list -> str)
            # Usually returns list like ['UTC+05:30'], we take the first one.
            tzs = data.get('timezones', [])
            data['timezone'] = tzs[0] if tzs else 'UTC'

            # 5. Handle Currencies (dict -> str)
            # ex: {'INR': {'name': 'Indian rupee'}} -> "Indian rupee (INR)"
            curr_dict = data.get('currencies', {})
            curr_list = [f"{v.get('name')} ({k})" for k, v in curr_dict.items()]
            data['currencies'] = ", ".join(curr_list) if curr_list else "N/A"

            # 6. Handle Languages (dict -> str)
            # ex: {'eng': 'English', 'hin': 'Hindi'} -> "English, Hindi"
            lang_dict = data.get('languages', {})
            data['languages'] = ", ".join(lang_dict.values()) if lang_dict else "N/A"

        return data