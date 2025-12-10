import aiohttp
#import rich
import logging
import time
from typing import List
from .models import Country
from .config import settings

log = logging.getLogger("rich")
class CountryAPI:
	BASE_URL = settings.API_BASE_URL

	def __init__(self, session: aiohttp.ClientSession):
		"""
		Initialize with an existing aiohttp session to reuse connections.
		"""
		self.session = session

	async def fetch(self, endpoint: str, value: str) -> List[Country]:
		"""
		Fetches data from the REST Countries API.
		
		Args:
			endpoint: "name" (for country name) or "capital" (for city name)
			value: The search term (e.g., "France", "Tokyo")
			
		Returns:
			List[Country]: A list of validated, flattened Country objects.
		"""
		url = f"{self.BASE_URL}/{endpoint}/{value}"
		
		try:
			async with self.session.get(url) as response:
				# Handle 404 (Not Found) gracefully - return empty list
				if response.status == 404:
					return []
				
				# Handle other API errors (500, 403, etc.)
				response.raise_for_status()
				
				data = await response.json()
				
				# The 'model_validator' in models.py will automatically 
				# extract and flatten the fields (name, currencies, etc).
				return [Country(**item, last_updated=int(time.time())) for item in data]

		except aiohttp.ClientError as e:
			log.exception(f"[API Error] Connection failed: {e}")
			return []
		except Exception as e:
			log.exception(f"[API Error] Unexpected error: {e}")
			return []