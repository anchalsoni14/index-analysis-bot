# bot.py
import requests
import datetime
import logging

# Telegram Config — Replace with your actual Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = "8397748539:AAEvU90zwCRvBhhAr-Ny6Drvy_bfTUP-u-c"
TELEGRAM_CHAT_ID = "439846137"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

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
        return []

def analyze_indices(data):
    focus_indices = ["NIFTY 50", "BANK NIFTY", "FINNIFTY", "MIDCPNIFTY"]
    result = []
    for row in data:
        if row['IndexName'] in focus_indices:
            change = float(row['PercentChange'])
            movement = "UP" if change > 0 else "DOWN"
            result.append(f"{row['IndexName']} is {movement} by {change:.2f}%")
    return result

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("Telegram message sent successfully.")
        else:
            logging.error(f"Failed to send message: {response.text}")
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

def main():
    logging.info("Starting index analysis bot...")
    data = get_index_data()
    if data:
        analysis = analyze_indices(data)
        full_message = f"📊 <b>Index Analysis - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n\n"
        full_message += "\n".join(analysis)
        print(full_message)
        send_telegram_message(full_message)
        logging.info("Analysis completed.")
    else:
        logging.info("No data to analyze.")

if __name__ == "__main__":
    main()
