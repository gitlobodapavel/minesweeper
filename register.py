from tkinter import *
from tkinter import messagebox
import login as login_module
import sqlite3_connect_db


def register():
    def save_to_db():
        login_data = login.get()
        password_data = password.get()
        password2_data = password2.get()
        if password_data == '' or login_data == '':
            messagebox.showinfo("Minesweeper Game", 'Name and Password fields should not be empty !')
        elif len(password_data) < 6:
            messagebox.showinfo("Minesweeper Game", 'Password should be longer then 5 characters !')
        elif password_data != password2_data:
            messagebox.showinfo("Minesweeper Game", 'Password1 should be equal to Password2 !')
        else:
            sqlite3_connect_db.cursor.execute("INSERT INTO users VALUES (?, ?)", (login_data, password_data))
            sqlite3_connect_db.conn.commit()
            messagebox.showinfo("Minesweeper Game", 'Account has been created ! Now you can LogIn')
            root.destroy()
            login_module.login()

    root = Tk()
    root.title("GUI на Python")

    login = StringVar()
    password = StringVar()
    password2 = StringVar()

    login_label = Label(text="Login")
    password_label = Label(text="Password")
    password2_label = Label(text='Confirm Password')

    login_label.grid(row=0, column=0, sticky="w")
    password_label.grid(row=1, column=0, sticky="w")
    password2_label.grid(row=2, column=0, sticky="w")

    login_entry = Entry(textvariable=login)
    password_entry = Entry(textvariable=password)
    password2_entry = Entry(textvariable=password2)

    login_entry.grid(row=0, column=1, padx=5, pady=5)
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    password2_entry.grid(row=2, column=1, padx=5, pady=5)

    message_button = Button(text="Register", command=save_to_db)
    message_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

    root.mainloop()