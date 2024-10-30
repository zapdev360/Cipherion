import tkinter as tk
from tkinter import messagebox, Toplevel
from src.process import encrypt, decrypt
from src.db import dbcon, dbsave, dbget

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption/Decryption App")
        self.root.geometry("400x400")
        self.root.configure(bg="#2E4053")   
        self.root.withdraw()       
        self.show_login_dialog()

    def show_login_dialog(self):
      
        self.login_window = Toplevel(self.root)
        self.login_window.title("MySQL Authentication")
        self.login_window.geometry("300x200")
        self.login_window.configure(bg="#1ABC9C")

        tk.Label(self.login_window, text="MySQL Password:", bg="#1ABC9C").pack(pady=(20, 5))
        self.dbpass_entry = tk.Entry(self.login_window, show="*", width=30)
        self.dbpass_entry.pack()

        tk.Label(self.login_window, text="Database Name:", bg="#1ABC9C").pack(pady=5)
        self.dbname_entry = tk.Entry(self.login_window, width=30)
        self.dbname_entry.pack()

        tk.Button(self.login_window, text="Connect", command=self.authenticate).pack(pady=20)

    def authenticate(self):
        dbpass = self.dbpass_entry.get()
        dbname = self.dbname_entry.get()

        if dbcon(dbpass, dbname):
            messagebox.showinfo("Success", f"Connected to database '{dbname}'")
            self.login_window.destroy() 
            self.root.deiconify()  
            self.show_main_menu() 
        else:
            messagebox.showerror("Error", "Authentication failed! Please try again.")

    def show_main_menu(self):
        tk.Label(self.root, text="Choose an Option", bg="#2E4053", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

        # Encrypt Section
        tk.Label(self.root, text="Text to Encrypt:", bg="#2E4053", fg="white").pack(pady=(10, 5))
        self.ptext_entry = tk.Entry(self.root, width=50)
        self.ptext_entry.pack()

        tk.Button(self.root, text="Encrypt Text", command=self.encrypt_data).pack(pady=10)

        # Decrypt Section
        tk.Label(self.root, text="Record ID to Decrypt:", bg="#2E4053", fg="white").pack(pady=(20, 5))
        self.record_id_entry = tk.Entry(self.root, width=20)
        self.record_id_entry.pack()

        tk.Button(self.root, text="Decrypt Text", command=self.decrypt_data).pack(pady=10)

    def encrypt_data(self):
        ptext = self.ptext_entry.get()
        dbpass = self.dbpass_entry.get()
        dbname = self.dbname_entry.get()

        if ptext.strip():
            key, encdata = encrypt(ptext)
            recid = dbsave(encdata, key, dbpass, dbname)
            messagebox.showinfo("Success", f"Data encrypted and saved with record ID {recid}")
        else:
            messagebox.showerror("Input Error", "Please enter text to encrypt.")

    def decrypt_data(self):
        try:
            inrec = int(self.record_id_entry.get())
            dbpass = self.dbpass_entry.get()
            dbname = self.dbname_entry.get()

            rec = dbget(inrec, dbpass, dbname)
            if rec:
                ctext, key = rec
                dctext = decrypt(ctext, key)
                messagebox.showinfo("Decrypted Text", f"Decrypted text: {dctext}")
            else:
                messagebox.showwarning("Not Found", "Record not found!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid record ID.")

#if __name__ == "__main__":
#    root = tk.Tk()
#    app = EncryptionApp(root)
#    root.mainloop()
