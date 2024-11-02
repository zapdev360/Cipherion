from prettytable import PrettyTable

def menutab():
    menu_table = PrettyTable()
    menu_table.field_names = ["Choice", "Action"]
    
    menu_table.add_row(["1", "Encrypt Data"])
    menu_table.add_row(["2", "Decrypt Data"])
    menu_table.add_row(["3", "Exit"])

    print(menu_table)

def algotab():
    algorithm_table = PrettyTable()
    algorithm_table.field_names = ["Choice", "Algorithm"]
    
    algorithm_table.add_row(["1", "AES"])
    algorithm_table.add_row(["2", "TripleDES"])
    algorithm_table.add_row(["3", "Blowfish"])
    algorithm_table.add_row(["4", "ChaCha20Poly1305"])

    print(algorithm_table)
