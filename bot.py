import os
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NIFTY_URL = os.getenv("NIFTY_URL", "https://www.niftyindices.com/indices/equity")

# Telegram send message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            print(f"Telegram Error: {res.text}")
    except Exception as e:
        print(f"Telegram Exception: {e}")

# Scrape index data
def fetch_index_data():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(NIFTY_URL, headers=headers, timeout=30)
        response.raise_for_status()

        # Save HTML for inspection if needed
        with open("nifty_indices_raw.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, "html.parser")
        index_table = soup.find("table", {"id": "equityStockIndicesTable"})

        if not index_table:
            print("⚠️ Index table not found in HTML.")
            return []

        rows = index_table.find("tbody").find_all("tr")
        index_data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                index_name = cols[0].text.strip()
                current_value = cols[1].text.strip()
                change = cols[2].text.strip()
                percent_change = cols[3].text.strip()
                index_data.append({
                    "name": index_name,
                    "value": current_value,
                    "change": change,
                    "percent": percent_change
                })
        return index_data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching index data: {e}")
        return []

# Analyze and send signals
def analyze_and_alert(index_data):
    if not index_data:
        send_telegram_message("⚠️ No index data available for analysis.")
        return

    send_telegram_message("✅ Index Option Strategy Bot Started\n\nRunning signal analysis...")

    for index in index_data:
        try:
            percent = float(index["percent"].replace("%", "").replace(",", ""))
            name = index["name"]
            if percent >= 0.5:
                msg = f"📈 <b>{name}</b> is up by {percent}% — Consider <b>BUYING CE</b>"
                send_telegram_message(msg)
            elif percent <= -0.5:
                msg = f"📉 <b>{name}</b> is down by {percent}% — Consider <b>BUYING PE</b>"
                send_telegram_message(msg)
        except Exception as e:
            print(f"⚠️ Error analyzing {index['name']}: {e}")

# Main entry
if __name__ == "__main__":
    send_telegram_message("📡 Telegram Bot test successful!")
    print("✅ Index Option Strategy Bot Started\n")
    index_data = fetch_index_data()
    analyze_and_alert(index_data)
