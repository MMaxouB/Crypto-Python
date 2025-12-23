# Crypto-Python

Crypto-Python est un projet pédagogique en Python pour explorer différents types de chiffrement et déchiffrement de textes. Le projet est organisé en trois niveaux de difficulté, allant des chiffrements simples aux méthodes plus avancées. Il inclut également des outils utilitaires pour faciliter la manipulation de fichiers et du texte.

## Structure du projet

Crypto-Python/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── inputs/ # Fichiers texte à chiffrer/déchiffrer
├── outputs/ # Fichiers texte générés par les scripts
│
├── niveau1/ # Niveau 1 : Chiffrements simples
├── niveau2/ # Niveau 2 : Chiffrements intermédiaires
├── niveau3/ # Niveau 3 : Chiffrements avancés
│
├── utils/ # Fonctions utilitaires communes
└── tests/ # Tests unitaires pour chaque niveau

markdown
Copier le code

## Niveaux de chiffrement

### Niveau 1 : Chiffrements simples
- **César** : Décalage fixe des lettres du texte.
- **Vigenère** : Chiffrement par mot-clé répétitif.

### Niveau 2 : Chiffrements intermédiaires
- **Substitution monoalphabétique** : Remplacement de chaque lettre par une autre selon une clé.
- **Transposition** : Réarrangement des lettres du texte selon un motif défini.

### Niveau 3 : Chiffrements avancés
- **XOR** : Chiffrement binaire par opération XOR avec une clé.
- **Block cipher simplifié** : Chiffrement par blocs inspiré d’AES (simplifié pour l’apprentissage).

## Utilitaires
- **file_handler.py** : Lecture et écriture de fichiers.
- **text_utils.py** : Fonctions communes sur texte (nettoyage, conversion en majuscules, etc.).

## Utilisation

1. Placer vos fichiers texte à chiffrer dans le dossier `inputs/`.
2. Exécuter le script correspondant au chiffrement choisi, par exemple :

```bash
python niveau1/cesar.py
Les fichiers chiffrés seront générés dans outputs/.

Tests
Pour exécuter les tests unitaires :

bash
Copier le code
pytest tests/
Assurez-vous d’avoir installé pytest :

bash
Copier le code
pip install pytest
Installation
Cloner le projet et installer les dépendances (si nécessaire) :

bash
Copier le code
git clone https://github.com/votre-utilisateur/Crypto-Python.git
cd Crypto-Python
pip install -r requirements.txt  # si vous ajoutez des dépendances
License
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

Auteur
Votre Nom – Étudiant en cybersécurité – GitHub
