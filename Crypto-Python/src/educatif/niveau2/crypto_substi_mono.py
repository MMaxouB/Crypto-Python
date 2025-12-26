import os

# Chemins par défaut vers les fichiers d'entrée (texte clair et chiffré)
# Base project directory (repo root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
INPUT_FILE_TEXT = os.path.join(BASE_DIR, "inputs", "inputs_substi_mono", "input_text_substi_mono.txt") # fichier d'entrée en texte clair
INPUT_FILE_CRYPT = os.path.join(BASE_DIR, "inputs", "inputs_substi_mono", "input_crypt_substi_mono.txt") # fichier d'entrée chiffré

# Alphabets de référence (majuscules puis minuscules)
ALPHABET_MAJ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_MIN = "abcdefghijklmnopqrstuvwxyz"

# Clés de substitution (alphabet permutation pour majuscules et minuscules)
CLE_MAJ = "FSKRUTYIXPLCDJWNGAEMQHOBZV"
CLE_MIN = "fskrutyixplcdjwngaemqhobzv"

def read_file(file_path):
    """Lit le contenu d'un fichier et le retourne en tant que chaîne de caractères."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content



def verify_key(cle_maj, cle_min):
    """Vérifie que les clés de substitution sont valides."""
    # On vérifie : longueur 26 et chaque lettre présente exactement une fois
    if (len(cle_maj) != 26 or len(cle_min) != 26 or sorted(cle_maj) != sorted(ALPHABET_MAJ) or sorted(cle_min) != sorted(ALPHABET_MIN)):
        raise ValueError("Clé de substitution invalide. Elle doit contenir chaque lettre de l'alphabet exactement une fois.")

def crypt_substi_mono(input_file, cle_maj, cle_min):
    result = ""
    # Parcours chaque caractère du texte d'entrée
    for char in input_file:
        # Si c'est une majuscule, remplacer par la lettre correspondante dans `cle_maj`
        if char in ALPHABET_MAJ:
            index = ALPHABET_MAJ.index(char)
            result += cle_maj[index]
        # Si c'est une minuscule, remplacer par la lettre correspondante dans `cle_min`
        elif char in ALPHABET_MIN:
            index = ALPHABET_MIN.index(char)
            result += cle_min[index]
        else:
            # Ne pas modifier les chiffres, ponctuation et espaces
            result += char  # Ne pas modifier les caractères non alphabétiques
    return result


def decrypt_substi_mono(input_file, cle_maj, cle_min):
    result = ""
    # Parcours chaque caractère du texte chiffré et inverse la substitution
    for char in input_file:
        # Si le caractère appartient à la clé majuscule, trouver son index et récupérer la lettre originale
        if char in cle_maj:
            index = cle_maj.index(char)
            result += ALPHABET_MAJ[index]
        # Même logique pour les minuscules
        elif char in cle_min:
            index = cle_min.index(char)
            result += ALPHABET_MIN[index]
        else:
            # Conserver chiffres, ponctuation et espaces inchangés
            result += char  # Ne pas modifier les caractères non alphabétiques
    return result


def main():
    verify_key(CLE_MAJ, CLE_MIN)
    choice = input("Voulez-vous crypter ou décrypter le texte du fichier d'entrée ? (c/d) : ")
    if choice.lower() == 'c':
        input_text = read_file(INPUT_FILE_TEXT)
        encrypted_text = crypt_substi_mono(input_text, CLE_MAJ, CLE_MIN)
        with open(os.path.join(BASE_DIR, "outputs", "substi_mono", "output_crypt_substi_mono.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(encrypted_text)
            file_output.write("\n" + "avec l'alphabet : " + CLE_MAJ + "\n")
    elif choice.lower() == 'd':
        input_crypt = read_file(INPUT_FILE_CRYPT)
        decrypted_text = decrypt_substi_mono(input_crypt, CLE_MAJ, CLE_MIN)
        with open(os.path.join(BASE_DIR, "outputs", "substi_mono", "output_decrypt_substi_mono.txt"), "w", encoding="utf-8") as file_output:
            file_output.write(decrypted_text)
            file_output.write("\n" + "avec l'alphabet : " + CLE_MAJ + "\n")
    else:
        print("Choix invalide. Veuillez entrer 'c' pour crypter ou 'd' pour décrypter.")
        main()


if __name__ == "__main__":
    main()