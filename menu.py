from tkinter import *
import game
import results as statistic
import game_recovery
import os.path
import re


def display():

    def easy():
        game.level = 'Easy'
        root.destroy()
        game.setup(9, 9, 10)

    def medium():
        game.level = 'Medium'
        root.destroy()
        game.setup(16, 16, 40)

    def hard():
        game.level = 'Hard'
        root.destroy()
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
        save_file = open('save_'+game.username+'.txt')
        line = save_file.readlines()
        username = line[0]
        level = line[1]
        mines = eval(line[2])
        clear = eval(line[3])
        marked = eval(line[4])
        marked_grid=eval(line[5])

        reg = re.compile('[^a-zA-Z ]')

        if reg.sub('', level) == 'Medium':
            grid_height = 16
            grid_width = 16
        elif reg.sub('', level) == 'Easy':
            grid_height = 9
            grid_width = 9
        else:
            grid_height = 16
            grid_width = 30
        save_file.close()
        game_recovery.username = reg.sub('', username)
        game_recovery.level = reg.sub('', level)
        game_recovery.pre_gametime = int(round(float(line[6])))
        root.destroy()
        game_recovery.setup(grid_height, grid_width, 10, 50, mines, clear, marked, marked_grid)

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