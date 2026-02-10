import requests
import os
from datetime import datetime
import pytz

# CONFIGURATION
LOCATION_ID = 5005  # Portland (PDX)
TOKEN = "8274111965:AAGljIkykgOzkR-4V0q8aCmsbSD_v_6xqeE"
CHAT_ID = "YOUR_CHAT_ID_HERE" 

# THE SPECIFIC MARCH WINDOW
# We use strings for easy comparison to avoid timezone "shuffling"
TARGET_DATES = ["2026-03-11", "2026-03-12", "2026-03-13"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=15&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        print(f"--- Checking {len(response)} total slots found at PDX ---")
        
        if not response:
            print("Zero slots available at PDX right now.")
            return

        for slot in response:
            # Extract just the YYYY-MM-DD part from the government's data
            slot_date = slot['startTimestamp'][:10] 
            print(f"Found slot on: {slot_date}") # This shows up in your GitHub logs

            if slot_date in TARGET_DATES:
                print(f"!!! MATCH FOUND for {slot_date} !!!")
                msg = (f"🚨 PORTLAND SLOT MATCH!\n"
                       f"Date: {slot_date}\n"
                       f"Time: {slot['startTimestamp'][11:16]}\n"
                       f"Book now: https://ttp.cbp.dhs.gov/")
                send_telegram(msg)
                return 
        
        print("Done. No slots matched your March 11-13 window.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slots()
