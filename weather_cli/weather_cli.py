import argparse
import requests
import json

WEATHER_CODES = {
    0: "Clear",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Foggy",
    61: "Rainy",
    80: "Showers"
}

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return None

    return response.json()["current_weather"]

def save_json(result, filename="result_weather.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Weather CLI")
    parser.add_argument("--city", required=True, help="City name (label only)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    args = parser.parse_args()

    data = get_weather(args.lat, args.lon)

    if data is None:
        return

    code = data["weathercode"]
    condition = WEATHER_CODES.get(code, f"Unknown code {code}")

    weather_data = {
        "city": args.city,
        "temperature": f"{data['temperature']}°C",
        "condition": condition,
        "time": data["time"]
    }

    print(f"City       : {weather_data['city']}")
    print(f"Temperature: {weather_data['temperature']}")
    print(f"Condition  : {weather_data['condition']}")
    print(f"Time       : {weather_data['time']}")

    save_json(weather_data)
    print("\nInformation stored in 'result_weather.json'")

if __name__ == '__main__':
    main()
