import sys
import os

# Ensure old-style imports like `niveau1.*` work when source moved under `src/educatif`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "educatif"))

from niveau1.crypto_cesar import cesar_encrypt, cesar_decrypt
from niveau1.crypto_vigenere import crypt_vigenere, decrypt_vigenere
from niveau2.crypto_substi_mono import crypt_substi_mono, decrypt_substi_mono, CLE_MAJ, CLE_MIN, verify_key
from niveau2.crypto_transposition import crypt_transposition, decrypt_transposition
from niveau3.crypto_XOR import crypt_xor, decrypt_xor
from niveau3.crypto_AES import encrypt_file, decrypt_file, MASTER_KEY

"""
Tests AES fichier - explication

 test_crypt_AES_file:
 - crée un petit fichier binaire d'entrée `test_aes_input.bin` contenant
   b'Hello AES file\n'.
 - appelle `encrypt_file(input_path, encrypted_path, MASTER_KEY, output_format='bin')`.
   `encrypt_file` lit les octets, les convertit en bits, applique un padding
   PKCS#7-like (au niveau octet), découpe en blocs, applique les rounds
   (AddRoundKey -> SubBytes -> ShiftRows -> MixColumns) et écrit le résultat
   chiffré en binaire (ou en hex si `output_format='hex'`).
 - vérifie que le fichier chiffré n'est pas identique au fichier clair (sanity).
 - supprime les fichiers temporaires créés dans un bloc `finally`.

 test_decrypt_AES_file:
 - prépare les chemins `test_aes_input.bin`, `test_aes_encrypted.bin`,
   `test_aes_decrypted.bin` et crée les fichiers manquants si le test est
   exécuté isolément (idempotence).
 - appelle `decrypt_file(encrypted_path, decrypted_path, MASTER_KEY, input_format='bin')`.
   `decrypt_file` lit les octets (ou la chaîne hex), reconvertit en bits puis
   appelle `decrypt_bits_to_bytes` qui inverse les rounds dans l'ordre
   (inverse_mix_columns, inverse_shift_rows, inverse_sub_bytes, AddRoundKey),
   reconstruit les octets puis retire le padding PKCS#7-like pour restituer
   exactement les octets originaux.
 - compare le contenu déchiffré avec les octets attendus puis nettoie les
   fichiers temporaires dans `finally`.

 Points techniques importants:
 - Padding: PKCS#7-like ajouté avant chiffrement (au niveau octet). Après
   déchiffrement, on retire le padding en vérifiant la valeur du dernier octet.
 - Réversibilité: `mix_columns` a été implémenté comme opération simple
   réversible (XOR constant + rotation) et `inverse_mix_columns` fournit
   l'opération inverse pour garantir `decrypt(encrypt(...))`.
 - Formats: `encrypt_file` peut écrire `bin` (octets) ou `hex` (chaîne hex).
   `decrypt_file` accepte `input_format='bin'` ou `'hex'`.
 - Clé: les tests utilisent `MASTER_KEY` importé depuis
   `niveau3/crypto_AES.py`.
"""

def test_crypt_cesar():
    try:
        assert cesar_encrypt("ABC XYZ abc xyz", 3) == "DEF ABC def abc"
        assert cesar_encrypt("Hello, World!", 5) == "Mjqqt, Btwqi!"
        assert cesar_encrypt("Python 3.8", 10) == "Zidryx 3.8"
        print("✅ César crypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au chiffrement césar: {e}")


def test_decrypt_cesar():
    try:
        assert cesar_decrypt("DEF ABC def abc", 3) == "ABC XYZ abc xyz"
        assert cesar_decrypt("Mjqqt, Btwqi!", 5) == "Hello, World!"
        assert cesar_decrypt("Zidryx 3.8", 10) == "Python 3.8"
        print("✅ César decrypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au déchiffrement césar: {e}")
    

def test_crypt_vigenere():
    try:
        assert crypt_vigenere("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
        assert crypt_vigenere("Hello, World!", "KEY") == "Rijvs, Uyvjn!"
        assert crypt_vigenere("Python 3.8", "CODE") == "Rmwlqb 3.8"
        print("✅ Vigenère crypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au chiffrement vigenère: {e}")


def test_decrypt_vigenere():
    try:
        assert decrypt_vigenere("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
        assert decrypt_vigenere("Rijvs, Uyvjn!", "KEY") == "Hello, World!"
        assert decrypt_vigenere("Rmwlqb 3.8", "CODE") == "Python 3.8"
        print("✅ Vigenère decrypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au déchiffrement vigenère: {e}")
    
def test_crypt_substi_mono():
    try:
        verify_key(CLE_MAJ, CLE_MIN)
        assert crypt_substi_mono("BoNjOuR", CLE_MAJ, CLE_MIN) == "SwJpWqA"
        assert crypt_substi_mono("Test 123, crypto #2025 !", CLE_MAJ, CLE_MIN) == "Muem 123, kaznmw #2025 !"
        assert crypt_substi_mono("La cryptographie est fascinante, surtout quand on comprend comment fonctionnent les algorithmes!", CLE_MAJ, CLE_MIN) == "Cf kaznmwyafnixu uem tfekxjfjmu, eqamwqm gqfjr wj kwdnaujr kwddujm twjkmxwjjujm cue fcywaxmidue!"
        print("✅ Substitution mono crypt OK")
    except AssertionError as e:
        print("Le test a échoué au chiffrement par substitution mono.")

def test_decrypt_substi_mono():
    try:
        verify_key(CLE_MAJ, CLE_MIN)
        assert decrypt_substi_mono("SwJpWqA", CLE_MAJ, CLE_MIN) == "BoNjOuR"
        assert decrypt_substi_mono("Muem 123, kaznmw #2025 !", CLE_MAJ, CLE_MIN) == "Test 123, crypto #2025 !"
        assert decrypt_substi_mono("Cf kaznmwyafnixu uem tfekxjfjmu, eqamwqm gqfjr wj kwdnaujr kwddujm twjkmxwjjujm cue fcywaxmidue!", CLE_MAJ, CLE_MIN) == "La cryptographie est fascinante, surtout quand on comprend comment fonctionnent les algorithmes!"
        print("✅ Substitution mono decrypt OK")
    except AssertionError as e:
        print("Le test a échoué au déchiffrement par substitution mono.")

def test_crypt_transposition():
    try:
        assert crypt_transposition("HELLO WORLD", 4) == "HORE LLWDLO¤"
        assert crypt_transposition("CRYPTOGRAPHY IS FUN", 5) == "COH RGYFYR UPAINTPS¤"
        assert crypt_transposition("TESTING TRANSPOSITION CIPHER", 6) == "TGSIPE POHSTONETRS RIAIC¤NNTI¤"
        print("✅ Transposition crypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au chiffrement par transposition: {e}")

def test_decrypt_transposition():
    try:
        assert decrypt_transposition("HORE LLWDLO¤", 4) == "HELLO WORLD"
        assert decrypt_transposition("COH RGYFYR UPAINTPS¤", 5) == "CRYPTOGRAPHY IS FUN"
        assert decrypt_transposition("TGSIPE POHSTONETRS RIAIC¤NNTI¤", 6) == "TESTING TRANSPOSITION CIPHER"
        print("✅ Transposition decrypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au déchiffrement par transposition: {e}")

def test_crypt_xor():
    try:
        # Test avec le texte connu
        text = "ceci est un joli test"
        key = "cleXOR"
        crypted = crypt_xor(text, key)
        expected_hex = "000906316f371018452d2172090309316f26061f11"
        assert crypted.hex() == expected_hex
        print("✅ XOR crypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au chiffrement XOR: {e}")

def test_decrypt_xor():
    try:
        # Test avec les bytes cryptés
        crypt_hex = "000906316f371018452d2172090309316f26061f11"
        crypt_bytes = bytes.fromhex(crypt_hex)
        key = "cleXOR"
        decrypted = decrypt_xor(crypt_bytes, key)
        expected_text = "ceci est un joli test"
        assert decrypted.decode('utf-8') == expected_text
        print("✅ XOR decrypt OK")
    except AssertionError as e:
        print(f"Le test a échoué au déchiffrement XOR: {e}")


def test_crypt_AES_file():
    try:
        # create a small binary input file
        input_path = 'test_aes_input.bin'
        encrypted_path = 'test_aes_encrypted.bin'
        decrypted_path = 'test_aes_decrypted.bin'
        data = b'Hello AES file\n'
        with open(input_path, 'wb') as f:
            f.write(data)

        encrypt_file(input_path, encrypted_path, MASTER_KEY, output_format='bin')
        # ensure encrypted file exists and is not identical to input
        with open(encrypted_path, 'rb') as f:
            enc = f.read()
        assert enc != data
        print('✅ AES file encrypt OK')
    except AssertionError as e:
        print(f'Le test a échoué au chiffrement fichier AES: {e}')
    finally:
        # clean files 
        for p in (input_path, encrypted_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass


def test_decrypt_AES_file():
    try:
        input_path = 'test_aes_input.bin'
        encrypted_path = 'test_aes_encrypted.bin'
        decrypted_path = 'test_aes_decrypted.bin'
        # create input and encrypted if missing (in case tests run independently)
        if not os.path.exists(input_path):
            with open(input_path, 'wb') as f:
                f.write(b'Hello AES file\n')
        if not os.path.exists(encrypted_path):
            encrypt_file(input_path, encrypted_path, MASTER_KEY, output_format='bin')
        # decrypt back
        decrypt_file(encrypted_path, decrypted_path, MASTER_KEY, input_format='bin')
        with open(decrypted_path, 'rb') as f:
            dec = f.read()
        expected = b'Hello AES file\n'
        assert dec == expected
        print('✅ AES file decrypt OK')
    except AssertionError as e:
        print(f'Le test a échoué au déchiffrement fichier AES: {e}')
    finally:
        for p in (input_path, encrypted_path, decrypted_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

def main():
    print("=== Tests césar ===")
    test_crypt_cesar()
    test_decrypt_cesar()
    print("\n")

    print("=== Tests vigenère ===")
    test_crypt_vigenere()
    test_decrypt_vigenere()
    print("\n")

    print("=== Tests substitution monoalphabétique ===")
    test_crypt_substi_mono()
    test_decrypt_substi_mono()
    print("\n")

    print("=== Tests transposition ===")
    test_crypt_transposition()
    test_decrypt_transposition()
    print("\n")

    print("=== Tests XOR ===")
    test_crypt_xor()
    test_decrypt_xor()
    print("\n")

    print("=== Tests AES fichier ===")
    test_crypt_AES_file()   
    test_decrypt_AES_file()
    print("\n")

    print("🎉 Tous les tests ont été exécutés !")

if __name__ == "__main__":
    main()