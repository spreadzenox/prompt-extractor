import os
from utils.file_utils import get_project_structure
from utils.dependency_extractor import extract_dependencies
from analyzers.language_analyzer import LanguageAnalyzer
from langchain_huggingface import HuggingFaceEndpoint

# Définir la clé API de Hugging Face
SECRET_KEY = ""
os.environ["HUGGINGFACEHUB_API_TOKEN"] = SECRET_KEY

def setup_huggingface_endpoint():
    # Initialiser HuggingFaceEndpoint pour utiliser l'API de Huggingface
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=512, temperature=0.7, token=SECRET_KEY)
    return llm

def main(project_path):
    # Étape 1 : Obtenir la structure du projet
    project_tree = get_project_structure(project_path)
    
    # Étape 2 : Analyser les fichiers
    analyzer = LanguageAnalyzer()
    files_info = analyzer.analyze_project(project_path)
    
    # Étape 3 : Extraire les dépendances
    dependencies = extract_dependencies(files_info)
    
    # Étape 4 : Générer les résumés
    llm = setup_huggingface_endpoint()
    
    # Résumé général du projet
    project_summary_prompt = f"Voici une analyse du projet basé sur les fichiers suivants: {list(files_info.keys())}. " \
                             f"Donne un résumé global du projet, en précisant les objectifs et les technologies utilisées."
    project_summary = llm(project_summary_prompt)
    
    # Générer la représentation arborescente
    tree_representation = project_tree.render()
    
    # Générer les résumés pour chaque fichier
    for file_path, info in files_info.items():
        content_summary_prompt = f"Résume en une ou deux phrases le fichier '{file_path}'. Donne juste son rôle général."
        content_summary = llm(content_summary_prompt)
        info['summary'] = content_summary
        
        # Résumer chaque fonction et classe
        for func in info['functions']:
            func_summary_prompt = f"Résume brièvement la fonction '{func}' dans le fichier '{file_path}' en une seule phrase."
            func_summary = llm(func_summary_prompt)
            info['function_summaries'][func] = func_summary
        
        for cls in info['classes']:
            cls_summary_prompt = f"Résume brièvement la classe '{cls}' dans le fichier '{file_path}' en une seule phrase."
            cls_summary = llm(cls_summary_prompt)
            info['class_summaries'][cls] = cls_summary
    
    # Afficher le résumé général
    print("=== Résumé Général du Projet ===")
    print(project_summary)
    print("\n=== Architecture du Projet ===")
    print(tree_representation)
    print("\n=== Détails des Fichiers ===")
    for file_path, info in files_info.items():
        print(f"\n--- {file_path} ---")
        print(f"Résumé du fichier: {info['summary']}")
        if info['functions']:
            print("Fonctions:")
            for func in info['functions']:
                print(f" - {func}: {info['function_summaries'][func]}")
        if info['classes']:
            print("Classes:")
            for cls in info['classes']:
                print(f" - {cls}: {info['class_summaries'][cls]}")
        if info['dependencies']:
            print(f"Dépendances: {', '.join(info['dependencies'])}")
    
if __name__ == "__main__":
    project_path = r"C:\Users\hpesq\OneDrive\Bureau\ultimate-member" # Chemin du projet à analyser
    main(project_path)
