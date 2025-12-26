import string
import os

alphabet_lower = string.ascii_lowercase # alphabet français avec accents minuscules
alphabet_upper = string.ascii_uppercase # alphabet français avec accents majuscules

# Robust paths: compute project root (repo) from file location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

INPUT_FILE_TEXT = os.path.join(BASE_DIR, "inputs", "inputs_cesar", "input_text_cesar.txt")
INPUT_FILE_CRYPT = os.path.join(BASE_DIR, "inputs", "inputs_cesar", "input_crypt_cesar.txt") # fichier d'entrée chiffré

n = 3  # décalage pour le chiffre de César

def read_file(file):
    """Lit le contenu d'un fichier et le retourne sous forme de chaîne de caractères."""
    content = file.read()
    return content

def cesar_encrypt(file, n):
    """Crypte le contenu du fichier en utilisant le chiffre de César avec un décalage de 'n'."""
    x = 0  # index pour parcourir les caractères
    result = ""  # chaîne de caractères résultante
    chars = list(file) # convertir la chaîne en liste de caractères pour modification
    for char in chars:
        if char in alphabet_lower:
            chars[x] = alphabet_lower[(alphabet_lower.index(char) + n) % len(alphabet_lower)] 
        elif char in alphabet_upper:
            chars[x] = alphabet_upper[(alphabet_upper.index(char) + n) % len(alphabet_upper)]
        elif char in string.digits:
            chars[x] = string.digits[(string.digits.index(char) + n) % 10]
        else:
            chars[x] = char
        x += 1
    return "".join(chars) # reconstituer la chaîne modifiée

def cesar_decrypt(file, n):
    """Décrypte le contenu du fichier chiffré avec le chiffre de César en utilisant un décalage de 'n'."""
    x = 0  # index pour parcourir les caractères
    result = ""  # chaîne de caractères résultante
    chars = list(file) # convertir la chaîne en liste de caractères pour modification
    for char in chars:
        if char in alphabet_lower:
            chars[x] = alphabet_lower[(alphabet_lower.index(char) - n) % len(alphabet_lower)] 
        elif char in alphabet_upper:
            chars[x] = alphabet_upper[(alphabet_upper.index(char) - n) % len(alphabet_upper)]
        elif char in string.digits:
            chars[x] = string.digits[(string.digits.index(char) - n) % 10]
        else:
            chars[x] = char
        x += 1
    return "".join(chars) # reconstituer la chaîne modifiée
    

def crypt_cesar():
    """Fonction principale pour exécuter le chiffrement de César."""
    file_input_text = open(INPUT_FILE_TEXT, "r", encoding="utf-8")
    content = read_file(file_input_text)

    file_output = open(os.path.join(BASE_DIR, "outputs", "cesar", "output_crypt_cesar.txt"), "w", encoding="utf-8")
    file_output.write(cesar_encrypt(content, n))

def decrypt_cesar():
    """Fonction principale pour exécuter le déchiffrement de César."""
    file_input_crypt = open(INPUT_FILE_CRYPT, "r", encoding="utf-8")
    content = read_file(file_input_crypt)

    file_output = open(os.path.join(BASE_DIR, "outputs", "cesar", "output_decrypt_cesar.txt"), "w", encoding="utf-8")
    file_output.write(cesar_decrypt(content, n))

def main():
    choise = input("Voulez-vous crypter ou décrypter le texte du fichier d'entrée ? (c/d) : ")
    if choise.lower() == 'c':
        crypt_cesar()
    elif choise.lower() == 'd':
        decrypt_cesar()
    else:
        print("Choix invalide. Veuillez entrer 'c' pour crypter ou 'd' pour décrypter.")

if __name__ == "__main__":
    main()