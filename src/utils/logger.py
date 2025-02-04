"""
Configuration du système de logging
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from src.config import LOGS_DIR

def setup_logging():
    """Configure le système de logging global"""
    
    # Création du répertoire de logs si nécessaire
    Path(LOGS_DIR).mkdir(exist_ok=True)
    
    # Nom du fichier de log avec la date
    log_file = LOGS_DIR / f'hal_manager_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Handler pour la console
            logging.StreamHandler(),
            # Handler pour le fichier
            logging.FileHandler(log_file)
        ]
    )
    
    # Logger spécifique pour les erreurs
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)
    
    error_file = LOGS_DIR / 'erreurs_hal.log'
    error_handler = logging.FileHandler(error_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    error_logger.addHandler(error_handler)
    
    return logging.getLogger(__name__) 