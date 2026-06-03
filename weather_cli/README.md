# Python Weather CLI

A command-line weather tool that fetches real-time weather data for any city using the
Open-Meteo API and exports the results to a JSON file. No API key required.

---

## How It Works

Sends an HTTP GET request to the Open-Meteo API, extracts the current weather data,
maps the numeric weather code to a human-readable condition, and saves the result to
`result_weather.json`.

```
python weather_cli.py --city Cochabamba --lat -17.39 --lon -66.16
        │                      │                │              │
        │                      │                └──────────────┘
        │                      │                coordinates
        │                      └── passed into the output (display + JSON)
        └── entry point
```

---

## Project Structure

```
weather_cli/
├── weather_cli.py
└── result_weather.json    # auto-generated after each run
```

---

## Tech Stack

- Python 3
- `requests` — HTTP calls to the Open-Meteo API
- `argparse` — CLI argument handling
- `json` — structured output

---

## Function Breakdown

### `WEATHER_CODES` — Lookup Dictionary
Maps the numeric weather codes returned by the API to human-readable conditions.
Uses `dict.get()` with a fallback to handle unknown codes gracefully:

```python
condition = WEATHER_CODES.get(code, f"Unknown code {code}")
```

### `get_weather(lat, lon)` — Core Logic
Receives latitude and longitude, builds the API URL dynamically, and sends a GET request
to the Open-Meteo API. Validates the response status code and returns only the
`current_weather` block from the JSON response:

```python
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
return response.json()["current_weather"]
```

Example API response:
```json
{
  "time": "2026-06-03T15:45",
  "temperature": 18.1,
  "windspeed": 3.8,
  "weathercode": 0
}
```

### `save_json(result, filename)` — Output Serializer
Writes the structured weather data to `result_weather.json` with 2-space indentation.

### `main()` — Entry Point
Parses `--city`, `--lat`, and `--lon` arguments via `argparse`, calls `get_weather(lat, lon)`,
maps the weather code to a condition, builds the output dictionary, prints it to the terminal,
and saves it to JSON.

---

## Usage

```bash
python weather_cli.py --city Cochabamba --lat -17.39 --lon -66.16
python weather_cli.py --city "New York" --lat 40.71 --lon -74.01
```

### CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--city` | ✅ | City name to label the output |
| `--lat` | ✅ | Latitude coordinate |
| `--lon` | ✅ | Longitude coordinate |

### Example Output

```
City       : Cochabamba
Temperature: 18.1°C
Condition  : Clear
Time       : 2026-06-03T15:45
```

```json
{
  "city": "Cochabamba",
  "temperature": "18.1°C",
  "condition": "Clear",
  "time": "2026-06-03T15:45"
}
```

---

## Prerequisites

```bash
pip install requests
```

---

## Concepts Practiced

- HTTP requests and response handling with `requests`
- API response parsing and key extraction from JSON
- Dictionary lookup with `.get()` and fallback values
- CLI argument parsing with `argparse`
- Structured data serialization with `json`
