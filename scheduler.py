#!/usr/bin/env python3
"""
Scheduler para DailyPush - Executa commits automáticos em intervalos regulares
"""

import schedule
import time
import logging
import sys
from pathlib import Path

# Adiciona o diretório atual ao path para importar daily_push
sys.path.append(str(Path(__file__).parent))

from daily_push import DailyPush

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_daily_push():
    """Executa o DailyPush"""
    try:
        daily_push = DailyPush()
        success = daily_push.daily_routine()
        
        if success:
            logger.info("✅ DailyPush executado com sucesso!")
        else:
            logger.error("❌ DailyPush falhou!")
            
    except Exception as e:
        logger.error(f"Erro ao executar DailyPush: {e}")

def main():
    """Função principal do scheduler"""
    logger.info("🚀 Iniciando DailyPush Scheduler...")
    
    # Agenda execução diária às 9:00 AM
    schedule.every().day.at("09:00").do(run_daily_push)
    
    # Agenda execução diária às 6:00 PM (alternativa)
    schedule.every().day.at("18:00").do(run_daily_push)
    
    # Para testes, também agenda execução a cada hora
    # schedule.every().hour.do(run_daily_push)
    
    logger.info("📅 Agendamentos configurados:")
    logger.info("   - Diário às 09:00")
    logger.info("   - Diário às 18:00")
    
    logger.info("⏰ Scheduler rodando... Pressione Ctrl+C para parar")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
            
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler interrompido pelo usuário")
        sys.exit(0)

if __name__ == "__main__":
    main()
