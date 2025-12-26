# Rapport des codes — Projet Crypto-Python

Ce document présente un résumé « rapport » des principaux fichiers du projet.

## test_all.py
- **But**: Suite de tests manuelle qui vérifie les fonctions de chiffrement/déchiffrement de tous les modules du projet.
- **Structure**: Importe les fonctions depuis les modules et définit une fonction `test_*` par algorithme, puis une `main()` qui exécute tous les tests.
- **Fonctions clés**: `test_crypt_cesar`, `test_decrypt_cesar`, `test_crypt_vigenere`, `test_decrypt_vigenere`, `test_crypt_substi_mono`, `test_decrypt_substi_mono`, `test_crypt_transposition`, `test_decrypt_transposition`, `test_crypt_xor`, `test_decrypt_xor`, `test_crypt_AES_file`, `test_decrypt_AES_file`.
- **Détails techniques**:
  - Utilisation d’`assert` pour vérifier les sorties attendues et capture d’`AssertionError` pour afficher les résultats.
  - Tests XOR comparent des hex/bytes et reconstruisent des bytes via `bytes.fromhex`.
  - Tests AES créent/suppriment des fichiers temporaires et appellent `encrypt_file`/`decrypt_file`.

## niveau1/crypto_cesar.py
- **But**: Chiffrement et déchiffrement par décalage de César pour lettres ASCII (majuscules/minuscules) et pour chiffres.
- **Structure**: Fonctions `read_file`, `cesar_encrypt`, `cesar_decrypt`, helpers d’I/O `crypt_cesar`, `decrypt_cesar`, et `main`.
- **Détails techniques**:
  - Utilisation de `string.ascii_lowercase`, `string.ascii_uppercase` et `string.digits`.
  - Conversion en liste `chars = list(text)` pour modification, puis `return "".join(chars)`.
  - Rotation via `(index ± n) % len(...)` pour les lettres et `% 10` pour les chiffres.
- **Lignes plus techniques**:
  - Remplacement par index : `chars[x] = alphabet_lower[(alphabet_lower.index(char) + n) % len(alphabet_lower)]`.

## niveau1/crypto_vigenere.py
- **But**: Chiffrement et déchiffrement Vigenère en conservant la casse et en alignant la clé sur les lettres ASCII.
- **Structure**: `read_file`, `prepare_key`, conversions `convert_letter_to_number`/`convert_number_to_letter`, `crypt_vigenere`, `decrypt_vigenere`, `main`.
- **Détails techniques**:
  - `prepare_key` répète la clé `CLE` en positionnant la clé uniquement sur les lettres ASCII.
  - Conversion lettre↔indice via `ord(letter.upper()) - ord('A')`.
  - Chiffrement : `encrypted_index = (letter_index + key_index) % 26`.
  - Déchiffrement : `decrypted_index = (letter_index - key_index + 26) % 26`.
- **Lignes plus techniques**:
  - Préservation de la casse avec `input_file[i].isupper()` lors de la reconversion en lettre.

## niveau2/crypto_substi_mono.py
- **But**: Substitution monoalphabétique avec alphabets séparés pour majuscules et minuscules.
- **Structure**: Constantes `ALPHABET_MAJ`, `ALPHABET_MIN`, `CLE_MAJ`, `CLE_MIN`, puis `read_file`, `verify_key`, `crypt_substi_mono`, `decrypt_substi_mono`, `main`.
- **Détails techniques**:
  - `verify_key` vérifie que chaque clé est une permutation valide via `sorted(cle) == sorted(ALPHABET)`.
  - `crypt_substi_mono` remplace chaque lettre par la lettre correspondante dans la clé selon l’index trouvé dans l’alphabet source.
  - `decrypt_substi_mono` inverse la substitution en trouvant l’index dans la clé puis en récupérant la lettre d’origine.
- **Lignes plus techniques**:
  - Utilisation de `index()` pour déterminer la position des lettres et faire la correspondance.

## niveau2/crypto_transposition.py
- **But**: Chiffrement par transposition colonne/par-lignes avec padding de remplissage.
- **Structure**: `read_file`, `create_matrix`, `crypt_transposition`, `decrypt_transposition`, `main`.
- **Détails techniques**:
  - `create_matrix(text, key)` calcule `rows = math.ceil(len(text)/key)` et remplit la matrice ligne par ligne, remplissant les cellules manquantes avec le caractère `'¤'`.
  - `crypt_transposition` lit la matrice colonne par colonne pour produire le texte chiffré.
  - `decrypt_transposition` reconstruit la matrice en remplissant colonne par colonne, relit ligne par ligne, puis retire le padding via `.replace('¤', '')`.
- **Lignes plus techniques**:
  - Calcul d’index dans `create_matrix`: `index = i * key + j` pour positionner chaque caractère.

## niveau3/crypto_XOR.py
- **But**: Chiffrement/déchiffrement par XOR octet-à-octet avec clé répétée.
- **Structure**: `read_plain_file`, `read_crypt_file`, `crypt_xor`, `decrypt_xor`, `crypt_decrypt_XOR`, `main`.
- **Détails techniques**:
  - `read_plain_file` retourne `content.encode('utf-8')`.
  - `read_crypt_file` convertit une chaîne hex en `bytes` via `bytes.fromhex`.
  - `crypt_xor`/`decrypt_xor`: conversion en bytes puis boucle `result.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])`.
  - `crypt_decrypt_XOR` applique l’opération sur des `bytes` et retourne les `bytes`.
- **Lignes plus techniques**:
  - Répétition de la clé via `i % len(key_bytes)` dans la boucle d’XOR.
  - Gestion du décodage UTF‑8 en sortie avec tentative de `.decode('utf-8')` et prise en charge des cas binaires.

---

Ce rapport est fourni pour être inclus dans le dossier final du projet.
