from tkinter import messagebox
from customtkinter import *
import sqlite3
from tkinter import *

set_appearance_mode('dark')


def criar_bd():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
    conn.commit()


def save():
    if ent_nm.get():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO pessoas (nome) VALUES ('{ent_nm.get().strip()}')")
        conn.commit()
        conn.close()
        ent_nm.delete(0, END)
        messagebox.showinfo("Beleza")


    else:
        print("Errô fi de Cristo")
        messagebox.showwarning("Belza")


def nomess():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")

    exibir = cursor.fetchall()
    print(exibir)
    row = ""

    for pessoas in exibir:
        row += f"\nID {pessoas[0]} - " + str(pessoas[1])

    listinha.configure(text=row)


root = CTk()
root.geometry('450x450')
root.title("Sistema Salva Nome")

text1 = CTkLabel(master=root, text="Sistema\nSalva Nome", font=("Arial", 20, "bold"))
text1.pack(pady=30)

ent_nm = CTkEntry(master=root, placeholder_text="Digite um nome:", width=160, font=("Arial", 14))
ent_nm.pack(pady=10)

salvar = CTkButton(master=root, text="Salvar", width=160, command=save)
salvar.pack(pady=5)

listar = CTkButton(master=root, text="Listar", width=160, command=nomess)
listar.pack(pady=10)

listinha = CTkLabel(master=root, text="", font=("Arial", 14))
listinha.pack(pady=10)


criar_bd()
root.mainloop()