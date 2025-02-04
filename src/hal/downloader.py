import os
import requests
import hashlib
from io import BytesIO
import PyPDF2
from ..utils.logger import setup_logger
from ..utils.data_cleaner import DataCleaner

class HALDownloader:
    def __init__(self, db_manager):
        self.logger = setup_logger('hal_downloader')
        self.db_manager = db_manager
        self.data_cleaner = DataCleaner()
        self.downloads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'downloads')
        
        if not os.path.exists(self.downloads_dir):
            os.makedirs(self.downloads_dir)
    
    def download_documents(self, limit=100):
        """Télécharge les documents depuis HAL"""
        self.logger.info(f"Démarrage du téléchargement (limite: {limit} documents)")
        
        # Recherche des documents
        documents = self._search_hal_documents(limit)
        if not documents:
            self.logger.warning("Aucun document trouvé")
            return
        
        self.logger.info(f"{len(documents)} documents trouvés")
        
        # Téléchargement des documents
        for doc in documents:
            if 'fileMain_s' in doc:
                self._process_document(doc)
    
    def _search_hal_documents(self, limit):
        """Recherche des documents dans HAL"""
        url = "http://api.archives-ouvertes.fr/search/"
        params = {
            "q": "*:*",
            "rows": limit,
            "wt": "json",
            "fl": (
                "docid,label_s,fileMain_s,uri_s,"
                "authFullName_s,keyword_s,language_s,"
                "publicationDate_s,submittedDate_s,domain_s,"
                "journalTitle_s,abstract_s,version_i,"
                "submitType_s,docType_s"
            )
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('response', {}).get('docs', [])
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche HAL : {e}")
            return []
    
    def _process_document(self, doc):
        """Traite un document"""
        doc_id = doc['docid']
        self.logger.info(f"Traitement du document {doc_id}")
        
        # Extraction des métadonnées
        metadata = self._extract_metadata(doc)
        
        # Nettoyage des métadonnées
        try:
            cleaned_metadata = self.data_cleaner.clean_metadata(metadata)
            
            # Téléchargement du PDF
            if self._download_pdf(doc['fileMain_s'], cleaned_metadata):
                self.db_manager.ajouter_document(cleaned_metadata)
                
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage des métadonnées pour {doc_id}: {e}")
    
    def _extract_metadata(self, doc):
        """Extrait les métadonnées d'un document"""
        # Extraction des auteurs et titre
        label = doc.get('label_s', '')
        auteurs, titre = self._split_authors_title(label)
        
        return {
            'doc_id': doc['docid'],
            'titre': titre,
            'auteurs': auteurs,
            'uri': doc.get('uri_s', ''),
            'date_publication': doc.get('publicationDate_s', ''),
            'mots_cles': ', '.join(doc.get('keyword_s', [])) if isinstance(doc.get('keyword_s'), list) else '',
            'langue': doc.get('language_s', ''),
            'date_soumission': doc.get('submittedDate_s', ''),
            'domaine_scientifique': doc.get('domain_s', ''),
            'journal': doc.get('journalTitle_s', ''),
            'resume': doc.get('abstract_s', ''),
            'version': int(doc.get('version_i', 0) or 0),
            'type_soumission': doc.get('submitType_s', ''),
            'type_document': doc.get('docType_s', '')
        }
    
    def _split_authors_title(self, label):
        """Sépare les auteurs du titre"""
        try:
            parts = label.split('. ', 1)
            return (parts[0], parts[1]) if len(parts) == 2 else ('', label)
        except Exception as e:
            self.logger.error(f"Erreur lors de la séparation auteurs/titre : {e}")
            return ('', label)
    
    def _download_pdf(self, url, metadata):
        """Télécharge un PDF"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Vérification du type de contenu
            if 'application/pdf' not in response.headers.get('content-type', '').lower():
                self.logger.error(f"Type de contenu invalide pour {metadata['doc_id']}")
                return False
            
            # Vérification du PDF
            pdf_content = response.content
            if not self._verify_pdf(pdf_content, metadata):
                return False
            
            # Sauvegarde du fichier
            filename = f"{metadata['doc_id']}.pdf"
            filepath = os.path.join(self.downloads_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(pdf_content)
            
            # Mise à jour des métadonnées
            metadata.update({
                'chemin_local': filepath,
                'hash_contenu': self._calculate_hash(pdf_content),
                'taille_fichier': len(pdf_content),
                'statut_traitement': 'téléchargé'
            })
            
            self.logger.info(f"Document {metadata['doc_id']} téléchargé avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement de {metadata['doc_id']} : {e}")
            return False
    
    def _verify_pdf(self, content, metadata):
        """Vérifie la validité d'un PDF"""
        try:
            pdf = PyPDF2.PdfReader(BytesIO(content))
            metadata['nombre_pages'] = len(pdf.pages)
            return True
        except Exception as e:
            self.logger.error(f"PDF invalide pour {metadata['doc_id']} : {e}")
            return False
    
    def _calculate_hash(self, content):
        """Calcule le hash SHA-256 du contenu"""
        return hashlib.sha256(content).hexdigest() 