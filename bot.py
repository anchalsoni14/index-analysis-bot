# bot.py
import requests
import datetime
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# ====== CONFIGURE TELEGRAM ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("TELEGRAM_TOKEN:", bool(TELEGRAM_TOKEN))
print("TELEGRAM_CHAT_ID:", TELEGRAM_CHAT_ID)

def send_telegram_message(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload)
            if res.status_code != 200:
                logging.warning(f"Telegram error: {res.text}")
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")
    else:
        logging.warning("Telegram credentials not set.")

def get_index_data():
    url = "https://www.niftyindices.com/Backpage.aspx/getindicesData"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://www.niftyindices.com/",
    }
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code == 200:
            return response.json()["d"]
        else:
            logging.error("Failed to fetch index data")
            return []
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        send_telegram_message(f"⚠️ *Error fetching index data:* {e}")
        return []

def analyze_indices(data):
    focus_indices = ["NIFTY 50", "BANK NIFTY", "FINNIFTY", "MIDCPNIFTY"]
    result = []
    for row in data:
        if row['IndexName'] in focus_indices:
            change = float(row['PercentChange'])
            movement = "UP" if change > 0 else "DOWN"
            result.append(f"*{row['IndexName']}* is *{movement}* by *{change:.2f}%*")
    return result

def main():
    logging.info("Starting index analysis bot...")
    data = get_index_data()
    if data:
        analysis = analyze_indices(data)
        message = "\n".join(analysis)
        if message:
            logging.info(message)
            send_telegram_message(f"📊 *Index Update:*\n\n{message}")
        else:
            logging.info("No relevant index movement found.")
            send_telegram_message("ℹ️ No significant index movement today.")
    else:
        logging.info("No data to analyze.")

if __name__ == "__main__":
    main()
