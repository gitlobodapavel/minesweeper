from tkinter import *
import login as login_module, register as registration_module


def start():
    def login():
        root.destroy()
        login_module.login()

    def register():
        root.destroy()
        registration_module.register()

    root = Tk()
    b1 = Button(text='Login',
                width=15, height=3)
    b1.config(command=login)
    b1.pack()
    b2 = Button(text='Register',
                width=15, height=3)
    b2.config(command=register)
    b2.pack()

    root.mainloop()
