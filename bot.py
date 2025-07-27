import os
import logging
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="index_analysis_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.info(f"TELEGRAM_TOKEN: {'Set' if TELEGRAM_TOKEN else 'Missing'}")
logging.info(f"TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID if TELEGRAM_CHAT_ID else 'Missing'}")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Telegram credentials are missing.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logging.info(f"Telegram message sent: {message}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Telegram error: {e.response.text if hasattr(e, 'response') and e.response else str(e)}")

def fetch_data():
    try:
        # Replace this with your actual source
        url = "https://www.niftyindices.com/indices/equity"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # For placeholder: simulate parsed data
        return pd.DataFrame({
            "Index": ["NIFTY MIDCAP 50", "NIFTY BANK"],
            "Signal": ["Buy", "Sell"],
            "Strength": [85, 42]
        })
    except Exception as e:
        logging.error(f"Exception occurred while fetching data: {str(e)}")
        return None

def main():
    logging.info("Starting index analysis bot...")

    send_telegram_message("✅ <b>Index Option Strategy Bot Started</b>\n\nRunning signal analysis...")

    data = fetch_data()

    if data is None or data.empty:
        logging.warning("No data to analyze.")
        send_telegram_message("⚠️ No index data available for analysis.")
        return

    summary = "\n".join([
        f"🔹 <b>{row['Index']}</b>: {row['Signal']} (Strength: {row['Strength']})"
        for _, row in data.iterrows()
    ])

    message = f"<b>📊 Index Analysis Signals:</b>\n\n{summary}"
    send_telegram_message(message)

if __name__ == "__main__":
    main()
