import argparse
import os
import sys
import time

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    print("[ERROR] The 'requests' package is required. Install it with: python3 -m pip install requests")
    sys.exit(1)

# --- CONFIGURATION ---
TARGET_URL = "https://example.com/"  # Override with --target flag
VERSION = "v1.2.1"
TOOL_NAME = "NEXUS-SHIFT"
REFRESH_INTERVAL = 5
PROXY_SOURCE = (
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http"
    "&timeout=5000&country=all&ssl=all&anonymity=all"
)

# Colors for Terminal UI
class Color:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw_header(success_count, fail_count, target_url, refresh_interval):
    clear_screen()
    print(f"{Color.CYAN}{Color.BOLD}" + "=" * 50)
    print(f"       {TOOL_NAME} | Traffic Logic Engine {VERSION}")
    print(f"       Target: {target_url}")
    print("=" * 50 + f"{Color.END}")
    print(f" Status: {Color.GREEN}ACTIVE{Color.END} | Reload Interval: {refresh_interval}s")
    print(f" Successes: {Color.CYAN}{success_count}{Color.END} | Failures: {Color.YELLOW}{fail_count}{Color.END}")
    print("-" * 50)


def fetch_proxies(proxy_source):
    try:
        response = requests.get(proxy_source, timeout=10)
        if response.status_code == 200:
            return [line.strip() for line in response.text.splitlines() if line.strip()]
        print(f"{Color.RED}[!] Failed to fetch proxy list: HTTP {response.status_code}{Color.END}")
    except RequestException as exc:
        print(f"{Color.RED}[!] Error fetching proxy list: {exc}{Color.END}")
    return []


def parse_args():
    parser = argparse.ArgumentParser(
        description="Nexus-Shift: proxy-rotating traffic simulator for infrastructure testing."
    )
    parser.add_argument(
        "--target",
        default=TARGET_URL,
        help="Target URL to reload (default: %(default)s)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=REFRESH_INTERVAL,
        help="Seconds to wait after each successful reload.",
    )
    parser.add_argument(
        "--proxy-source",
        default=PROXY_SOURCE,
        help="Proxy list source URL.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=0,
        help="Stop after this many proxy attempts (0 = unlimited).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch the proxy list and validate configuration without sending requests to the target.",
    )
    return parser.parse_args()


def run_nexus(target_url, refresh_interval, proxy_source, max_attempts=0):
    success_count = 0
    fail_count = 0
    attempts = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NexusShift/1.2"
    }

    while True:
        draw_header(success_count, fail_count, target_url, refresh_interval)
        print(f"{Color.YELLOW}[*] Fetching fresh network nodes...{Color.END}")

        nodes = fetch_proxies(proxy_source)
        if not nodes:
            print(f"{Color.RED}[!] No nodes found. Sleeping...{Color.END}")
            time.sleep(10)
            continue

        for node in nodes:
            if max_attempts and attempts >= max_attempts:
                return

            if not node:
                continue

            attempts += 1
            proxies = {"http": f"http://{node}", "https": f"http://{node}"}

            try:
                start_time = time.time()
                response = requests.get(
                    target_url,
                    headers=headers,
                    proxies=proxies,
                    timeout=3,
                )
                elapsed = round(time.time() - start_time, 2)

                if response.status_code == 200:
                    success_count += 1
                    draw_header(success_count, fail_count, target_url, refresh_interval)
                    print(
                        f"{Color.GREEN}[+] SUCCESS{Color.END} | Node: {node} | Ping: {elapsed}s"
                    )
                    time.sleep(refresh_interval)
                else:
                    fail_count += 1
                    print(
                        f"{Color.RED}[-] FAILED{Color.END} | Node: {node} | Status: {response.status_code}"
                    )

            except RequestException as exc:
                fail_count += 1
                if fail_count % 10 == 0 or attempts <= 3:
                    draw_header(success_count, fail_count, target_url, refresh_interval)
                print(
                    f"{Color.RED}[!] PROXY ERROR{Color.END} | Node: {node} | {exc.__class__.__name__}: {exc}"
                )
                continue

    print(f"{Color.YELLOW}[!] Nexus-Shift complete.{Color.END}")


if __name__ == "__main__":
    args = parse_args()

    if args.dry_run:
        print(f"{Color.CYAN}[*] Dry run mode: fetching proxy list and validating configuration only.{Color.END}")
        proxies = fetch_proxies(args.proxy_source)
        print(f"{Color.GREEN}[+] Retrieved {len(proxies)} proxy nodes.{Color.END}")
        sys.exit(0)

    try:
        run_nexus(
            target_url=args.target,
            refresh_interval=args.interval,
            proxy_source=args.proxy_source,
            max_attempts=args.max_attempts,
        )
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Nexus-Shift shutting down safely.{Color.END}")
        sys.exit(0)
