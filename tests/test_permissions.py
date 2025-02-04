import os
import sqlite3
from pathlib import Path

def verifier_environnement():
    """Vérifie l'environnement de travail"""
    print("=== Vérification de l'environnement ===")
    
    # Répertoire courant
    current_dir = os.getcwd()
    print(f"Répertoire courant : {current_dir}")
    print(f"Permissions du répertoire : {oct(os.stat(current_dir).st_mode)[-3:]}")
    
    # Utilisateur courant
    print(f"Utilisateur effectif : {os.geteuid()}")
    print(f"Groupe effectif : {os.getegid()}")
    
    # Chemin de la base de données
    db_path = os.path.abspath("hal_documents.db")
    print(f"\nChemin de la base de données : {db_path}")
    
    # Vérifier si le fichier existe
    if os.path.exists(db_path):
        print("La base de données existe")
        print(f"Permissions : {oct(os.stat(db_path).st_mode)[-3:]}")
        print(f"Taille : {os.path.getsize(db_path)} octets")
    else:
        print("La base de données n'existe pas encore")
    
    # Tester la création d'un fichier
    test_file = "test_write.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("Test d'écriture")
        print("\nTest d'écriture de fichier : OK")
        os.remove(test_file)
    except Exception as e:
        print(f"\nErreur lors du test d'écriture : {e}")
    
    # Tester SQLite
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        print("Test SQLite en mémoire : OK")
        conn.close()
    except Exception as e:
        print(f"Erreur lors du test SQLite : {e}")

if __name__ == "__main__":
    verifier_environnement() 