import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import chromadb
from chromadb.config import Settings
from langchain_openai import ChatOpenAI

# Chargement des variables d'environnement
load_dotenv()

class RAGSystem:
    def __init__(self, pdf_directory="downloads"):
        self.pdf_directory = pdf_directory
        self.documents = []
        self.db = None
        self.qa_chain = None
        
        # Configuration ChromaDB
        self.chroma_settings = Settings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory="chroma_db",
            allow_reset=True
        )
        
        self.chroma_client = chromadb.Client(self.chroma_settings)
        
        # Initialisation du modèle OpenAI GPT-4
        self.init_openai_model()
        
    def init_openai_model(self):
        """Initialise le modèle OpenAI GPT-4"""
        print("Initialisation du modèle GPT-4...")
        self.llm = ChatOpenAI(
            model="gpt-4-0125-preview",  # GPT-4 Turbo
            temperature=0.7,
            max_tokens=4096,
            streaming=True,
            verbose=True
        )
        
    def load_documents(self):
        """Charge tous les PDFs du dossier"""
        print("Chargement des documents...")
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.pdf_directory, filename)
                try:
                    loader = PyPDFLoader(file_path)
                    self.documents.extend(loader.load())
                    print(f"Document chargé : {filename}")
                except Exception as e:
                    print(f"Erreur lors du chargement de {filename}: {str(e)}")
    
    def process_documents(self):
        """Traite les documents avec une configuration optimisée"""
        print("Traitement des documents...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Augmenté car GPT-4 peut gérer plus de contexte
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        texts = text_splitter.split_documents(self.documents)
        
        # Utilisation d'OpenAI pour les embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large"  # Utilisation du dernier modèle d'embedding
        )
        
        self.db = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            client=self.chroma_client,
            collection_name="hal_documents",
            persist_directory="chroma_db"
        )
        
        self.db.persist()
        
    def setup_qa_chain(self):
        """Configure la chaîne de question-réponse"""
        print("Configuration de la chaîne QA...")
        retriever = self.db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 20,
                "lambda_mult": 0.7
            }
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )
    
    def query(self, question):
        """Pose une question au système"""
        if not self.qa_chain:
            self.setup_qa_chain()
        
        result = self.qa_chain({"query": question})
        return {
            "réponse": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
    
    def setup(self):
        """Configure tout le système"""
        self.load_documents()
        self.process_documents()
        print("Système RAG prêt à l'emploi!")

    def maintenance(self):
        """Effectue la maintenance de la base de données"""
        print("Maintenance de la base de données...")
        self.db.persist()
        self.chroma_client.persist()

def main():
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("OPENAI_API_KEY=votre_clé_api_ici\n")
        print("Veuillez configurer votre clé API OpenAI dans le fichier .env")
        return
    
    rag = RAGSystem()
    rag.setup()
    
    print("\nPosez vos questions (tapez 'quit' pour quitter):")
    
    while True:
        question = input("\nVotre question : ")
        if question.lower() == 'quit':
            break
            
        try:
            result = rag.query(question)
            print("\nRéponse :", result["réponse"])
            print("\nSources :")
            for source in result["sources"]:
                print(f"- {source.get('source', 'Source inconnue')}")
        except Exception as e:
            print(f"Erreur : {str(e)}")

if __name__ == "__main__":
    main() 