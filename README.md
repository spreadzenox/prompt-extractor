
# Prompt Extractor

## Description

**Prompt Extractor** est un outil Python qui analyse automatiquement un projet de développement (par exemple en PHP, JavaScript, HTML, CSS, Python, Java, C++) pour extraire un résumé structuré du projet. Il génère un prompt pour soumettre à un modèle de langage (LLM) capable de résumer l'architecture du projet, les fichiers présents, les fonctions et classes définies, ainsi que les relations entre les fichiers.

Cet outil est particulièrement utile pour ceux qui souhaitent rapidement obtenir une vue d'ensemble d'un projet de développement complexe sans devoir explorer manuellement chaque fichier.

## Fonctionnalités

- Exploration de la structure du projet et génération d'une arborescence.
- Analyse de fichiers dans plusieurs langages (PHP, JavaScript, HTML, CSS, Python, Java, C++).
- Extraction automatique des fonctions et classes définies dans chaque fichier.
- Génération d'un prompt détaillé pour soumission à un modèle de langage (LLM) pour obtenir un résumé.
- Résumés succincts de chaque fonction et classe.
- Représentation des relations entre les fichiers (imports, dépendances, etc.).
- Prise en charge des fichiers avec des extensions inconnues.

## Technologies utilisées

- **Python 3** pour la logique d'analyse.
- **LangChain** pour l'intégration avec des modèles de langage.
- **Transformers** pour la génération des prompts.
- Bibliothèques pour l'analyse de fichiers dans différents langages :
  - `esprima` pour JavaScript
  - `javalang` pour Java
  - `clang` pour C++
  - `BeautifulSoup` pour HTML
  - **etc.**

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/yourusername/prompt-extractor.git
   cd prompt-extractor
   ```

2. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Avant d'exécuter l'outil, vous devez configurer votre LLM :

1. Assurez-vous d'avoir les informations d'authentification ou d'accès pour le modèle de langage que vous souhaitez utiliser.
2. Ajoutez ces informations dans le fichier `main.py` :

   ```python
   LLM_API_KEY = "your_llm_api_key_here"
   ```

3. Modifiez le chemin du projet à analyser dans le fichier `main.py`, par exemple :

   ```python
   project_path = r"C:\chemin\vers\votre\projet"
   ```

## Utilisation

1. Après avoir modifié `main.py` avec le chemin correct de votre projet à analyser, exécutez simplement le script :

   ```bash
   python main.py
   ```

2. Le script analysera tous les fichiers du projet, générera un prompt et enverra ce prompt à un modèle de langage (LLM) pour obtenir un résumé complet.

3. Le résultat affichera :
   - Un résumé général du projet.
   - Une représentation arborescente du projet.
   - Un résumé pour chaque fichier, fonction et classe.

## Exemple de sortie

```plaintext
=== Résumé Général du Projet ===
Ce projet est une application web simple écrite en JavaScript avec Node.js...

=== Architecture du Projet ===
my-app/
├─ cert/
│  ├─ server.crt
│  ├─ server.key
├─ public/
│  ├─ scripts.js
│  ├─ styles.css
└─ templates/
   ├─ login.html
   └─ main.html

=== Détails des Fichiers ===
--- httpd.js ---
Résumé du fichier: Ce fichier gère les requêtes HTTP...
Fonctions:
 - parseCookies: Analyse les cookies...
 - serveStaticFile: Sert des fichiers statiques...
```

