import string
import os

# Base project directory (repo root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

INPUT_FILE_TEXT = os.path.join(BASE_DIR, "inputs", "inputs_vigenere", "input_text_vigenere.txt") # fichier d'entrée en texte clair
INPUT_FILE_CRYPT = os.path.join(BASE_DIR, "inputs", "inputs_vigenere", "input_crypt_vigenere.txt") # fichier d'entrée chiffré

"""CLE = input("Entrez la clé de chiffrement/déchiffrement : ")"""
CLE = "MAIS"  # clé de chiffrement/déchiffrement prédéfinie

def read_file(file_path):
    """Lit le contenu d'un fichier et le retourne sous forme de chaîne de caractères."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def prepare_key(input_file, CLE):
    """Prépare la clé en la répétant pour les caractères non-espace/non-nouvelle-ligne, en préservant les espaces et nouvelles lignes."""
    key = ""
    key_index = 0
    for char in input_file:
        # Ne répéter la clé que pour les lettres ASCII ; préserver tout caractère non alphabétique ou accentué
        if char not in string.ascii_letters:
            key += char
        else:
            key += CLE[key_index % len(CLE)]
            key_index += 1
    return key

def convert_letter_to_number(letter):
    """Convertit une lettre en son index numérique (A=0, B=1, ..., Z=25)."""
    if letter not in string.ascii_letters:
        raise ValueError(f"convert_letter_to_number attendu une lettre ASCII A-Z/a-z, reçu: {letter!r}")
    valeur = ord(letter.upper()) - ord('A')
    return valeur

def convert_number_to_letter(number, is_upper):
    """Convertit un index numérique en lettre correspondante."""
    if is_upper:
        letter = chr(number + ord('A'))
    else:
        letter = chr(number + ord('a'))
    return letter

def crypt_vigenere(input_file, CLE):
    key = prepare_key(input_file, CLE)
    result = ""
    for i in range(len(input_file)):
        # Ne chiffrer que les lettres ASCII ; laisser chiffres, accents et caractères spéciaux inchangés
        if input_file[i] not in string.ascii_letters:
            result += input_file[i]
        else:
            letter_index = convert_letter_to_number(input_file[i])
            key_index = convert_letter_to_number(key[i])
            encrypted_index = (letter_index + key_index) % 26
            result += convert_number_to_letter(encrypted_index, input_file[i].isupper())
    return result

def decrypt_vigenere(input_file, CLE):
    key = prepare_key(input_file, CLE)
    result = ""
    for i in range(len(input_file)):
        # Ne déchiffrer que les lettres ASCII ; laisser chiffres, accents et caractères spéciaux inchangés
        if input_file[i] not in string.ascii_letters:
            result += input_file[i]
        else:
            letter_index = convert_letter_to_number(input_file[i])
            key_index = convert_letter_to_number(key[i])
            decrypted_index = (letter_index - key_index + 26) % 26
            result += convert_number_to_letter(decrypted_index, input_file[i].isupper())
    return result

def main():
    choice = input("Voulez-vous crypter ou décrypter le texte du fichier d'entrée ? (c/d) : ")
    if choice.lower() == 'c':
        input_text = read_file(INPUT_FILE_TEXT)
        encrypted_text = crypt_vigenere(input_text, CLE)
        with open(os.path.join(BASE_DIR, "outputs", "vigenere", "output_crypt_vigenere.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(encrypted_text)
            file_output.write("\n" + "avec la clé : " + CLE + "\n")
    elif choice.lower() == 'd':
        input_crypt = read_file(INPUT_FILE_CRYPT)
        decrypted_text = decrypt_vigenere(input_crypt, CLE)
        with open(os.path.join(BASE_DIR, "outputs", "vigenere", "output_decrypt_vigenere.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(decrypted_text)
            file_output.write("\n" + "avec la clé : " + CLE + "\n")
    else:
        print("Choix invalide. Veuillez entrer 'c' pour crypter ou 'd' pour décrypter.")

if __name__ == "__main__":
    main()