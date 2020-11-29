from tkinter import *
from tkinter import messagebox
import menu
import sqlite3_connect_db
import game


def login():
    def validate_data():
        login_data = login.get()
        password_data = password.get()

        if login == '' or password == '':
            messagebox.showinfo("Minesweeper Game", 'Name and Password fields should not be empty !')
        elif len(password_data) < 5:
            messagebox.showinfo("Minesweeper Game", 'Password should be longer then 5 characters !')
        else:
            sqlite3_connect_db.cursor.execute("SELECT * FROM users WHERE login = ? ", (login_data,))
            rows = sqlite3_connect_db.cursor.fetchall()
            if rows:
                if rows[0][0] == login_data and rows[0][1] == password_data:
                    root.destroy()
                    game.username = login_data
                    menu.display()
                else:
                    messagebox.showinfo("Minesweeper Game", 'Incorrect login or password !')
            else:
                messagebox.showinfo("Minesweeper Game", 'Cant find account with this login !')

    root = Tk()
    root.title("Minesweeper Game")

    login = StringVar()
    password = StringVar()

    login_label = Label(text="Login:")
    password_label = Label(text="Password")

    login_label.grid(row=0, column=0, sticky="w")
    password_label.grid(row=1, column=0, sticky="w")

    login_entry = Entry(textvariable=login)
    password_entry = Entry(textvariable=password)

    login_entry.grid(row=0, column=1, padx=5, pady=5)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    message_button = Button(text="Login", command=validate_data)
    message_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    root.mainloop()