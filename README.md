# api-integration

A robust, asynchronous command-line tool built with Python to fetch, filter, and cache country data from the public REST Countries API.


## Features

*   **Asynchronous I/O:** Built with `asyncio`, `aiohttp`, and `aiosqlite` for non-blocking performance.
*   **Smart Caching (Offline Mode):** Automatically saves fetched data to a local SQLite database (`countries.db`). If the API is unreachable, the tool seamlessly queries the local cache.
*   **Data Normalization:** Uses **Pydantic Model Validators** to flatten deeply nested API responses (e.g., transforming `name['nativeName']['hin']['common']` into a simple string) before the data enters the application logic.
*   **Rich UI:** specific fields (Official Name, Capital, Currency, Timezone) are displayed in a clean, color-coded table using `rich`.


## Setup and Installation

**Prerequisites:** Python 3.10+

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Shaun420/api-integration.git
    cd api-integration
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    # Search by Country Name
    python main.py name "India"

    # Search by Capital City
    python main.py city "Tokyo"
    ```


## Error Handling

The application implements a multi-layer error handling strategy:

1.  **Network Failures:** `aiohttp` exceptions are caught gracefully. If the internet is down, the app logs a warning and automatically attempts to retrieve data from the local database.
2.  **API 404 (Not Found):** Handled specifically to return an empty list rather than raising an exception, allowing the flow to proceed to the cache check.
3.  **Data Parsing:** The **Pydantic validator** is designed to handle missing keys (e.g., countries with no `capital`) by assigning default values (`"N/A"`) instead of crashing.
4.  **Context Safety:** Database and Network connections are managed via **Async Context Managers** (`async with`), ensuring connections close correctly even during crashes.


## API Endpoints Used

The application queries the [REST Countries v3.1 API](https://restcountries.com/):

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v3.1/name/{name}` | Search by country name (e.g., "India") |
| `GET` | `/v3.1/capital/{city}` | Search by capital city (e.g., "Paris") |


## Testing

Run the test suite to verify logic, including mock API responses:

```bash
pytest -v
```


## LICENSE
See [LICENSE](LICENSE)
