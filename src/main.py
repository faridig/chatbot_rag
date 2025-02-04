#!/usr/bin/env python3
"""
Point d'entrée principal du CHATBOT_RAG - Version simplifiée
"""

import os
import sys

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.manager import DatabaseManager
from src.hal.downloader import HALDownloader
import logging

def configurer_logging():
    """Configure le système de logging basique"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def afficher_menu():
    """Affiche le menu principal"""
    print("\n=== CHATBOT RAG - Menu Principal ===")
    print("1. Télécharger des documents")
    print("2. Voir les statistiques")
    print("3. Réinitialiser la base de données")
    print("4. Quitter")
    return input("Choisissez une option (1-4): ")

def main():
    logger = configurer_logging()
    db = DatabaseManager()
    
    while True:
        choix = afficher_menu()
        
        try:
            if choix == "1":
                logger.info("Démarrage du téléchargement...")
                downloader = HALDownloader(db)
                downloader.download_documents()
                
            elif choix == "2":
                stats = db.obtenir_statistiques()
                print("\n=== Statistiques ===")
                print(f"Documents totaux: {stats['total_documents']}")
                for statut, nombre in stats['documents_par_statut'].items():
                    print(f"{statut}: {nombre}")
                    
            elif choix == "3":
                confirmation = input("Êtes-vous sûr de vouloir réinitialiser ? (oui/non): ")
                if confirmation.lower() == "oui":
                    db.reset_database()
                    print("Base de données réinitialisée.")
                    
            elif choix == "4":
                print("Au revoir!")
                break
                
            else:
                print("Option invalide. Veuillez réessayer.")
                
        except Exception as e:
            logger.error(f"Erreur: {str(e)}")
            print("Une erreur est survenue. Consultez les logs pour plus de détails.")

if __name__ == "__main__":
    main() 