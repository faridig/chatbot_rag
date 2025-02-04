# CHATBOT RAG

Un chatbot intelligent utilisant l'architecture RAG (Retrieval-Augmented Generation) pour interagir avec les documents HAL (Archives Ouvertes).

## 🚀 Fonctionnalités

- Téléchargement automatique de documents depuis HAL
- Gestion de base de données SQLite pour le stockage
- Interface en ligne de commande interactive
- Système de logging pour le suivi des opérations

## 📋 Prérequis

- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)
- Environnement virtuel (recommandé)

## 🛠️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/chatbot_rag.git
cd chatbot_rag
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installez les dépendances :
```bash
pip install -e .
```

## 🎮 Utilisation

Lancez l'application :
```bash
python src/main.py
```

Le menu principal vous permettra de :
1. Télécharger des documents
2. Voir les statistiques
3. Réinitialiser la base de données
4. Quitter

## 📁 Structure du Projet

```
chatbot_rag/
├── src/
│   ├── database/      # Gestion de la base de données
│   ├── hal/           # Interface avec l'API HAL
│   └── main.py        # Point d'entrée
├── data/              # Stockage des données
├── logs/              # Fichiers de logs
└── downloads/         # Documents téléchargés
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 