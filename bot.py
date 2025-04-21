import os
import requests
from bs4 import BeautifulSoup
import time
import logging

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))  # segundos entre checagens

URL = "https://visa.vfsglobal.com/cpv/pt/prt/application-detail"

def check_vacancy():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Aqui você adapta com base no conteúdo real da página:
    if "No appointments available" not in response.text:
        return True
    return False

def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    requests.post(telegram_url, data=payload)

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🔍 Iniciando monitoramento da VFS Global...")

    while True:
        try:
            if check_vacancy():
                send_telegram("🚨 POSSÍVEL VAGA ENCONTRADA na VFS Global: " + URL)
                logging.info("✅ Vaga encontrada e alerta enviado.")
            else:
                logging.info("❌ Nenhuma vaga ainda.")
        except Exception as e:
            logging.error(f"Erro ao verificar vaga: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
