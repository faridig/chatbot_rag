from db_manager import DatabaseManager
import sqlite3

def afficher_tables():
    """Affiche la structure et le contenu des tables"""
    db = DatabaseManager()
    with sqlite3.connect(db.db_name) as conn:
        cursor = conn.cursor()
        
        # Liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nTables dans la base de données:")
        for table in tables:
            table_name = table[0]
            print(f"\n=== Table: {table_name} ===")
            
            # Structure de la table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("\nStructure:")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
            
            # Contenu de la table
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            print(f"\nContenu (5 premiers enregistrements):")
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(Table vide)")

def ajouter_donnee_test():
    """Ajoute une donnée de test dans la base"""
    db = DatabaseManager()
    doc_info = {
        'doc_id': 'TEST001',
        'titre': 'Document de test',
        'auteurs': 'Auteur Test',
        'date_publication': '2024-02-03',
        'uri': 'https://test.com',
        'chemin_local': '/downloads/test.pdf',
        'nombre_pages': 10,
        'taille_fichier': 1000,
        'statut_traitement': 'test',
        'mots_cles': 'test, exemple',
        'langue': 'fr',
        'date_soumission': '2024-02-03',
        'domaine_scientifique': 'Informatique',
        'journal': 'Journal Test',
        'resume': 'Ceci est un test',
        'version': 1,
        'type_soumission': 'test',
        'type_document': 'ART',
        'hash_contenu': 'abc123'
    }
    
    try:
        db.ajouter_document(doc_info)
        print("Donnée de test ajoutée avec succès")
        
        # Ajouter un enregistrement dans l'historique
        db.enregistrer_telechargement('TEST001', 'succès', 'Test réussi')
        print("Historique de test ajouté avec succès")
    except Exception as e:
        print(f"Erreur lors de l'ajout des données de test : {e}")

def main():
    print("=== Test de la base de données HAL ===")
    
    # Afficher la structure actuelle
    print("\n1. Structure actuelle de la base de données:")
    afficher_tables()
    
    # Ajouter une donnée de test
    print("\n2. Ajout d'une donnée de test:")
    ajouter_donnee_test()
    
    # Réafficher la structure avec les nouvelles données
    print("\n3. Structure après ajout des données de test:")
    afficher_tables()
    
    # Afficher les statistiques
    print("\n4. Statistiques de la base de données:")
    db = DatabaseManager()
    stats = db.obtenir_statistiques()
    print(f"Total des documents: {stats['total_documents']}")
    print("Documents par statut:")
    for statut, nombre in stats['documents_par_statut'].items():
        print(f"- {statut}: {nombre}")

if __name__ == "__main__":
    main() 