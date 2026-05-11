# Nexus-Shift | Traffic Logic Engine

Nexus-Shift is a Python-based proxy-rotating traffic simulator designed for infrastructure testing and load validation. It scrapes fresh public HTTP proxies and attempts reloads of a configured target URL while tracking success and failure counts.

## Features

- Dynamic proxy rotation using a live proxy feed
- Real-time CLI dashboard with success/failure counts
- Configurable target URL, refresh interval, and proxy source
- Optional dry-run mode to validate proxy list without sending traffic

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    NEXUS-SHIFT WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

1. PROXY FETCHING
   ├─ Fetch fresh proxies from ProxyScrape API
   ├─ Parse proxy list
   └─ Validate format

2. TRAFFIC GENERATION
   ├─ Select proxy from list
   ├─ Send HTTP request to target URL
   ├─ Track success/failure
   └─ Apply refresh interval

3. REAL-TIME DASHBOARD
   ├─ Display success count (✓)
   ├─ Display failure count (✗)
   ├─ Show current target
   └─ Show reload interval

4. LOOP & ROTATE
   └─ Return to step 2 until max attempts reached
```

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

## Screenshots

### Project Overview & Features

![Screenshot 1](Screenshot%202026-05-10%20212702.png)

### CLI Dashboard in Action

![Screenshot 2](Screenshot%202026-05-10%20212719.png)

### Real-time Traffic Monitoring

![Screenshot 3](Screenshot%202026-05-10%20212737.png)

### Active Proxy Rotation

![Screenshot 4](Screenshot%202026-05-10%20212744.png)

## License

MIT License
