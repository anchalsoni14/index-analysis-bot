# bot.py
import requests
import datetime
import logging

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

def main():
    logging.info("Starting index analysis bot...")
    data = get_index_data()
    if data:
        analysis = analyze_indices(data)
        for line in analysis:
            print(line)
            logging.info(line)
    else:
        logging.info("No data to analyze.")

if __name__ == "__main__":
    main()
