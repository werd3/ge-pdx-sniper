import requests
import os
from datetime import datetime

# CONFIG - pulled from GitHub Secrets / environment variables
LOCATION_ID = 5005
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Target dates
TARGETS = [
    "2026-05-12",
    "2026-05-13",
    "2026-05-14",
    "2026-05-15",
    "2026-05-16",
    "2026-05-17",
]

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("ERROR: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(f"Telegram send error: {e}")

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=30&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url, timeout=10).json()
        print(f"--- SCAN at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        found = False
        for slot in response:
            date_only = slot['startTimestamp'][:10]
            if date_only not in TARGETS:
                print(f"  Skipping {date_only}")
                continue
            msg = f"✅ MATCH FOUND!\nDate: {date_only}\nBook now: https://ttp.cbp.dhs.gov/"
            print(msg)
            send_telegram(msg)
            found = True
        if not found:
            print("  No matching slots found.")
    except Exception as e:
        print(f"Error fetching slots: {e}")

if __name__ == "__main__":
    check_slots()
