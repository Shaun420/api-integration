import asyncio
import argparse
import aiohttp
import logging
from time import time
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

from app.models import Country
from app.database import CountryStorage
from app.api_client import CountryAPI
from app.config import settings

logging.basicConfig(handlers=[RichHandler()])

console = Console()

def display_table(countries: list[Country]):
	if not countries:
		console.print("[yellow]No countries found.[/yellow]")
		return

	# Expanded table with specific fields
	table = Table(title=f"Country Data ({len(countries)} found)", show_lines=True)

	table.add_column("Code", style="dim")
	table.add_column("Name / Official", style="cyan", no_wrap=False)
	table.add_column("Capital", style="magenta")
	table.add_column("Region", style="green")
	table.add_column("Population", justify="right")
	table.add_column("Details (Lang / Curr / TZ)")

	for c in countries:
		# Combine Name and Official Name in one cell for cleaner UI
		name_display = f"[bold]{c.name}[/bold]\n[italic dim]{c.official_name}[/italic dim]"
		
		# Combine extra details in one cell
		details = (
			f"[b]Lang:[/b] {c.languages}\n"
			f"[b]Curr:[/b] {c.currencies}\n"
			f"[b]Time:[/b] {c.timezone}"
		)

		table.add_row(
			c.code,
			name_display,
			c.capital,
			c.region,
			f"{c.population:,}",
			details
		)

	console.print(table)

async def handle_request(args, session, storage):
	api = CountryAPI(session)
	endpoint = "capital" if args.command == "city" else "name"
	
	console.print(f"[bold blue]Searching for {args.command}: '{args.query}'...[/bold blue]")
	
	all_cached = await storage.get_countries(args.query)

	current_time = int(time())
	cache_ttl = settings.CACHE_TTL_DAYS * 86400

	cached = [
		country
		for country in all_cached
		if (current_time - country.last_updated) < cache_ttl
	]

	if cached:
		console.print(f"[green]:ballot_box_with_check: Fetched {len(cached)} result(s) from cache.[/green]")
		display_table(cached)
	else:
		console.print(f"[dim]:hourglass: Not found in cache. Fetching from API endpoint.[/dim]")
		try:
			countries = await api.fetch(endpoint, args.query)
			if countries:
				await storage.save_countries(countries)
				display_table(countries)
				console.print(f"[green]:ballot_box_with_check: Fetched and cached {len(countries)} result(s).[/green]")
			else:
				console.print("[red]:x: API returned no results.[/red]")
		except aiohttp.ClientError:
			console.print("[bold red]:warning: API Connection Failed.[/bold red]")

			# Fallback to cached data if exists
			if all_cached:
				console.print(f"[bold orange3]:warning: FALLBACK: Displaying cached data (Stale).[/bold orange3]")
				display_table(all_cached)
			else:
				console.print(f"[bold red]:x: System Failure: API down and no local cache available.[/bold red]")

async def main():
	parser = argparse.ArgumentParser(description="Advanced Country Fetcher")
	subparsers = parser.add_subparsers(dest="command", required=True)

	subparsers.add_parser("name").add_argument("query")
	subparsers.add_parser("city").add_argument("query")

	args = parser.parse_args()

	async with CountryStorage() as storage:
		async with aiohttp.ClientSession() as session:
			await handle_request(args, session, storage)

if __name__ == "__main__":
	asyncio.run(main())