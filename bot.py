import requests
from bs4 import BeautifulSoup
import time
import logging

BOT_TOKEN = "7325319031:AAGz6fpflit6-6QYX4PQ3gSfmzjoauPvWhs"
CHAT_ID = "5193079733"
URL = "https://visa.vfsglobal.com/cpv/pt/prt/application-detail"
CHECK_INTERVAL = 300  # segundos

def check_vacancy():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    if "No appointment" not in response.text and "Sem marcações disponíveis" not in response.text:
        return True
    return False

def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, data=data)

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("✅ Bot iniciado. Monitorando VFS...")

    while True:
        try:
            if check_vacancy():
                msg = f"🚨 POSSÍVEL VAGA ENCONTRADA: {URL}"
                send_telegram(msg)
                logging.info(msg)
            else:
                logging.info("❌ Nenhuma vaga encontrada.")
        except Exception as e:
            logging.error(f"Erro ao checar vaga: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
