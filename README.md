# Nexus-Shift | Traffic Logic Engine

Nexus-Shift is a Python-based proxy-rotating traffic simulator designed for infrastructure testing and load validation. It scrapes fresh public HTTP proxies and attempts reloads of a configured target URL while tracking success and failure counts.

## Features

- Dynamic proxy rotation using a live proxy feed
- Real-time CLI dashboard with success/failure counts
- Configurable target URL, refresh interval, and proxy source
- Optional dry-run mode to validate proxy list without sending traffic

## Requirements

- Python 3.8+
- `requests`

## Installation

```bash
python3 -m pip install requests
```

## Usage

```bash
python3 NexusShift.py
```

Optional flags:

- `--target URL` : Target URL to reload (default: `https://hushsmp.net/`)
- `--interval N` : Seconds to wait after each successful reload
- `--proxy-source URL` : Proxy list source URL
- `--max-attempts N` : Stop after N proxy attempts (0 = unlimited)
- `--dry-run` : Fetch and validate the proxy list without sending requests

Example:

```bash
python3 NexusShift.py --target https://example.com --interval 5 --max-attempts 20
```

## Notes

This tool is intended for authorized testing only. Use it only on systems and domains where you have explicit permission.

## License

MIT License
