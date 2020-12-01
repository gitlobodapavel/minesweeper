from tkinter import *
import game
import results as statistic
import time
import os.path


def display():

    def easy():
        game.level = 'Easy'
        game.setup(4, 4, 2)

    def medium():
        game.level = 'Medium'
        game.setup(16, 16, 40)

    def hard():
        game.level = 'Hard'
        game.setup(16, 30, 90)

    def results():
        root.destroy()
        statistic.show()

    def get_self_results():
        root.destroy()
        statistic.show(game.username)

    def self_results():
        get_self_results()

    def continue_game():
        print('loading saved game...')

    root = Tk()

    if os.path.exists('save_'+str(game.username)+'.txt'):
        b6 = Button(text='Continue playing',
                    width=15, height=3)
        b6.config(command=continue_game)
        b6.pack()

    b1 = Button(text='Easy',
                width=15, height=3)
    b1.config(command=easy)
    b1.pack()
    b2 = Button(text='Medium',
                width=15, height=3)
    b2.config(command=medium)
    b2.pack()

    b3 = Button(text='Hard',
                width=15, height=3)
    b3.config(command=hard)
    b3.pack()

    b4 = Button(text='All Results',
                width=15, height=3)
    b4.config(command=results)
    b4.pack()

    b5 = Button(text='My Games',
                width=15, height=3)
    b5.config(command=self_results)
    b5.pack()

    root.mainloop()