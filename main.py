import requests
from datetime import datetime

# --- CONFIGURATION ---
LOCATION_ID = 5005  # Portland (PDX)
TOKEN = "8274111965:AAGljIkykgOzkR-4V0q8aCmsbSD_v_6xqeE"
CHAT_ID = "YOUR_CHAT_ID_HERE" # <--- Double check this is YOUR ID

# --- THE ONLY DATES YOU WANT ---
# Using strict string matching to avoid any timezone shifting errors
TARGET_DATES = ["2026-03-11", "2026-03-12", "2026-03-13"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=20&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        print(f"Bot started. Checking {len(response)} total slots found...")

        for slot in response:
            date_only = slot['startTimestamp'][:10] # Extract YYYY-MM-DD
            
            if date_only in TARGET_DATES:
                print(f"MATCH FOUND: Sending alert for {date_only}")
                msg = (f"🚨 MARCH SLOT MATCH!\n"
                       f"Date: {date_only}\n"
                       f"Time: {slot['startTimestamp'][11:16]}\n"
                       f"Book now: https://ttp.cbp.dhs.gov/")
                send_telegram(msg)
                return 
            else:
                # This log entry proves the filter is working
                print(f"Skipping {date_only} - Not in your March 11-13 window.")

    except Exception as e:
        print(f"Error checking slots: {e}")

if __name__ == "__main__":
    check_slots()
