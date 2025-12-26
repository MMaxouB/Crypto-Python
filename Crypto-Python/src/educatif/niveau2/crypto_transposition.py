import math
import os

# Base project directory (repo root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Chemins vers les fichiers d'entrée pour la transposition (texte clair et texte chiffré)
INPUT_FILE_TEXT = os.path.join(BASE_DIR, "inputs", "inputs_transpostion", "input_text_transposition.txt") # fichier d'entrée texte
INPUT_FILE_CRYPT = os.path.join(BASE_DIR, "inputs", "inputs_transpostion", "input_crypt_transposition.txt")  # fichier d'entrée chiffré

# Nombre de colonnes utilisé comme clé pour la transposition
COLUMNS_KEY = 4 # Clé de chiffrement/déchiffrement (nombre de colonnes)

def read_file(file_path):
    """Lit le contenu d'un fichier et le retourne en tant que chaîne de caractères."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def create_matrix(text, key):
    """Crée une matrice pour le chiffrement/déchiffrement par transposition."""
    # Calcul du nombre de lignes nécessaires (arrondi supérieur)
    rows = math.ceil(len(text) / key)
    # On initialise une matrice (liste de listes) rows x key contenant des chaînes vides
    matrix = [[''] * key for _ in range(rows)]
    # Remplissage ligne par ligne à partir du texte
    for i in range(rows):
        for j in range(key):
            # Calcul de l'index dans la chaîne d'origine correspondant à la position (i,j)
            index = i * key + j
            if index < len(text):
                # Placer le caractère correspondant dans la cellule
                matrix[i][j] = text[index]
            else:
                # Si on dépasse la longueur du texte, on ajoute un caractère de remplissage spécial
                matrix[i][j] = '¤'  # Remplir avec '¤' si nécessaire
    return matrix

def crypt_transposition(input_text, key):
    matrix = create_matrix(input_text, key)
    result = ""
    # Lecture par colonnes (transpose) : concatène les colonnes du haut vers le bas
    for j in range(key):
        for i in range(len(matrix)):
            result += matrix[i][j]
    return result

def decrypt_transposition(input_crypt, key):
    rows = math.ceil(len(input_crypt) / key)
    matrix = [[''] * key for _ in range(rows)]
    index = 0
    # Reconstruire la matrice en remplissant par colonne à partir du texte chiffré
    for j in range(key):
        for i in range(rows):
            if index < len(input_crypt):
                matrix[i][j] = input_crypt[index]
                index += 1
    # Relecture ligne par ligne pour retrouver le texte original
    result = ""
    for i in range(rows):
        for j in range(key):
            result += matrix[i][j]
    # Supprimer les caractères de remplissage utilisés lors du chiffrement
    return result.replace('¤', '')  # Retirer les caractères de remplissage

def main():
    choice = input("Voulez-vous crypter ou décrypter le texte du fichier d'entrée ? (c/d) : ")
    if choice.lower() == 'c':
        input_text = read_file(INPUT_FILE_TEXT)
        encrypted_text = crypt_transposition(input_text, COLUMNS_KEY)
        with open(os.path.join(BASE_DIR, "outputs", "transposition", "output_crypt_transposition.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(encrypted_text)
    elif choice.lower() == 'd':
        input_crypt = read_file(INPUT_FILE_CRYPT)
        decrypted_text = decrypt_transposition(input_crypt, COLUMNS_KEY)
        with open(os.path.join(BASE_DIR, "outputs", "transposition", "output_decrypt_transposition.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(decrypted_text)
    else:
        print("Choix invalide. Veuillez entrer 'c' pour crypter ou 'd' pour décrypter.")
        main()

if __name__ == "__main__":
    main()
    # Exemple d'utilisation