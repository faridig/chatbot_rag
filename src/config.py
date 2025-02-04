"""
Configuration simplifiée du CHATBOT_RAG
"""

import os
from pathlib import Path

# Chemins principaux
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DOWNLOADS_DIR = BASE_DIR / 'downloads'
LOGS_DIR = BASE_DIR / 'logs'

# Base de données
DB_NAME = DATA_DIR / 'hal_documents.db'

# API HAL
HAL_API_URL = "http://api.archives-ouvertes.fr/search/"
HAL_DEFAULT_LIMIT = 10  # Réduit pour les tests
HAL_SEARCH_PARAMS = {
    "q": "computer science",  # Recherche en informatique
    "wt": "json",
    "fl": "docid,label_s,fileMain_s,uri_s,authFullName_s,abstract_s,publicationDate_s"
}

# Création automatique des répertoires
for directory in [DATA_DIR, DOWNLOADS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True) 