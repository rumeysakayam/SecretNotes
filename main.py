from tkinter import *
from tkinter import messagebox
import base64

FONT = ("Arial", 16, "bold")

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

#window
window = Tk()
window.title("Secret Notes")
window.minsize(350, 600)
window.config(padx=30, pady=30)

#logo
logo = PhotoImage(file="image.png")
logo_label = Label(window, image=logo)
logo_label.pack()

#title
l_title = Label(window, text="Enter your title ", font=FONT)
l_title.pack()
title_entry = Entry(window)
title_entry.pack()

#secret
l_secret = Label(window, text="Enter your secret ", font=FONT)
l_secret.pack()
secret_text = Text(window)
secret_text.config(width=30, height=20)
secret_text.pack()

#key
l_key = Label(window, text="Enter master key ", font=FONT)
l_key.pack()
key_entry = Entry(window)
key_entry.pack()

#encryption
def save_encrypt_notes():
    title = title_entry.get()
    note = str(secret_text.get("1.0", END))
    key = key_entry.get()

    if len(title) == 0 or len(note) == 0 or len(key) == 0:
        messagebox.showwarning(title="Error!", message="Please enter all info")
    else:
        message_encrypted = encode(key, note)
        try:
            with open("mysecret.txt", mode="a") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}\n")
        except FileNotFoundError:
            with open("mysecret.txt", mode="w") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}\n")
        finally:
            title_entry.delete(0, END)
            secret_text.delete("1.0", END)
            key_entry.delete(0, END)



#decrypt text
def decrypt_notes():
    message_encrypted = secret_text.get("1.0", END)
    master_secret = key_entry.get()

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showwarning(title="Error!", message="Please enter all info")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            secret_text.delete("1.0", END)
            secret_text.insert("1.0", decrypted_message)
        except:
            messagebox.showwarning(title="Error!", message="Please enter encrypted text!")

#buttons
save_button = Button(window, text="Save & Encrypt", bg="white", fg="black", command=save_encrypt_notes)
save_button.pack()
decrypt_button = Button(window, text="Decrypt", bg="white", fg="black", command=decrypt_notes)
decrypt_button.pack()

window.mainloop()