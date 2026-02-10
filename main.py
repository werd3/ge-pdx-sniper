import requests
from datetime import datetime

# CONFIG
LOCATION_ID = 5005
TOKEN = "8274111965:AAGljIkykgOzkR-4V0q8aCmsbSD_v_6xqeE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

# THE ONLY VALID WINDOW
TARGETS = ["2026-03-11", "2026-03-12", "2026-03-13"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_slots():
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=30&locationId={LOCATION_ID}&minimum=1"
    try:
        response = requests.get(url).json()
        print(f"--- V3.0 SCAN START ---")
        
        for slot in response:
            date_only = slot['startTimestamp'][:10]
            
            # THE SAFETY LOCK
            if date_only not in TARGETS:
                print(f"DEBUG: Blocking {date_only}")
                continue # Moving to the next slot without sending anything
            
            # THE ONLY WAY A MESSAGE SENDS
            msg = f"✅ MATCH (V3.0)\nDate: {date_only}\nhttps://ttp.cbp.dhs.gov/"
            send_telegram(msg)
            return

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slots()
