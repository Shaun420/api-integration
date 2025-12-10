from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DEBUG: bool = False
	DB_NAME: str = "countries.db"
	API_BASE_URL: str = "https://restcountries.com/v3.1"
	CACHE_TTL_DAYS: int = 7

	model_config = SettingsConfigDict(env_file=".env")

settings = Settings()