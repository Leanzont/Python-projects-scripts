# Python Port Scanner

A lightweight command-line port scanner written in Python. Probes a target host for open TCP ports
and exports the results to a structured JSON file. Built from scratch using only the Python standard
library — no external dependencies required.

---

## How It Works

The scanner attempts a TCP connection to each port in the specified range. If the connection
succeeds, the port is recorded as open. All open ports are serialized to `result.json`.

````
python port_scanner.py --host scanme.nmap.org --start 1 --end 1024
        │                      │                    │          │
        │                      │                    └──────────┘
        │                      │                    port range
        │                      └── target host
        └── entry point
````

---

## Project Structure

````
port-scanner/
├── port_scanner.py
└── result.json        # auto-generated after each scan
````

---

## Tech Stack

- Python 3
- `socket` — TCP connection probing
- `argparse` — CLI argument handling
- `json` — structured output

---

## Function Breakdown

### `check_port(host, port)` — Core Logic
Opens a TCP socket to the target host and port with a 1-second timeout.
Uses `connect_ex()` which returns `0` on success (port open) or a non-zero error code (port closed/filtered).

```python
result = s.connect_ex((host, port))
return result == 0
```

### `scan(host, start_port, end_port)` — Port Range Iterator
Iterates over the specified port range, calls `check_port()` for each port,
and collects only the open ones into a list of dictionaries.

```python
{ "port": 80, "status": "Open" }
```

### `save_json(results, filename)` — Output Serializer
Writes the results list to a JSON file using `json.dump()` with 2-space indentation
for human-readable output.

### `main()` — Entry Point
Parses CLI arguments via `argparse`, orchestrates the scan, and triggers the file save.
The `if __name__ == '__main__':` guard ensures the script only runs when executed directly —
its functions remain importable without triggering a scan.

---

## Usage

```bash
# Scan default range (ports 1–1024)
python port_scanner.py --host scanme.nmap.org

# Scan a custom port range
python port_scanner.py --host scanme.nmap.org --start 70 --end 90
```

### CLI Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--host` | ✅ | — | Target hostname or IP address |
| `--start` | ❌ | `1` | First port in the scan range |
| `--end` | ❌ | `1024` | Last port in the scan range |

---

## Example Output

```json
[
  { "port": 80, "status": "Open" },
  { "port": 443, "status": "Open" }
]
```

---

## Prerequisites

- Python 3.x
- No external packages required

---
## Concepts Practiced

- TCP connection probing with `socket`
- CLI argument parsing with `argparse`
- Structured data serialization with `json`
- Modular function design and the `__main__` guard
