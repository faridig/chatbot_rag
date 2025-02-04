from setuptools import setup, find_packages

setup(
    name="chatbot_rag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "sqlite3",
        "logging",
    ],
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Un chatbot utilisant l'architecture RAG avec HAL",
    python_requires=">=3.6",
) 