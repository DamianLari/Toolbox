import json

def caesar_cipher_encrypt(text, key):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + key - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + key - 97) % 26 + 97)
        else:
            result += char
    return result

def caesar_cipher_decrypt(text, key):
    return caesar_cipher_encrypt(text, -key)

def caesar_cipher_decrypt_all(text):
    for key in range(1, 26):
        print(f'Key {key}: {caesar_cipher_decrypt(text, key)}')


def caesar_cipher_decrypt_most_likely(text):
    common_words = [
    "le", "de", "un", "et", "en", "à", "pour", "qui", "dans", "ce", "il", "que", "ne", "sur", "se", "pas", "par", "avec", "être", 
    "faire", "son", "avoir", "comme", "tout", "nous", "dire", "mais", "voir", "quelque", "donner", "bien", "où", "là", "si", "me", 
    "mon", "votre", "faire", "sa", "ces", "cette", "on", "aller", "autre", "quel", "elle", "aussi", "doit", "oui", "non", "encore", 
    "très", "jamais", "chez", "grand", "sous", "entre", "déjà", "peut", "deux", "trois", "premier", "depuis", "sans", "ainsi", "heure", 
    "jour", "fois", "tous", "deux", "pouvoir", "vouloir", "venir", "quelque", "chose", "peu", "personne", "année", "temps", "main", "part", 
    "prendre", "trouver", "donner", "nouveau", "parler", "savoir", "femme", "homme", "lieu", "partir", "petit", "vivre", "penser", "regarder", 
    "suivre", "entendre", "demander", "sentir", "rester", "quitter", "répondre", "croire", "monde", "voici", "où", "bon", "grand", "beau", "jeune", 
    "propre", "vieux", "gentil", "mauvais", "petit", "certain", "noir", "blanc", "plein", "vide", "riche", "pauvre", "lourd", "léger", "chaud", 
    "froid", "dur", "doux", "haut", "bas", "long", "court", "large", "étroit", "épais", "fin", "ancien", "nouveau", "bon", "mauvais", "même", 
    "différent", "tout", "aucun", "chaque", "quelque", "plusieurs", "tel", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", 
    "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf", "vingt", "trente", "quarante", 
    "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix", "cent", "mille", "million", "milliard"
    ]
    most_likely_text = ""
    most_likely_key = 0
    max_common_word_count = 0
    
    for key in range(1, 26):
        decrypted = caesar_cipher_decrypt(text, key)
        common_word_count = sum(decrypted.lower().count(word) for word in common_words)
        
        if common_word_count > max_common_word_count:
            max_common_word_count = common_word_count
            most_likely_text = decrypted
            most_likely_key = key
    return most_likely_text, most_likely_key