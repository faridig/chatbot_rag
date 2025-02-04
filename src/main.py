#!/usr/bin/env python3
"""
Point d'entrée principal du CHATBOT_RAG - Version simplifiée
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from src.database.manager import DatabaseManager
from src.hal.downloader import HALDownloader
from src.utils.logger import setup_logging

def afficher_menu():
    """Affiche le menu principal"""
    print("\n=== CHATBOT RAG - Menu Principal ===")
    print("1. Télécharger des documents")
    print("2. Voir les statistiques")
    print("3. Réinitialiser la base de données")
    print("4. Quitter")
    return input("Choisissez une option (1-4): ")

def main():
    # Configuration du logging
    logger = setup_logging()
    logger.info("Démarrage de l'application")
    
    try:
        # Initialisation de la base de données
        db = DatabaseManager()
        logger.info("Base de données initialisée")
        
        while True:
            choix = afficher_menu()
            
            try:
                if choix == "1":
                    logger.info("Démarrage du téléchargement...")
                    downloader = HALDownloader(db)
                    downloader.download_documents()
                    logger.info("Téléchargement terminé")
                    
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
                        logger.info("Base de données réinitialisée")
                        print("Base de données réinitialisée avec succès.")
                    
                elif choix == "4":
                    logger.info("Arrêt de l'application")
                    print("Au revoir!")
                    break
                    
                else:
                    print("Option invalide. Veuillez réessayer.")
                    
            except Exception as e:
                logger.error(f"Erreur lors de l'exécution de l'option {choix}: {str(e)}")
                print("Une erreur est survenue. Consultez les logs pour plus de détails.")
                
    except Exception as e:
        logger.error(f"Erreur critique: {str(e)}")
        print("Erreur critique. Impossible de continuer.")
        sys.exit(1)

if __name__ == "__main__":
    main() 