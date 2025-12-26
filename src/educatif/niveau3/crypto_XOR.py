import os

# Constantes pour les chemins des fichiers d'entrée et sortie
# Base project directory (repo root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
INPUT_TEXT_FILE = os.path.join(BASE_DIR, "inputs", "inputs_XOR", "input_text_XOR.txt")  # Fichier avec texte clair (représentation bytes)
INPUT_CRYPT_FILE = os.path.join(BASE_DIR, "inputs", "inputs_XOR", "input_crypt_XOR.txt")  # Fichier avec texte crypté (en hex)
CLE = "cleXOR"  # Clé de chiffrement XOR

# Fonction pour lire un fichier texte clair et le convertir en bytes
def read_plain_file(file_path):
    """Lit le contenu d'un fichier texte clair et retourne les bytes."""
    with open(file_path, 'r', encoding='utf-8') as f:  # Ouvre le fichier en mode lecture texte avec encodage UTF-8
        content = f.read()  # Lit tout le contenu du fichier
    return content.encode('utf-8')  # Encode le texte en bytes UTF-8

# Fonction pour lire un fichier crypté (en hex) et le convertir en bytes
def read_crypt_file(file_path):
    """Lit le contenu d'un fichier crypté (en hex) et retourne les bytes."""
    with open(file_path, 'r', encoding='utf-8') as f:  # Ouvre le fichier en mode lecture texte
        content = f.read().strip()  # Lit le contenu et enlève les espaces/blancs
    return bytes.fromhex(content)  # Convertit la string hex en bytes

# Fonction pour chiffrer un texte avec XOR
def crypt_xor(text, key):
    """Chiffre un texte avec XOR."""
    text_bytes = text.encode('utf-8')  # Convertit le texte en bytes
    key_bytes = key.encode('utf-8')  # Convertit la clé en bytes
    result = bytearray()  # Initialise un bytearray pour le résultat
    for i in range(len(text_bytes)):  # Boucle sur chaque byte du texte
        result.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])  # Applique XOR avec répétition de la clé
    return bytes(result)  # Retourne les bytes chiffrés

# Fonction pour déchiffrer des bytes avec XOR
def decrypt_xor(crypt_bytes, key):
    """Déchiffre des bytes avec XOR."""
    key_bytes = key.encode('utf-8')  # Convertit la clé en bytes
    result = bytearray()  # Initialise un bytearray pour le résultat
    for i in range(len(crypt_bytes)):  # Boucle sur chaque byte crypté
        result.append(crypt_bytes[i] ^ key_bytes[i % len(key_bytes)])  # Applique XOR inverse
    return bytes(result)  # Retourne les bytes déchiffrés

# Fonction principale pour chiffrer/déchiffrer avec affichage
def crypt_decrypt_XOR(texte_bytes, cle_bytes):
    """Chiffre ou déchiffre une chaîne de bytes en utilisant l'opération XOR avec la clé."""
    result = bytearray()  # Initialise le résultat
    for i in range(len(texte_bytes)):  # Boucle sur les bytes d'entrée
        byte_texte = texte_bytes[i]  # Byte actuel du texte
        byte_cle = cle_bytes[i % len(cle_bytes)]  # Byte correspondant de la clé (répétée)
        byte_chiffre = byte_texte ^ byte_cle  # Opération XOR
        result.append(byte_chiffre)  # Ajoute au résultat
    result_bytes = bytes(result)  # Convertit en bytes
    print(f"Résultat en bytes : {result_bytes}")  # Affiche le résultat
    return result_bytes  # Retourne les bytes

# Fonction principale du programme
def main():
    choice = input("Voulez-vous crypter ou décrypter le texte du fichier d'entrée ? (c/d) : ")  # Demande le choix utilisateur
    cle_bytes = CLE.encode('utf-8')  # Encode la clé en bytes
    
    if choice.lower() == 'c':  # Si choix 'c' pour crypter
        texte_bytes = read_plain_file(INPUT_TEXT_FILE)  # Lit le texte clair
        result_bytes = crypt_decrypt_XOR(texte_bytes, cle_bytes)  # Chiffre
        output_file = os.path.join(BASE_DIR, "outputs", "XOR", "output_XOR_crypt.txt")  # Fichier de sortie
        with open(output_file, 'wb') as f:  # Ouvre en écriture binaire
            f.write(result_bytes)  # Écrit les bytes
        print(f"Texte chiffré écrit dans {output_file}")  # Message de confirmation
    elif choice.lower() == 'd':  # Si choix 'd' pour décrypter
        texte_bytes = read_crypt_file(INPUT_CRYPT_FILE)  # Lit les bytes cryptés
        result_bytes = crypt_decrypt_XOR(texte_bytes, cle_bytes)  # Déchiffre
        output_file = os.path.join(BASE_DIR, "outputs", "XOR", "output_XOR_decrypt.txt")  # Fichier de sortie
        try:
            decrypted_text = result_bytes.decode('utf-8')  # Essaie de décoder en texte UTF-8
            with open(output_file, 'w', encoding='utf-8') as f:  # Ouvre en écriture texte
                f.write(decrypted_text)  # Écrit le texte
            print(f"Texte déchiffré écrit dans {output_file} (texte clair)")  # Confirmation
        except UnicodeDecodeError:  # Si décodage échoue
            print("Erreur : les bytes déchiffrés ne forment pas un texte UTF-8 valide. Écriture en bytes bruts.")  # Message d'erreur
            with open(output_file, 'wb') as f:  # Ouvre en binaire
                f.write(result_bytes)  # Écrit les bytes bruts
    else:  # Choix invalide
        print("Choix invalide. Veuillez entrer 'c' pour crypter ou 'd' pour décrypter.")  # Message d'erreur

# Point d'entrée du script
if __name__ == "__main__":
    main()  # Lance la fonction principale