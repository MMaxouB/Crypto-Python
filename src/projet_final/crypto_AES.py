# 1️⃣ Paramètres de base
BLOCK_SIZE = 16
KEY_SIZE = 16
ROUNDS = 4
MASTER_KEY = 0b1010110011001010

import os
# Base project directory (repo root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# default input/output files (absolute, from repo root)
INPUT_FILE_TEXT = os.path.join(BASE_DIR, "inputs", "inputs_AES", "input_text_AES.txt")
INPUT_FILE_CRYPT = os.path.join(BASE_DIR, "inputs", "inputs_AES", "input_crypt_AES.txt")
OUTPUT_FILE_CRYPT = os.path.join(BASE_DIR, "outputs", "AES", "output_crypt_AES.txt")
OUTPUT_FILE_DECRYPT = os.path.join(BASE_DIR, "outputs", "AES", "output_decrypt_AES.txt")

def read_file(file_path):
    """Lit le contenu d'un fichier et le retourne en tant que chaîne de caractères."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# 2️⃣ Fonctions utilitaires
def text_to_bits(text):
    # Convertit texte → liste de bits
    bits = []
    for char in text:
        bin_char = format(ord(char), '08b')
        bits.extend(int(b) for b in bin_char)
    return bits

def bits_to_text(bits):
    # Convertit liste de bits → texte
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        char = chr(int(''.join(str(b) for b in byte), 2))
        chars.append(char)
    return ''.join(chars)

def split_blocks(bits, block_size=BLOCK_SIZE):
    # Découpe bits en blocs de block_size, avec padding si nécessaire
    blocks = []
    for i in range(0, len(bits), block_size):
        block = bits[i:i+block_size]
        if len(block) < block_size:
            block += [0] * (block_size - len(block))  # Padding avec des zéros
        blocks.append(block)
    return blocks


def pad_bits_pkcs7(bits, block_size=BLOCK_SIZE):
    # PKCS#7-like padding at byte granularity for block_size (bits)
    if len(bits) % 8 != 0:
        raise ValueError('pad_bits_pkcs7 expects bit length multiple of 8')
    bytes_per_block = block_size // 8
    total_bytes = len(bits) // 8
    rem = total_bytes % bytes_per_block
    if rem == 0:
        pad_bytes = bytes_per_block
    else:
        pad_bytes = bytes_per_block - rem
    pad_val = pad_bytes & 0xFF
    pad_bits = []
    for _ in range(pad_bytes):
        pad_bits.extend([int(b) for b in f"{pad_val:08b}"])
    return bits + pad_bits


def bits_to_hex(bits):
    # Convertit une liste de bits en chaîne hexadécimale
    if not bits:
        return ''
    # Pad to full bytes
    if len(bits) % 8 != 0:
        bits = bits + [0] * (8 - (len(bits) % 8))
    hex_bytes = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        val = int(''.join(str(b) for b in byte), 2)
        hex_bytes.append(f"{val:02x}")
    return ''.join(hex_bytes)


def bytes_to_bits(b: bytes) -> list:
    bits = []
    for byte in b:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
    return bits


def bits_to_bytes(bits: list) -> bytes:
    if len(bits) % 8 != 0:
        bits = bits + [0] * (8 - (len(bits) % 8))
    ba = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        val = int(''.join(str(b) for b in byte), 2)
        ba.append(val)
    return bytes(ba)


def hex_to_bits(hexstr: str) -> list:
    return bytes_to_bits(bytes.fromhex(hexstr))

# 3️⃣ Key schedule
def rotl(x: int, n: int, bits: int = 16) -> int:
    """
    Rotation gauche de n bits sur une taille donnée.
    """
    mask = (1 << bits) - 1
    return ((x << n) & mask) | (x >> (bits - n))


def generate_round_keys(master_key: int, rounds: int, key_size: int = 16) -> list:
    """
    Génère les sous-clés à partir d'une clé maître.
    
    master_key : clé maître en entier (ex: 16 bits)
    rounds     : nombre de rounds
    key_size   : taille de la clé en bits (par défaut 16)
    
    Étapes :
    - rotation gauche de 3 bits
    - XOR avec motif fixe (0b1010101010101010)
    - conversion en liste de bits
    """
    round_keys = []
    motif = 0b1010101010101010  # motif fixe

    current_key = master_key
    for r in range(rounds):
        # rotation gauche de 3 bits
        current_key = rotl(current_key, 3, key_size)
        # XOR avec motif
        current_key ^= motif
        # conversion en liste de bits
        bits_list = [(current_key >> i) & 1 for i in reversed(range(key_size))]
        round_keys.append(bits_list)

    return round_keys


# 4️⃣ AddRoundKey
def add_round_key(block, round_key):
    """
    XOR bit à bit du bloc avec la sous-clé.
    
    block     : liste de bits (ex: [0,1,1,0,...])
    round_key : liste de bits de même taille
    
    Retourne  : nouvelle liste de bits après XOR

    Description de l'opération :
    # zip → [(1,0), (0,1), (1,0), (1,1)]
    # XOR → [1^0, 0^1, 1^0, 1^1] → [1,1,1,0]

    """
    if len(block) != len(round_key):
        raise ValueError("Le bloc et la sous-clé doivent avoir la même taille.")
    
    return [b ^ k for b, k in zip(block, round_key)]


# 5️⃣ SubBytes
S_BOX = {
    # Table S-box simplifiée pour 4 bits
    0: 14,  # 0000 -> 1110
    1: 4,   # 0001 -> 0100
    2: 13,  # 0010 -> 1101
    3: 1,   # 0011 -> 0001
    4: 2,   # 0100 -> 0010
    5: 15,  # 0101 -> 1111
    6: 11,  # 0110 -> 1011
    7: 8,   # 0111 -> 1000
    8: 3,   # 1000 -> 0011
    9: 10,  # 1001 -> 1010
    10: 6,  # 1010 -> 0110
    11: 12, # 1011 -> 1100
    12: 5,  # 1100 -> 0101
    13: 9,  # 1101 -> 1001
    14: 0,  # 1110 -> 0000
    15: 7   # 1111 -> 0111
}

def sub_bytes(block):
    # Substitution nibble par nibble
    new_block = []
    for i in range(0, len(block), 4):
        nibble_bits = block[i:i+4]
        nibble_val = int("".join(map(str, nibble_bits)), 2)
        sub_val = S_BOX[nibble_val]
        sub_bits = [int(b) for b in f"{sub_val:04b}"]
        new_block.extend(sub_bits)

    return new_block


# 6️⃣ ShiftRows
def shift_rows(block: list[int]) -> list[int]:
    # Décalage des lignes du bloc pour diffusion
    row1 = block[:8]
    row2 = block[8:]

    row2_shifted = row2[1:] + row2[:1]  # Décalage circulaire à gauche de 1
    new_block = row1 + row2_shifted
    return new_block

# 7️⃣ MixColumns
def mix_columns(block):
    # Diffusion très simple et parfaitement inversible :
    # - découpe en nibbles (4 bits)
    # - XOR chaque nibble avec une constante (0xA)
    # - rotation circulaire des nibbles vers la gauche
    if not block:
        return []

    if len(block) % 4 != 0:
        pad_len = 4 - (len(block) % 4)
        block = block + [0] * pad_len

    nibbles = []
    for i in range(0, len(block), 4):
        nib = block[i:i+4]
        val = int(''.join(str(b) for b in nib), 2) & 0xF
        nibbles.append(val)

    # XOR with constant
    xored = [ (n ^ 0xA) & 0xF for n in nibbles ]
    # rotate left by 1 nibble
    if len(xored) > 1:
        xored = xored[1:] + xored[:1]

    new_block = []
    for v in xored:
        bits = [int(b) for b in f"{v:04b}"]
        new_block.extend(bits)
    return new_block

# 8️⃣ Round complet
def round(block, round_key, last_round=False):
    # Un round complet : AddRoundKey → SubBytes → ShiftRows → MixColumns (sauf dernier)
    add_round_keyed = add_round_key(block, round_key)
    subbed = sub_bytes(add_round_keyed)
    shifted = shift_rows(subbed)
    if not last_round:
        mixed = mix_columns(shifted)
        return mixed
    else:
        return shifted

# 9️⃣ Chiffrement complet
def encrypt(bits, master_key, rounds=ROUNDS):
    # Découpe en blocs
    # Génération sous-clés
    # Applique rounds sur chaque bloc
    # Concatène les blocs chiffrés
    # apply PKCS7-like padding (expects bits length multiple of 8)
    if len(bits) % 8 != 0:
        raise ValueError('encrypt expects bits length multiple of 8')
    bits_padded = pad_bits_pkcs7(bits, BLOCK_SIZE)
    blocks = split_blocks(bits_padded, BLOCK_SIZE)
    round_keys = generate_round_keys(master_key, rounds, KEY_SIZE)
    for i in range(len(blocks)):
        block = blocks[i]
        for r in range(rounds):
            last_round = (r == rounds - 1)
            block = round(block, round_keys[r], last_round)
        blocks[i] = block
    # Concaténation des blocs chiffrés
    encrypted_bits = []
    for block in blocks:
        encrypted_bits.extend(block)
    
    return encrypted_bits


def decrypt_bits_to_bytes(bits_encrypted, master_key, rounds=ROUNDS):
    # Similar to decrypt but returns raw bytes (no text decoding)
    blocks = split_blocks(bits_encrypted, BLOCK_SIZE)
    round_keys = generate_round_keys(master_key, rounds, KEY_SIZE)
    for i in range(len(blocks)):
        block = blocks[i]
        for r in range(rounds - 1, -1, -1):
            if r != rounds - 1:
                block = inverse_mix_columns(block)
            block = inverse_shift_rows(block)
            block = inverse_sub_bytes(block)
            block = add_round_key(block, round_keys[r])
        blocks[i] = block

    decrypted_bits = []
    for block in blocks:
        decrypted_bits.extend(block)

    # Ensure full bytes
    if len(decrypted_bits) % 8 != 0:
        decrypted_bits = decrypted_bits[:len(decrypted_bits) - (len(decrypted_bits) % 8)]
    data = bits_to_bytes(decrypted_bits)
    # remove PKCS7-like padding (byte-wise)
    if len(data) == 0:
        return data
    pad_val = data[-1]
    bytes_per_block = BLOCK_SIZE // 8
    if 1 <= pad_val <= bytes_per_block and all(b == pad_val for b in data[-pad_val:]):
        return data[:-pad_val]
    return data


def encrypt_file(input_path: str, output_path: str, master_key: int, output_format: str = 'bin'):
    # Read input as binary, encrypt, write either binary or hex
    with open(input_path, 'rb') as f:
        data = f.read()
    bits = bytes_to_bits(data)
    encrypted_bits = encrypt(bits, master_key)
    if output_format == 'hex':
        with open(output_path, 'w', encoding='utf-8') as fo:
            fo.write(bits_to_hex(encrypted_bits))
    else:
        with open(output_path, 'wb') as fo:
            fo.write(bits_to_bytes(encrypted_bits))


def decrypt_file(input_path: str, output_path: str, master_key: int, input_format: str = 'bin'):
    # Read encrypted input (bin or hex), decrypt and write raw bytes
    if input_format == 'hex':
        with open(input_path, 'r', encoding='utf-8') as f:
            hexstr = f.read().strip()
        bits = hex_to_bits(hexstr)
    else:
        with open(input_path, 'rb') as f:
            data = f.read()
        bits = bytes_to_bits(data)

    decrypted_bytes = decrypt_bits_to_bytes(bits, master_key)
    with open(output_path, 'wb') as fo:
        fo.write(decrypted_bytes)


# ---- Fonctions d'inversion pour le déchiffrement ----
INVERSE_S_BOX = {v: k for k, v in S_BOX.items()}

def inverse_sub_bytes(block):
    # Inverse de sub_bytes (nibble par nibble)
    new_block = []
    for i in range(0, len(block), 4):
        nibble_bits = block[i:i+4]
        nibble_val = int("".join(map(str, nibble_bits)), 2)
        orig_val = INVERSE_S_BOX.get(nibble_val, 0)
        orig_bits = [int(b) for b in f"{orig_val:04b}"]
        new_block.extend(orig_bits)
    return new_block


def inverse_shift_rows(block: list[int]) -> list[int]:
    # Inverse du shift_rows: rotation droite de la seconde ligne
    row1 = block[:8]
    row2 = block[8:]
    row2_unshifted = row2[-1:] + row2[:-1]
    return row1 + row2_unshifted


def inverse_mix_columns(block):
    # Inverse of the simple mix_columns above:
    # - reconstruct nibbles
    # - rotate right by 1 nibble
    # - XOR with the same constant (0xA) to recover original
    if not block:
        return []

    if len(block) % 4 != 0:
        pad_len = 4 - (len(block) % 4)
        block = block + [0] * pad_len

    final_nibbles = []
    for i in range(0, len(block), 4):
        nib = block[i:i+4]
        val = int(''.join(str(b) for b in nib), 2) & 0xF
        final_nibbles.append(val)

    if len(final_nibbles) > 1:
        y = final_nibbles[-1:] + final_nibbles[:-1]
    else:
        y = final_nibbles[:]

    orig = [ (v ^ 0xA) & 0xF for v in y ]

    new_block = []
    for val in orig:
        bits = [int(b) for b in f"{val:04b}"]
        new_block.extend(bits)
    return new_block


def decrypt(bits_encrypted, master_key, rounds=ROUNDS):
    # Découpe en blocs
    blocks = split_blocks(bits_encrypted, BLOCK_SIZE)
    # Génération des sous-clés (même order; on utilisera index direct)
    round_keys = generate_round_keys(master_key, rounds, KEY_SIZE)

    for i in range(len(blocks)):
        block = blocks[i]
        # Parcourir les rounds depuis le dernier vers le premier
        for r in range(rounds - 1, -1, -1):
            # si ce n'est pas le premier round de la boucle (c.-à-d. pas le round final
            # d'encryption), on applique d'abord l'inverse de MixColumns
            if r != rounds - 1:
                block = inverse_mix_columns(block)
            # inverse ShiftRows
            block = inverse_shift_rows(block)
            # inverse SubBytes
            block = inverse_sub_bytes(block)
            # AddRoundKey (même opération)
            block = add_round_key(block, round_keys[r])

        blocks[i] = block

    # Réutiliser la version qui retourne des bytes, puis décoder en texte
    decrypted_bytes = decrypt_bits_to_bytes(bits_encrypted, master_key, rounds)
    try:
        return decrypted_bytes.decode('utf-8')
    except Exception:
        # si décodage échoue, retourner représentation avec replacement
        return decrypted_bytes.decode('utf-8', errors='replace')

# 🔟 Utilisation
def main():
    # Interactive helper to encrypt/decrypt files.
    # Usage (interactive):
    # - Choisissez '1' pour chiffrer un fichier : fournissez le chemin entrée, le chemin sortie,
    #   et le format de sortie ('bin' ou 'hex').
    # - Choisissez '2' pour déchiffrer un fichier : fournissez le chemin entrée (bin ou hex),
    #   le chemin sortie, et le format d'entrée ('bin' ou 'hex').
    # - Tapez 'q' pour quitter.
    print('AES simple — chiffrement/déchiffrement de fichiers (interactive)')
    while True:
        print('\nActions:')
        print('  1) Encrypt file')
        print('  2) Decrypt file')
        print("  q) Quit")
        choice = input('Votre choix: ').strip().lower()
        if choice in ('q', 'quit', 'exit'):
            print('Au revoir.')
            break
        if choice == '1':
            # Use predefined constants for input/output
            try:
                # ensure output dirs exist
                os.makedirs(os.path.dirname(OUTPUT_FILE_CRYPT), exist_ok=True)
                # write hex text file only
                encrypt_file(INPUT_FILE_TEXT, OUTPUT_FILE_CRYPT, MASTER_KEY, output_format='hex')
                print(f'Fichier chiffré écrit : {OUTPUT_FILE_CRYPT} (hex)')
            except Exception as e:
                print('Erreur lors du chiffrement :', e)
        elif choice == '2':
            # Use predefined constants for input/output. Prefer INPUT_FILE_CRYPT if it exists.
            fmt = 'hex'
            in_path = INPUT_FILE_CRYPT if __import__('os').path.exists(INPUT_FILE_CRYPT) else OUTPUT_FILE_CRYPT
            try:
                decrypt_file(in_path, OUTPUT_FILE_DECRYPT, MASTER_KEY, input_format=fmt)
                print(f'Fichier déchiffré écrit dans: {OUTPUT_FILE_DECRYPT} (input: {in_path}, format: {fmt})')
            except Exception as e:
                print('Erreur lors du déchiffrement :', e)
        else:
            print('Choix invalide, réessayez.')

if __name__ == "__main__":
    main()