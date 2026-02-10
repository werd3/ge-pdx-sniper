import requests
import os
from datetime import datetime
import pytz # This handles the Spokane time zone

# CONFIGURATION
LOCATION_ID = 5005  # Portland (PDX)
TOKEN = "8274111965:AAGljIkykgOzkR-4V0q8aCmsbSD_v_6xqeE"
CHAT_ID = "YOUR_CHAT_ID_HERE" 

# DATE FILTERS: Only your specific trip home dates
START_FILTER = datetime.strptime("2026-03-11", "%Y-%m-%d")
END_FILTER = datetime.strptime("2026-03-13", "%Y-%m-%d")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_heartbeat():
    # Gets the current time in Spokane
    spokane_tz = pytz.timezone('America/Los_Angeles')
    now = datetime.now(spokane_tz)
    
    # If it's between 9:00 AM and 9:15 AM, send a heartbeat
    if now.hour == 9 and now.minute < 15:
        send_telegram("☀️ Good morning! Your Portland Global Entry bot is awake and scanning.")

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=10&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        if not response:
            return

        for slot in response:
            slot_date_str = slot['startTimestamp'][:10] 
            slot_date = datetime.strptime(slot_date_str, "%Y-%m-%d")
            
            if START_FILTER <= slot_date <= END_FILTER:
                msg = f"🚨 PORTLAND SLOT FOUND!\nDate: {slot['startTimestamp']}\nLogin: https://ttp.cbp.dhs.gov/"
                send_telegram(msg)
                return 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_heartbeat()
    check_slots()
