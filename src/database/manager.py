"""
Gestionnaire de base de données simplifié pour CHATBOT_RAG
"""

import sqlite3
import logging
from pathlib import Path
from src.config import DB_NAME

class DatabaseManager:
    def __init__(self):
        """Initialise la connexion à la base de données"""
        self.db_path = DB_NAME
        self.logger = logging.getLogger(__name__)
        self._init_db()
        
    def _init_db(self):
        """Initialise la structure de la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        doc_id TEXT PRIMARY KEY,
                        titre TEXT,
                        auteurs TEXT,
                        resume TEXT,
                        date_publication TEXT,
                        uri TEXT,
                        chemin_local TEXT,
                        statut TEXT DEFAULT 'nouveau'
                    )
                ''')
                conn.commit()
                self.logger.info(f"Base de données initialisée : {self.db_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation de la base : {e}")
            raise
            
    def ajouter_document(self, document):
        """Ajoute un nouveau document dans la base"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO documents 
                    (doc_id, titre, auteurs, resume, date_publication, uri, chemin_local, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    document.get('doc_id', ''),
                    document.get('titre', ''),
                    document.get('auteurs', ''),
                    document.get('resume', ''),
                    document.get('date_publication', ''),
                    document.get('uri', ''),
                    document.get('chemin_local', ''),
                    document.get('statut', 'nouveau')
                ))
                conn.commit()
                self.logger.info(f"Document ajouté/mis à jour : {document.get('doc_id')}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout du document : {e}")
            raise
            
    def obtenir_statistiques(self):
        """Retourne les statistiques de la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Nombre total de documents
                cursor.execute('SELECT COUNT(*) FROM documents')
                total = cursor.fetchone()[0]
                
                # Documents par statut
                cursor.execute('''
                    SELECT statut, COUNT(*) as count 
                    FROM documents 
                    GROUP BY statut
                ''')
                statuts = dict(cursor.fetchall())
                
                return {
                    'total_documents': total,
                    'documents_par_statut': statuts
                }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des statistiques : {e}")
            return {'total_documents': 0, 'documents_par_statut': {}}
        
    def reset_database(self):
        """Réinitialise la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DROP TABLE IF EXISTS documents')
                conn.commit()
            self._init_db()
            self.logger.info("Base de données réinitialisée avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de la réinitialisation : {e}")
            raise

    def rechercher_documents(self, criteres):
        """Recherche des documents selon des critères"""
        query = "SELECT * FROM documents WHERE 1=1"
        params = []
        
        if 'titre' in criteres:
            query += " AND titre LIKE ?"
            params.append(f"%{criteres['titre']}%")
        
        if 'auteurs' in criteres:
            query += " AND auteurs LIKE ?"
            params.append(f"%{criteres['auteurs']}%")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall() 