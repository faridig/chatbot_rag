"""
Gestionnaire de base de données simplifié pour CHATBOT_RAG
"""

import sqlite3
from src.config import DB_NAME
import logging

class DatabaseManager:
    def __init__(self):
        """Initialise la connexion à la base de données"""
        self.db_path = DB_NAME
        self._init_db()
        
    def _init_db(self):
        """Initialise la structure de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    titre TEXT,
                    auteurs TEXT,
                    resume TEXT,
                    date_publication TEXT,
                    statut TEXT DEFAULT 'nouveau'
                )
            ''')
            
    def ajouter_document(self, document):
        """Ajoute un nouveau document dans la base"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO documents (id, titre, auteurs, resume, date_publication)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                document['id'],
                document['titre'],
                document['auteurs'],
                document['resume'],
                document['date_publication']
            ))
            
    def obtenir_statistiques(self):
        """Retourne les statistiques de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute('SELECT COUNT(*) FROM documents').fetchone()[0]
            statuts = conn.execute('''
                SELECT statut, COUNT(*) as count 
                FROM documents 
                GROUP BY statut
            ''').fetchall()
            
        return {
            'total_documents': total,
            'documents_par_statut': dict(statuts)
        }
        
    def reset_database(self):
        """Réinitialise la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DROP TABLE IF EXISTS documents')
        self._init_db()
        logging.info("Base de données réinitialisée")

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