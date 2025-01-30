from prettytable import PrettyTable

def menutab():
    menutab = PrettyTable()
    menutab.field_names = ["Choice", "Action"]
    
    menutab.add_row(["1", "Encrypt Data"])
    menutab.add_row(["2", "Decrypt Data"])
    menutab.add_row(["3", "Exit"])

    print(menutab)

def algotab():
    algotab = PrettyTable()
    algotab.field_names = ["Choice", "Algorithm", "Security"]
    
    algotab.add_row(["1", "AES", "Industry Standard"])
    algotab.add_row(["2", "ChaCha20Poly1305", "Strong"])
    algotab.add_row(["3", "Blowfish", "Moderate"])
    algotab.add_row(["4", "TripleDES", "Weak"])

    print(algotab)
