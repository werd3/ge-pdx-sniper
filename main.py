import requests
from datetime import datetime

# --- CONFIGURATION ---
LOCATION_ID = 5005  # Portland (PDX)
TOKEN = "8274111965:AAGljIkykgOzkR-4V0q8aCmsbSD_v_6xqeE"
CHAT_ID = "YOUR_CHAT_ID_HERE" 

# --- THE ONLY DATES YOU WANT (STRICT) ---
TARGET_DATES = ["2026-03-11", "2026-03-12", "2026-03-13"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=30&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        print(f"--- STRICT SCAN START: Checking {len(response)} slots ---")

        for slot in response:
            date_only = slot['startTimestamp'][:10] # e.g. "2026-02-18"
            
            if date_only in TARGET_DATES:
                print(f"!!! MATCH FOUND !!! Date: {date_only}")
                msg = f"🚨 MARCH {date_only} FOUND!\nTime: {slot['startTimestamp'][11:16]}\nBook: https://ttp.cbp.dhs.gov/"
                send_telegram(msg)
                return 
            else:
                # This log entry proves the filter is working
                print(f"Skipping {date_only}: Not in March 11-13 window.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slots()
