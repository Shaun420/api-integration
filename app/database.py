import aiosqlite
from typing import List
from .models import Country

class CountryStorage:
    def __init__(self, db_name: str = "countries.db"):
        self.db_name = db_name
        self.db = None

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_name)
        self.db.row_factory = aiosqlite.Row
        await self._init_db()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            await self.db.close()

    async def _init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS countries (
            code TEXT PRIMARY KEY,
            name TEXT,
            official_name TEXT,
            capital TEXT,
            region TEXT,
            population INTEGER,
            currencies TEXT,
            languages TEXT,
            timezone TEXT
        );
        """
        await self.db.execute(query)
        await self.db.commit()

    async def save_countries(self, countries: List[Country]):
        query = """
        INSERT OR REPLACE INTO countries 
        (code, name, official_name, capital, region, population, currencies, languages, timezone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = [
            (
                c.code, c.name, c.official_name, c.capital, c.region, 
                c.population, c.currencies, c.languages, c.timezone
            )
            for c in countries
        ]
        await self.db.executemany(query, data)
        await self.db.commit()

    async def get_countries(self, search_term: str) -> List[Country]:
        term = f"%{search_term}%"
        # Search by common name, official name, or capital
        query = """
            SELECT * FROM countries 
            WHERE name LIKE ? OR official_name LIKE ? OR capital LIKE ?
        """
        
        async with self.db.execute(query, (term, term, term)) as cursor:
            rows = await cursor.fetchall()

        # Convert DB Rows back to Pydantic Models
        return [Country(**dict(row)) for row in rows]