import requests
import os
from datetime import datetime

# Configuration
LOCATION_ID = 5005  # Portland PDX
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Your requested Date Filter: Feb 1 to March 31, 2026
START_FILTER = datetime.strptime("2026-02-01", "%Y-%m-%d")
END_FILTER = datetime.strptime("2026-03-31", "%Y-%m-%d")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_slots():
    # We check the top 10 soonest slots to ensure we don't miss any in our window
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=10&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        if not response:
            print("No slots found at all for PDX.")
            return

        for slot in response:
            slot_date_str = slot['startTimestamp'][:10] # Extracts YYYY-MM-DD
            slot_date = datetime.strptime(slot_date_str, "%Y-%m-%d")
            
            # Check if it falls in your Feb/March window
            if START_FILTER <= slot_date <= END_FILTER:
                msg = f"🚨 PORTLAND SLOT FOUND!\nDate: {slot['startTimestamp']}\nBook it now: https://ttp.cbp.dhs.gov/"
                send_telegram(msg)
                print(f"Match found: {slot_date_str}")
                return # Alert once per run to avoid spam
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slots()
