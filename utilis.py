import random
import string

def generate_activation_key():
    pattern = "A1A1A-AAAAA-11111-AAA1A-11AA1"
    key = ""

    for char in pattern:
        if char == "A":
            key += random.choice(string.ascii_uppercase)
        elif char == "1":
            key += random.choice(string.digits)
        elif char == "-":
            key += "-"
    
    return key
