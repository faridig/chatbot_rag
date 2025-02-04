"""
Module de nettoyage et normalisation des données pour CHATBOT_RAG
"""

import re
from datetime import datetime
from typing import Dict, Any
from .logger import setup_logger

class DataCleaner:
    def __init__(self):
        self.logger = setup_logger('data_cleaner')

    def clean_text(self, text: str) -> str:
        """Nettoie un texte"""
        if not text:
            return ""
        
        # Suppression des caractères spéciaux indésirables
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        # Normalisation des espaces
        text = ' '.join(text.split())
        return text.strip()

    def normalize_date(self, date_str: str) -> str:
        """Normalise une date au format YYYY-MM-DD"""
        if not date_str:
            return ""
        
        try:
            # Gestion des différents formats possibles
            formats = [
                "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y",
                "%Y-%m", "%Y", "%Y-%m-%dT%H:%M:%SZ"
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue
                    
            self.logger.warning(f"Format de date non reconnu : {date_str}")
            return date_str
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la normalisation de la date {date_str}: {e}")
            return ""

    def clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Nettoie et normalise les métadonnées d'un document"""
        cleaned = {}
        
        try:
            # Nettoyage des champs textuels
            text_fields = ['titre', 'auteurs', 'mots_cles', 'resume', 
                          'domaine_scientifique', 'journal', 'type_document']
            for field in text_fields:
                if field in metadata:
                    cleaned[field] = self.clean_text(str(metadata.get(field, '')))

            # Normalisation des dates
            date_fields = ['date_publication', 'date_soumission']
            for field in date_fields:
                if field in metadata:
                    cleaned[field] = self.normalize_date(str(metadata.get(field, '')))

            # Normalisation de la langue
            if 'langue' in metadata:
                langue = str(metadata['langue']).lower()
                cleaned['langue'] = {
                    'fr': 'fr',
                    'fre': 'fr',
                    'french': 'fr',
                    'en': 'en',
                    'eng': 'en',
                    'english': 'en'
                }.get(langue, langue)

            # Conversion et validation des champs numériques
            cleaned['nombre_pages'] = max(0, int(metadata.get('nombre_pages', 0)))
            cleaned['taille_fichier'] = max(0, int(metadata.get('taille_fichier', 0)))
            cleaned['version'] = max(1, int(metadata.get('version', 1)))

            # Champs qui ne nécessitent pas de nettoyage
            cleaned['doc_id'] = str(metadata['doc_id'])
            cleaned['uri'] = str(metadata.get('uri', ''))
            cleaned['chemin_local'] = str(metadata.get('chemin_local', ''))
            cleaned['hash_contenu'] = str(metadata.get('hash_contenu', ''))
            cleaned['statut_traitement'] = str(metadata.get('statut_traitement', 'nouveau'))

            # Validation finale
            self._validate_cleaned_data(cleaned)
            
            return cleaned

        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage des métadonnées : {e}")
            raise

    def _validate_cleaned_data(self, data: Dict[str, Any]) -> None:
        """Valide les données nettoyées"""
        required_fields = ['doc_id', 'titre', 'auteurs']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Champ requis manquant ou vide après nettoyage : {field}")

        if data.get('nombre_pages', 0) < 0:
            raise ValueError("Le nombre de pages ne peut pas être négatif")

        if data.get('taille_fichier', 0) < 0:
            raise ValueError("La taille du fichier ne peut pas être négative") 