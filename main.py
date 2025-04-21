import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import time
import os
import logging

# Configuração inicial
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('7325319031:AAGz6fpflit6-6QYX4PQ3gSfmzjoauPvWhs')
CHAT_ID = os.getenv('5193079733')
MONITORING_URL = os.getenv('https://casino.bet365.com/Play/BacBo')

# Variáveis para controle
ultimo_sinal = None
contador_sequencia = 0

def analisar_resultados():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(MONITORING_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # MODIFIQUE ESTA PARTE CONFORME A ESTRUTURA DO SEU SITE
        resultados = []
        elementos = soup.select('.resultado-item')  # Altere para o seletor correto
        
        for elemento in elementos[:5]:  # Pega os últimos 5 resultados
            resultado = elemento.get_text().strip().lower()
            if 'player' in resultado or 'p' in resultado:
                resultados.append('P')
            elif 'banker' in resultado or 'b' in resultado:
                resultados.append('B')
        
        return resultados
    
    except Exception as e:
        logger.error(f"Erro ao analisar resultados: {e}")
        return None

def gerar_sinal(resultados):
    global ultimo_sinal, contador_sequencia
    
    if not resultados or len(resultados) < 3:
        return None
    
    # Estratégia básica: detecta sequências
    ultimos_3 = resultados[:3]
    
    # Se os últimos 3 foram Player
    if all(r == 'P' for r in ultimos_3):
        if ultimo_sinal != 'B':
            ultimo_sinal = 'B'
            contador_sequencia = 0
            return "🟥 ENTRAR NO BANKER - Sequência de 3 Players"
        else:
            contador_sequencia += 1
            if contador_sequencia >= 2:
                return "🟥 FORTE SINAL PARA BANKER - Sequência persistente"
    
    # Se os últimos 3 foram Banker
    elif all(r == 'B' for r in ultimos_3):
        if ultimo_sinal != 'P':
            ultimo_sinal = 'P'
            contador_sequencia = 0
            return "🟦 ENTRAR NO PLAYER - Sequência de 3 Bankers"
        else:
            contador_sequencia += 1
            if contador_sequencia >= 2:
                return "🟦 FORTE SINAL PARA PLAYER - Sequência persistente"
    
    return None

def enviar_sinal(context):
    try:
        resultados = analisar_resultados()
        if resultados:
            sinal = gerar_sinal(resultados)
            if sinal:
                context.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🎰 BAC BO SINAL 🎰\n\n{sinal}\n\n🔍 Últimos resultados: {' | '.join(resultados[:5])}\n\n⚠️ Gerencie seu risco!",
                    parse_mode='Markdown'
                )
    except Exception as e:
        logger.error(f"Erro ao enviar sinal: {e}")

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ Bot de sinais Bac Bo ativado!\n\nEstarei monitorando os resultados e enviando sinais automaticamente."
    )

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    
    # Verifica a cada 1 minuto
    job_queue = updater.job_queue
    job_queue.run_repeating(enviar_sinal, interval=60, first=0)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
