import logging
import os
from datetime import datetime

def setup_logger(name='hal_manager'):
    """Configure et retourne un logger"""
    
    # Créer le dossier logs s'il n'existe pas
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Nom du fichier de log avec la date
    log_file = os.path.join(logs_dir, f'hal_manager_{datetime.now().strftime("%Y%m%d")}.log')
    
    # Configuration du logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Handler pour fichier
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Format des messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Ajout des handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 