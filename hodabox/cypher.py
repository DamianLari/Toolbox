
def chiffrer_cesar_key(texte, decalage):
    resultat = ""
    for lettre in texte:
        if lettre.isalpha(): # Vérifier si le caractère est une lettre
            ascii_offset = 65 if lettre.isupper() else 97
            lettre_chiffree = chr((ord(lettre) - ascii_offset + decalage) % 26 + ascii_offset)
            resultat += lettre_chiffree
        else:
            resultat += lettre
    return resultat

def dechiffrer_cesar_key(texte, decalage):
    return chiffrer_cesar_key(texte, -decalage)