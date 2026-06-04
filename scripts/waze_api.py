import json
import os
import random
import time

import logger as lg
from playwright.sync_api import sync_playwright

MAP_URL = [
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.12672622%2C-8.5799253&from=place.EipBdi4gU2VycGEgUGludG8sIDQ0NTAgTWF0b3NpbmhvcywgUG9ydHVnYWwiLiosChQKEgkXLMT4L28kDRHRu3jMRXXoJxIUChIJi0gLpZ1oJA0R0DiQ5L3rAAQ&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.1157667%2C-8.64933014&from=ll.41.19338142%2C-8.54255676&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.11945241%2C-8.59130859&from=ll.41.21288374%2C-8.63044739&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.12139217%2C-8.63027573&from=ll.41.19983979%2C-8.67267609&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.215079%2C-8.589077&from=ll.41.10703657%2C-8.62358093&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.11402077%2C-8.56178284&from=ll.41.1834343%2C-8.6948204&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
    "https://www.waze.com/pt-BR/live-map/directions?to=ll.41.1994523%2C-8.6441803&from=ll.41.10703657%2C-8.62358093&utm_medium=lm_share_directions&utm_campaign=default&utm_source=waze_website",
]


INTERVAL = 60  # 1 minute
OUTPUT_DIR = "../Data/Waze"
USER_DATA_DIR = "./browser_profile"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def handle_response(response):
    """Listens to background network traffic and intercepts the GeoRSS API payload."""
    if "live-map/api/georss" in response.url or "TGeoRSS" in response.url:
        print(f"Caught native Waze API call: {response.url[:70]}...")
        try:
            if response.status == 200:
                json_data = response.json()
                timestamp = int(time.time())
                filename = os.path.join(OUTPUT_DIR, f"waze_{timestamp}.json")

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                print(f"Successfully saved active payload to: {filename}")
                lg.log(type="Waze", logtext=f"SUCCESS: {filename}")
                exit(0)
            else:
                print(
                    f"Intercepted API call but server returned status: {response.status}"
                )
                lg.log(
                    type="Waze",
                    logtext=f"ERROR: Error getting the reponse code: {response.status}",
                )
        except Exception as e:
            print(f"Failed to read response stream: {e}")
            lg.log(
                type="Waze",
                logtext=f"ERROR: Error getting the reponse code: {response.status}",
            )


def fetch_waze_data():
    with sync_playwright() as p:
        print(f"Launching a browser instance...")

        # A persistent context retains session state and avoids leaking raw driver traits
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # Headful mode is required initially to pass anti-bot device tests
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
        )
        page = context.new_page()

        # Register the background packet sniffer
        page.on("response", handle_response)

        print(f"Loading Waze Live Map interface...")
        try:
            page.goto(random.choice(MAP_URL), wait_until="networkidle", timeout=60000)
            time.sleep(3)

            page.mouse.move(860, 240)
            for i in range(2):
                page.mouse.wheel(0, 150)
                time.sleep(0.5)

        except Exception as e:
            print(f"Initial page-load warning (proceeding anyway): {e}")

        print(
            "\n Active Monitoring Loop engaged. Press Ctrl+C to terminate.\n" + "=" * 50
        )

        try:
            while True:
                time.sleep(INTERVAL)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f"[{current_time}] Refreshing map viewport to force a fresh data sync..."
                )

                # Reloading the visual page mimics
                page.reload(wait_until="networkidle", timeout=45000)

        except KeyboardInterrupt:
            print("\nMonitoring session closed gracefully by user command.")
        finally:
            context.close()


if __name__ == "__main__":
    fetch_waze_data()
